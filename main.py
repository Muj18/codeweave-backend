import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AsyncOpenAI
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import smtplib
from email.message import EmailMessage
from typing import Optional, List
import re
import hashlib

# Import the new mapping file
from template_mapping import TEMPLATE_MAP

# Load from .env in the project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("❌ OPENAI_API_KEY not found in .env file")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

# --- Capability keywords ---
CAPABILITY_KEYWORDS = {
    "k8s_core": ["k8", "kubernetes", "pod", "deployment", "hpa", "node", "eks", "gke", "aks", "crashloopbackoff"],
    "ingress_lb": ["ingress", "nginx", "alb", "nlb", "elb", "agic", "gateway", "istio", "traefik", "load balancer", "target group", "unhealthy"],
    "db_sql": ["postgres", "postgresql", "mysql", "mariadb", "aurora", "rds", "cloud sql", "too many clients", "max connections", "connection pool"],
    "cache_kv": ["redis", "memcached", "cache", "hot key"],
    "messaging_streams": ["kafka", "msk", "eventhub", "pubsub", "rabbitmq", "nats", "consumer lag"],
    "iac_state": ["terraform", "tfstate", "backend.hcl", "terragrunt", "state lock", "force-unlock", "s3 state"],
    "observability": ["prometheus", "grafana", "datadog", "new relic", "opentelemetry", "apm", "trace", "metrics", "logs"],
    "storage_obj": ["s3", "gcs", "blob", "object storage", "bucket", "signed url", "403", "access denied"],
    "auth_network": ["iam", "irsa", "managed identity", "service account", "role", "security group", "nacl", "firewall", "nat", "vpc", "subnet", "dns"],
}

def detect_capabilities(text: str) -> List[str]:
    t = (text or "").lower()
    caps: List[str] = []
    for cap, keys in CAPABILITY_KEYWORDS.items():
        if any(k in t for k in keys):
            caps.append(cap)
    if "observability" not in caps:
        caps.append("observability")
    return caps

# --- Request model ---
class PromptRequest(BaseModel):
    tool: str
    prompt: str
    context: Optional[str] = None
    plan: str = "free"
    mode: Optional[str] = None
    capabilities: Optional[List[str]] = None  # NEW

# --- Updated model limits ---
MODEL_LIMITS = {
    "gpt-5-nano": 128_000,
    "gpt-5-mini": 128_000,
    "gpt-5": 128_000,
}

# --- Plan → model mapping ---
def choose_model_from_plan(plan: str | None) -> str:
    p = (plan or "free").strip().lower()
    if p == "free":
        return "gpt-5-nano"
    if p in {"pro", "teams"}:
        return "gpt-5-mini"
    return "gpt-5"  # enterprise / fallback

def _rough_token_count(text: str) -> int:
    words = max(1, len(text.split()))
    chars = len(text)
    return int(min(words * 1.3, chars / 4))

try:
    import tiktoken
    def count_tokens(model_name: str, text: str) -> int:
        try:
            enc = tiktoken.encoding_for_model(model_name)
        except KeyError:
            enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
except Exception:
    def count_tokens(model_name: str, text: str) -> int:
        return _rough_token_count(text)

def safe_max_tokens(model_name: str, prompt_text: str, desired_cap: int, buffer: int = 200) -> int:
    limit = MODEL_LIMITS.get(model_name, 128_000)
    prompt_tokens = count_tokens(model_name, prompt_text)
    remaining = max(256, limit - prompt_tokens - buffer)
    return max(256, min(desired_cap, remaining))

def is_unresolved(response: str) -> bool:
    return any(k in response.lower() for k in ["sorry", "afraid", "not sure", "unable", "can't", "unknown", "doesn’t seem"])

def log_unresolved_issue(data: dict):
    with open("unresolved_issues.jsonl", "a") as f:
        f.write(json.dumps(data) + "\n")

def email_issue(issue_data: dict):
    sender_email = os.getenv("EMAIL_USER")
    sender_pass = os.getenv("EMAIL_PASS")
    recipient_email = os.getenv("EMAIL_RECIPIENT")
    if not (sender_email and sender_pass and recipient_email):
        return
    msg = EmailMessage()
    msg["Subject"] = "🚨 Unresolved DevOps/GenAI Issue"
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content(json.dumps(issue_data, indent=2))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_pass)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Email failed: {e}")

FOOTER = "\n"

SYSTEM_GUARD = (
    "You are a senior cloud architect. Follow the provided audit structure exactly. "
    "DO NOT recommend service mesh, multi-region, or new managed products unless justified. "
    "Prioritize cost cuts and simplification first. "
    "If you cannot finish due to length, end with: [CONTINUE_NEEDED]."
)

