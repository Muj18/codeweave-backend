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
from typing import Optional

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

class PromptRequest(BaseModel):
    tool: str
    prompt: str
    context: Optional[str] = None
    plan: str = "free"
    mode: Optional[str] = None

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

def detect_task_type(prompt: str, tool: str) -> str:
    p = prompt.lower()
    t = tool.lower()
    if t == "platform audit":
        return "platform_audit"
    kubernetes_and_containers = {"kubernetes", "docker", "openshift", "helm", "istio"}
    cloud_and_infra = {"aws", "azure", "gcp", "terraform", "flux", "ansible", "vault", "jenkins", "packer", "aws lambda"}
    genai = {"chatbot builder", "pdf / document qa bot", "rag pipeline", "data preprocessing pipeline",
             "fastapi backend for genai", "agent & tool builder", "model fine-tuning starter",
             "model training pipeline", "llm evaluation toolkit", "llm deployment", "vector db",
             "streamlit dashboard", "streamlit app", "langchain", "fine-tuning", "openai api", "hugging face",
             "agent & tools", "fastapi backend"}
    data_mlops = {"airflow / dbt", "vertex ai / sagemaker", "data preprocessing pipeline"}
    code_languages = {"python", "go", "bash", "typescript", "javascript", "java", "c#", "rust",
                      "powershell", "shell script", "other (script/code)", "bash script", "python script", "go script"}
    mlops_keywords = ["mlops", "ml pipeline", "ml model", "model training", "model testing", "model validation",
                      "model deployment", "model serving", "model monitoring", "model registry", "model versioning",
                      "training loop", "training job", "experiment tracking", "hyperparameter tuning", "batch training",
                      "automl", "pytorch", "tensorflow", "onnx", "tfx", "kubeflow", "mlflow", "vertex ai", "sagemaker",
                      "azure ml", "google ai platform", "ai platform", "training pipeline", "model evaluation",
                      "online inference", "offline inference", "real-time prediction", "docker for ml", "ci/cd for ml",
                      "deploy model", "test model", "fine-tune model", "llm training", "training script", "training dataset"]
    data_architecture_keywords = [
        "data architecture", "data modeling", "data schema", "data ingestion", "data transformation",
        "data pipeline", "data quality", "data validation", "data integration", "data lineage",
        "data lake", "datalake", "data warehouse", "data mart", "data platform", "data flow",
        "etl", "elt", "extract transform load", "batch processing", "stream processing",
        "bigquery", "redshift", "snowflake", "synapse", "hudi", "iceberg", "delta lake", "delta",
        "lakehouse", "schema evolution", "columnar storage", "parquet", "avro", "orc", "data mesh",
        "metadata store", "data catalog", "data governance", "dbt", "airflow", "apache beam", "glue job",
        "warehouse design", "data system", "data sync", "data sharding", "big data", "distributed storage"
    ]
    troubleshooting_keywords = ["error", "bug", "crash"]

    normalized_tool = t.strip().lower()
    if any(w in p for w in troubleshooting_keywords):
        return "troubleshooting"
    if normalized_tool in kubernetes_and_containers:
        return "troubleshooting"
    if normalized_tool in cloud_and_infra:
        return "architecture"
    if normalized_tool in genai:
        return "genai"
    if normalized_tool in data_mlops:
        if any(w in p for w in mlops_keywords):
            return "mlops"
        if any(w in p for w in data_architecture_keywords):
            return "data_architecture"
        return "architecture"
    if normalized_tool in code_languages:
        return "code_gen"
    if normalized_tool == "troubleshooting":
        return "troubleshooting"
    return "architecture"

def render_template(task_type: str, tool_type: str, prompt: str, context: Optional[str] = None, mode: Optional[str] = None):
    template_name = None
    if task_type == "platform_audit":
        template_name = "platform_audit.jinja2"
    elif task_type == "genai":
        template_name = "genai_architecture.jinja2"
    elif task_type == "architecture":
        template_name = "solutions_architecture.jinja2"
    elif task_type == "mlops":
        template_name = "mlops_architecture.jinja2"
    elif task_type == "data_architecture":
        template_name = "data_architecture.jinja2"
    elif task_type == "troubleshooting":
        template_name = "troubleshooting.jinja2"
    elif task_type == "code_gen":
        template_name = "code_generation.jinja2"

    if not template_name:
        return f"You are a DevOps AI assistant for {tool_type}. Only return valid code. Prompt: {prompt}"

    template = env.get_template(template_name)

    # ✅ Prevent duplication for Platform Audit by clearing context
    if template_name == "platform_audit.jinja2":
        context = None  

    rendered = template.render(
        prompt=prompt,
        tool=tool_type,
        context=context,
        mode=mode
    )

    if template_name == "platform_audit.jinja2":
        assert "TEMPLATE_VERSION: 2025-08-11 LeanExec" in rendered, "Wrong audit template version loaded"

    return rendered

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

async def stream_paged_completion(model: str, system_guard: str, initial_user_content: str, desired_cap: int):
    temperature = 0.3
    max_pages = 6
    page = 1
    full_text = ""
    current_prompt = initial_user_content

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
        )

        page_buf = ""
        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                page_buf += content

        if "[CONTINUE_NEEDED]" in page_buf:
            trimmed = page_buf.replace("[CONTINUE_NEEDED]", "").rstrip()
            if trimmed:
                yield trimmed
                full_text += trimmed
            tail = full_text[-3000:]
            current_prompt = (
                initial_user_content
                + "\n\n---\n"
                + "Continue from where you left off. Do not repeat prior text. "
                + "If you hit limit again, end with [CONTINUE_NEEDED].\n"
                + "Tail context:\n<<<TAIL>>>\n"
                + tail
                + "\n<<<END_TAIL>>>"
            )
            page += 1
            continue
        else:
            if page_buf:
                yield page_buf
                full_text += page_buf
            break

    if is_unresolved(full_text):
        log_unresolved_issue({"task": "platform_audit", "response": full_text})
        email_issue({"task": "platform_audit", "response": full_text})

@app.post("/generate")
async def generate_code(req: PromptRequest):
    task_type = detect_task_type(req.prompt, req.tool)
    rendered_prompt = render_template(
        task_type=task_type,
        tool_type=req.tool,
        prompt=req.prompt,
        context=req.context,
        mode=req.mode or "summary"
    )

    print("[DEBUG] FIRST_200]\n", rendered_prompt[:200])

    model = "gpt-3.5-turbo" if (req.plan or "free").lower() == "free" else "gpt-4o"
    desired_cap = 3000

    print("[DEBUG] PROMPT TOKENS:", count_tokens(model, rendered_prompt))

    async def token_stream():
        try:
            async for chunk in stream_paged_completion(
                model=model,
                system_guard=SYSTEM_GUARD,
                initial_user_content=rendered_prompt,
                desired_cap=desired_cap,
            ):
                yield chunk
            if req.tool and req.tool.lower() in ["architecture", "genai", "platform_audit"]:
                yield FOOTER
        except Exception as e:
            import traceback
            print("[DEBUG] Exception in token_stream:", str(e))
            traceback.print_exc()
            yield f"\n\n[Error]: {str(e)}"

    return StreamingResponse(token_stream(), media_type="text/plain")
