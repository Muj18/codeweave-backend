# pytest test runner & harness
import re, os, json, hashlib, pathlib, datetime
from typing import Dict, Any, List, Tuple
import pytest, yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, meta

# ------------------------- Config -------------------------
REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE_DIRS = [
    REPO_ROOT / "templates",
    REPO_ROOT / "templates" / "snippets",
]
MAPPING_FILES = [
    REPO_ROOT / "template_mapping.json",
    REPO_ROOT / "template_mapping.yaml",
    REPO_ROOT / "template_mapping.yml",
]

ARTIFACTS_DIR = pathlib.Path(__file__).parent / "_artifacts"
SNAPSHOT_DIR = ARTIFACTS_DIR / "snapshots"
RENDER_DIR   = ARTIFACTS_DIR / "renders"
NOTES_DIR    = ARTIFACTS_DIR / "notes"

ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
RENDER_DIR.mkdir(parents=True, exist_ok=True)
NOTES_DIR.mkdir(parents=True, exist_ok=True)

# CLI flags
def pytest_addoption(parser):
    parser.addoption("--update-snapshots", action="store_true", default=False,
                     help="Update golden snapshots from current renders")
    parser.addoption("--no-snapshots", action="store_true", default=False,
                     help="Skip snapshot checks")
    parser.addoption("--family", action="append", default=[],
                     help="Only test templates whose path contains this substring (repeatable)")

@pytest.fixture(scope="session")
def opts(request):
    return {
        "update_snapshots": request.config.getoption("--update-snapshots"),
        "no_snapshots": request.config.getoption("--no-snapshots"),
        "families": request.config.getoption("--family") or [],
    }

# ------------------------- Helpers -------------------------
def _load_prompts() -> Dict[str, List[str]]:
    p = pathlib.Path(__file__).parent / "prompts.yaml"
    if p.exists():
        return yaml.safe_load(p.read_text()) or {}
    return {}

def _load_template_mapping() -> Dict[str, Dict[str, Any]]:
    for f in MAPPING_FILES:
        if f.exists():
            if f.suffix.lower() in [".yaml", ".yml"]:
                return yaml.safe_load(f.read_text()) or {}
            return json.loads(f.read_text())
    return {}

def _smart_fake_value(var: str):
    v = var.lower()
    now = datetime.datetime.utcnow().isoformat()

    # structured defaults for common template vars
    if v == "runner":
        return {"os": "ubuntu-latest"}
    if v == "flags":
        return {"skipChecks": False}
    if v in ("context", "env", "config"):
        return {"example": "value"}
    if v == "secrets":
        return {"API_KEY": "dummy-key", "TOKEN": "dummy-token"}
    if v == "artifacts":
        return {"path": "/tmp/output", "enabled": True}

    catalog = {
        "aws_region": "eu-west-1",
        "azure_region": "westeurope",
        "gcp_region": "europe-west2",
        "cluster_name": "prod-eks-primary",
        "project": "acme-platform",
        "environment": "production",
        "namespace": "core",
        "owner": "platform-team",
        "account_id": "123456789012",
        "vpc_id": "vpc-0abc1234def567890",
        "cidr": "10.0.0.0/16",
        "app": "payments-api",
        "service": "orders",
        "domain": "example.com",
        "now": now,
    }

    for key, val in catalog.items():
        if key in v:
            return val
    if "bool" in v or v.startswith("is_"):
        return True
    if "count" in v or "replica" in v:
        return 3
    if "timeout" in v:
        return 30
    if "url" in v:
        return "https://api.example.com"
    if "email" in v:
        return "platform-team@example.com"
    if "cost" in v or "budget" in v:
        return 1000

    return f"sample-{var}"

def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]

def _env():
    loader = FileSystemLoader([str(p) for p in TEMPLATE_DIRS if p.exists()])
    return Environment(
        loader=loader,
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True
    )

def _collect_templates() -> List[pathlib.Path]:
    paths = []
    for d in TEMPLATE_DIRS:
        if d.exists():
            for p in d.rglob("*.jinja2"):
                paths.append(p)
    return sorted(paths)

