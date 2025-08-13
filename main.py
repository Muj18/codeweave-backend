import os
from dotenv import load_dotenv

# Load from .env in the project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("❌ OPENAI_API_KEY not found in .env file")

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

MODEL_LIMITS = {
    "gpt-3.5-turbo": 4096,
    "gpt-4o": 4096,
    "gpt-4o-mini": 4096,
}

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
    limit = MODEL_LIMITS.get(model_name, 4096)
    prompt_tokens = count_tokens(model_name, prompt_text)
    remaining = max(256, limit - prompt_tokens - buffer)
    return max(256, min(desired_cap, remaining))

# --- Generate route ---
@app.post("/generate")
async def generate_code(req: PromptRequest):
    print("DEBUG Request Payload:", req.dict())

    # Look up template from mapping file
    template_name = TEMPLATE_MAP.get(req.tool)

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

    model = "gpt-3.5-turbo" if (req.plan or "free").lower() == "free" else "gpt-4o"
    desired_cap = 3000

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
