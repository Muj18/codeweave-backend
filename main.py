from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AsyncOpenAI
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import asyncio
import json
import smtplib
from email.message import EmailMessage

load_dotenv()

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
    context: str = None
    plan: str = "free"

def detect_task_type(prompt: str, tool: str) -> str:
    p = prompt.lower()
    t = tool.lower()

    if t == "platform audit":
        return "platform_audit"

    kubernetes_and_containers = {
        "kubernetes", "docker", "openshift", "helm", "istio"
    }

    cloud_and_infra = {
        "aws", "azure", "gcp", "terraform", "flux", "ansible", "vault",
        "jenkins", "packer", "aws lambda"
    }

    genai = {
        "chatbot builder", "pdf / document qa bot", "rag pipeline",
        "data preprocessing pipeline", "fastapi backend for genai",
        "agent & tool builder", "model fine-tuning starter",
        "model training pipeline", "llm evaluation toolkit", "llm deployment",
        "vector db", "streamlit dashboard", "streamlit app", "langchain",
        "fine-tuning", "openai api", "hugging face", "agent & tools",
        "fastapi backend"
    }

    data_mlops = {
        "airflow / dbt", "vertex ai / sagemaker", "data preprocessing pipeline"
    }

    code_languages = {
        "python", "go", "bash", "typescript", "javascript", "java", "c#", "rust",
        "powershell", "shell script", "other (script/code)", "bash script", "python script", "go script"
    }

    mlops_keywords = [
        "mlops", "ml pipeline", "ml model", "model training", "model testing", "model validation",
        "model deployment", "model serving", "model monitoring", "model registry", "model versioning",
        "training loop", "training job", "experiment tracking", "hyperparameter tuning", "batch training",
        "automl", "pytorch", "tensorflow", "onnx", "tfx", "kubeflow", "mlflow", "vertex ai", "sagemaker",
        "azure ml", "google ai platform", "ai platform", "training pipeline", "model evaluation", 
        "online inference", "offline inference", "real-time prediction", "docker for ml", "ci/cd for ml",
        "deploy model", "test model", "fine-tune model", "llm training", "training script", "training dataset"
    ]


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


    troubleshooting_keywords = [
        "error", "bug", "crash"
    ]

    normalized_tool = t.strip().lower()

    if any(word in p for word in troubleshooting_keywords):
        return "troubleshooting"

    if normalized_tool in kubernetes_and_containers:
        return "troubleshooting"

    if normalized_tool in cloud_and_infra:
        return "architecture"

    if normalized_tool in genai:
        return "genai"

    if normalized_tool in data_mlops:
        if any(word in p for word in mlops_keywords):
            return "mlops"
        if any(word in p for word in data_architecture_keywords):
            return "data_architecture"
        return "architecture" 

    if normalized_tool in code_languages:
        return "code_gen"

    if normalized_tool == "troubleshooting":
        return "troubleshooting"

    return "architecture"

def render_template(task_type: str, tool_type: str, prompt: str, context: str = None):
    template_name = None

    if task_type == "platform_audit":
        template_name = "platform_audit.jinja2"
    if task_type == "genai":
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
        return f"You are a DevOps AI assistant for {tool_type}. Only return valid code. No explanations or markdown.\nPrompt: {prompt}"

    template = env.get_template(template_name)
    return template.render(prompt=prompt, tool=tool_type, context=context)

def is_unresolved(response: str) -> bool:
    return any(keyword in response.lower() for keyword in [
        "sorry", "afraid", "not sure", "unable", "can't", "unknown", "doesn’t seem"
    ])

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

FOOTER = """

"""

@app.post("/generate")
async def generate_code(req: PromptRequest):
    task_type = detect_task_type(req.prompt, req.tool)
    tool_type = req.tool
    plan = req.plan or "free"
    system_prompt = render_template(task_type, tool_type, req.prompt, req.context)
    temperature = 0.3 if task_type in ["troubleshooting", "architecture"] else 0.2

    async def token_stream():
        try:
            full_response = ""
            stream = await client.chat.completions.create(
                model = "gpt-3.5-turbo" if plan == "free" else "gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": req.prompt}
                ],
                temperature=temperature,
                max_tokens=2000,
                stream=True,
            )
            buffer = []
            total_length = 0

            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
                    full_response += content
                    total_length += len(content)

            if total_length > 700 and task_type in ["architecture", "genai"]:
                yield FOOTER
            
            if is_unresolved(full_response):
                print("Unresolved issue detected, logging and emailing...")
                issue_data = {
                    "prompt": req.prompt,
                    "context": req.context,
                    "task_type": task_type,
                    "tool_type": tool_type,
                    "response": full_response
                }
                log_unresolved_issue(issue_data)
                print("Logging unresolved issue to file...")
                email_issue(issue_data)
                print("Emailing unresolved issue to support...")
                
        except Exception as e:
            yield f"\n\n[Error]: {str(e)}"

    return StreamingResponse(token_stream(), media_type="text/plain")