def _norm_text_for_dedupe(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())

# --- Streaming completion ---
async def stream_paged_completion(model: str, system_guard: str, initial_user_content: str, desired_cap: int):
    temperature = 0.3
    max_pages = 4
    page = 1
    full_text = ""
    seen_hashes = set()
    current_prompt = initial_user_content
    HARD_STOP_TOKENS = [
        "📬 For hands-on execution",
        "## 🚀 Executive Snapshot",
        "<<<END_TAIL>>>",
    ]

    while page <= max_pages:
        prompt_tokens = count_tokens(model, current_prompt)
        max_tokens = safe_max_tokens(model, current_prompt, desired_cap=desired_cap, buffer=200)
        print(f"[DEBUG] PAGE {page} | MAX_TOKENS {max_tokens} | PROMPT_TOKENS {prompt_tokens}")

        stream = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_guard},
                {"role": "user", "content": current_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            stop=HARD_STOP_TOKENS,
        )
        
        page_buf = ""
        async for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            if content:
                page_buf += content

        if not page_buf.strip():
            break

        page_hash = hashlib.sha256(_norm_text_for_dedupe(page_buf).encode()).hexdigest()
        if page_hash in seen_hashes:
            break
        seen_hashes.add(page_hash)

        if _norm_text_for_dedupe(page_buf) in _norm_text_for_dedupe(full_text):
            break

        if "[CONTINUE_NEEDED]" in page_buf:
            trimmed = page_buf.replace("[CONTINUE_NEEDED]", "").rstrip()
            yield trimmed
            full_text += trimmed
        else:
            yield page_buf
            full_text += page_buf

        if "[CONTINUE_NEEDED]" not in page_buf:
            break

        tail = full_text[-3000:]
        current_prompt = (
            initial_user_content
            + "\n\n---\n"
            + "Continue from where you left off. Do not repeat prior text. "
              "If you hit limit again, end with [CONTINUE_NEEDED].\n"
              "Tail context:\n<<<TAIL>>>\n"
            + tail
            + "\n<<<END_TAIL>>>"
        )
        page += 1

    if is_unresolved(full_text):
        log_unresolved_issue({"task": "platform_audit", "response": full_text})
        email_issue({"task": "platform_audit", "response": full_text})

# --- Generate route ---
@app.post("/generate")
async def generate_code(req: PromptRequest):
    print("DEBUG Request Payload:", req.dict())

    # --- Normalize tool key to lowercase for safe lookup ---
    tool_key = (req.tool or "").strip().lower()
    template_map_normalized = {k.lower(): v for k, v in TEMPLATE_MAP.items()}
    template_name = template_map_normalized.get(tool_key)

    print(f"[DEBUG] Tool requested: {req.tool} -> Using template: {template_name}")
    
    # If not found, default to solutions_architecture
    if not template_name:
        template_name = "solutions_architecture.jinja2"

    template = env.get_template(template_name)

    # Render prompt based on template type
    if template_name == "troubleshooting.jinja2":
        caps = req.capabilities or detect_capabilities(f"{req.prompt} {req.tool} {req.context or ''}")
        rendered_prompt = template.render(
            prompt=req.prompt,
            tool=req.tool,
            context=req.context,
            mode=req.mode or "summary",
            capabilities=caps,
        )
    else:
        rendered_prompt = template.render(
            prompt=req.prompt,
            tool=req.tool,
            context=req.context,
            mode=req.mode or "summary",
        )

    # --- Select model & token budget (updated for GPT-5 family) ---
    model = choose_model_from_plan(req.plan)

    if model == "gpt-5-nano":
        desired_cap = 1_200   # small cap for free users
    elif model == "gpt-5-mini":
        desired_cap = 6_000   # generous engineer cap
    else:  # gpt-5
        desired_cap = 20_000  # enterprise cap

    prompt_tokens = count_tokens(model, rendered_prompt)
    desired_cap = safe_max_tokens(model, rendered_prompt, desired_cap=desired_cap, buffer=800)

    async def token_stream():
        try:
            async for chunk in stream_paged_completion(
                model=model,
                system_guard=SYSTEM_GUARD,
                initial_user_content=rendered_prompt,
                desired_cap=desired_cap,
            ):
                yield chunk
            if req.tool and req.tool.lower() in ["architecture", "genai", "platform audit", "platform_audit"]:
                yield FOOTER
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield f"\n\n[Error]: {str(e)}"

    return StreamingResponse(token_stream(), media_type="text/plain")