# ------------------------- Rubric -------------------------
def _load_rubric(tpl_path: pathlib.Path) -> Dict[str, Dict[str, Any]]:
    base = pathlib.Path(__file__).parent
    fname = tpl_path.name

    if "snippets" in str(tpl_path):
        rubric_path = base / "snippet_rubric.yaml"
    elif any(x in fname for x in ["playbook", "workflow", "helper", "troubleshoot", "code_generation"]):
        rubric_path = base / "playbook_rubric.yaml"
    else:
        rubric_path = base / "rubric.yaml"

    if not rubric_path.exists():
        raise FileNotFoundError(f"Missing rubric file: {rubric_path}")
    return yaml.safe_load(rubric_path.read_text()) or {}


def score_output(text: str, rubric: Dict[str, Dict[str, Any]]) -> Tuple[int, Dict[str, int]]:
    scores = {}
    total = 0
    for k, rule in rubric.items():
        pts = 0
        for group in rule.get("any_of", []):
            if all(kw.lower() in text.lower() for kw in group):
                pts = rule["points"]
                break
        scores[k] = pts
        total += pts
    return total, scores

# ------------------------- Tests -------------------------
@pytest.mark.parametrize("tpl_path", _collect_templates(), ids=lambda p: p.name)
def test_compile_and_render(tpl_path, opts):
    fams = opts["families"]
    if fams and not any(f in str(tpl_path) for f in fams):
        pytest.skip("filtered by --family")

    env = _env()
    src = tpl_path.read_text(encoding="utf-8")
    ast = env.parse(src)
    needed = sorted(meta.find_undeclared_variables(ast))

    mapping = _load_template_mapping().get(tpl_path.name, {})
    context = {}

    for k, v in mapping.items():
        context[k] = v

    for var in needed:
        if var not in context and not var.startswith(("loop", "cycler", "namespace")):
            context[var] = _smart_fake_value(var)

    # Ensure core defaults
    context.setdefault("tool", "Universal Playbook")
    context.setdefault("cloud", "multi-cloud (AWS/Azure/GCP)")
    context.setdefault("prompt", "Design a production-grade workload with automation, security, and cost controls.")

    template = env.get_template(tpl_path.name)

    try:
        out = template.render(**context)
    except Exception as e:
        NOTES_DIR.joinpath(tpl_path.name + ".json").write_text(json.dumps({
            "error": str(e),
            "needed_vars": needed,
            "context_keys": list(context.keys())
        }, indent=2))
        raise

    render_file = RENDER_DIR / f"{tpl_path.stem}.md"
    render_file.write_text(out, encoding="utf-8")

    if not opts["no_snapshots"]:
        snap_file = SNAPSHOT_DIR / f"{tpl_path.stem}.snap.md"
        if opts["update_snapshots"] or not snap_file.exists():
            snap_file.write_text(out, encoding="utf-8")
        else:
            expected = snap_file.read_text(encoding="utf-8")
            assert _normalize(out) == _normalize(expected), \
                f"Snapshot mismatch for {tpl_path.name}. Run with --update-snapshots to accept."

@pytest.mark.parametrize("tpl_path", _collect_templates(), ids=lambda p: p.name)
def test_rubric_scoring(tpl_path, opts):
    fams = opts["families"]
    if fams and not any(f in str(tpl_path) for f in fams):
        pytest.skip("filtered by --family")

    out_file = RENDER_DIR / f"{tpl_path.stem}.md"
    assert out_file.exists(), "Render artifacts missing; run compile_and_render first."
    text = out_file.read_text(encoding="utf-8")

    rubric = _load_rubric(tpl_path)
    total, breakdown = score_output(text, rubric)

    max_score = sum(v["points"] for v in rubric.values())

    # 🔑 stricter thresholding
    if "snippets" in str(tpl_path):
        threshold = 3  # snippet rubric, max 7
    elif any(x in tpl_path.name for x in ["playbook", "workflow", "helper", "troubleshoot", "code_generation"]):
        threshold = 7  # playbook rubric, max 12
    else:
        threshold = int(0.6 * max_score)  # full rubric, ~18/30

    NOTES_DIR.joinpath(tpl_path.name + ".rubric.json").write_text(json.dumps({
        "total": total,
        "breakdown": breakdown,
        "max": max_score,
        "threshold": threshold
    }, indent=2))

    assert total >= threshold, (
        f"Low rubric score for {tpl_path.name}: {total}/{max_score} "
        f"(minimum required: {threshold})."
    )
