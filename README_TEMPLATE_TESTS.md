# CodeWeave Jinja2 Template Test Harness

Drop this folder in the **root** of your repo and run the tests to validate every `.jinja2` template and snippet.

## What it does
1) **Static checks** – compiles templates with `StrictUndefined`, finds **undefined/unused variables**, missing filters/globals.
2) **Render tests** – renders each template with *smart fake data* or provided fixtures, then writes outputs to `tests/_artifacts/`.
3) **Snapshot tests** – compares outputs to saved snapshots (first run will create them).
4) **Rubric scoring** – auto-scores each render against a staff-level rubric (security, cost, HA, multi-cloud, steps, diagrams, risks, etc.).
5) **Prompt coverage** – lets you run multiple prompts per template family (e.g., EKS, Terraform, GenAI, Troubleshooting).

## Quick start
```bash
pip install -U pytest jinja2 pyyaml
pytest -q
# or update snapshots on purpose:
pytest -q --update-snapshots
# run only rubric scoring summary:
pytest -q -k rubric --no-snapshots
```
Artifacts: `tests/_artifacts/` (renders, JSON notes, and rubric scores).

## Repo assumptions
- Templates under `templates/*.jinja2` and `templates/snippets/*.jinja2`
- Optional `template_mapping.(json|yaml)` describes variables per template
- Optional `tests/fixtures/*.yaml` for domain-specific contexts

> If your paths differ, tweak `TEMPLATE_DIRS` in `tests/run_template_tests.py`.
