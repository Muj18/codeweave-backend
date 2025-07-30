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

def detect_task_type(prompt: str, tool: str) -> str:
    p = prompt.lower()
    t = tool.lower()


    troubleshooting_keywords = [
        "error", "bug", "crash", "timeout", "stack trace", "traceback",
        "failed", "issue", "not working", "unexpected", "exception", "panic"
    ]

    code_gen_indicators = [
        "main.tf", "variables.tf", "outputs.tf", "terraform file", "terraform setup",
        "dockerfile", "docker-compose", "helm chart", "cloudformation", "pipeline file",
        "ci/cd yaml", "cicd file", "workflow file", ".yaml", ".yml", ".json", ".hcl",
        ".tf", ".py", ".sh", "generate file", "write file", "create file", "multifile"
    ]
    if any(word in p for word in code_gen_indicators):
        return "genai"

    architecture_keywords = [
        "architecture", "design", "blueprint", "infrastructure", "high availability",
        "multi-tenant", "scaling", "autoscaling", "deployment", "cluster",
        "cloud", "load balancer", "vpc", "fargate", "ecs", "eks", "aks", "gke",
        "s3", "rds", "lambda", "container", "microservice", "serverless",
        "distributed", "kubernetes", "helm", "terraform", "ansible", "packer",
        "vault", "cicd", "ci/cd", "jenkins", "github actions", "gitlab ci",
        "devops", "infrastructure as code", "iac", "provision", "pipeline"
    ]

    genai_keywords = [
        "rag", "llm", "langchain", "agent", "retriever", "embedding", "tokenizer",
        "fine-tune", "finetune", "finetuning", "vector db", "faiss", "pinecone",
        "openai", "hugging face", "model training", "prompt", "prompt tuning",
        "streamlit", "inference", "transformer", "dataset", "generation",
        "qa bot", "pdf bot", "chatbot", "evaluation", "summarize", "sentiment"
    ]

    if any(word in p for word in troubleshooting_keywords):
        return "troubleshooting"
    elif any(word in p for word in genai_keywords):
        return "genai"
    elif any(word in p for word in architecture_keywords):
        return "architecture"

    if t in {
        "chatbot builder", "pdf / document qa bot", "rag pipeline", "data preprocessing pipeline",
        "fastapi backend for genai", "agent & tool builder", "model fine-tuning starter",
        "model training pipeline", "llm evaluation toolkit", "llm deployment", "vector db",
        "streamlit dashboard", "streamlit app", "langchain", "fine-tuning", "openai api",
        "hugging face", "agent & tools",  "fastapi backend", "bash script", "python script", "go script",
    }:
        return "genai"

    if t in {
        "aws", "azure", "gcp", "terraform", "kubernetes", "docker", "helm", "flux", "ansible",
        "vault", "jenkins", "packer", "aws lambda",
    }:
        return "architecture"

    if t == "troubleshooting":
        return "troubleshooting"

    return "code_gen"

def render_template(task_type: str, tool_type: str, prompt: str, context: str = None):
    template_name = None

    if task_type == "genai":
        template_name = "genai_architecture.jinja2"
    elif task_type == "architecture":
        template_name = "solutions_architecture.jinja2"
    elif task_type == "troubleshooting":
        template_name = "troubleshooting.jinja2"
    elif task_type == "code_gen":
        return f"You are a DevOps AI assistant for {tool_type}. Only return valid code. No explanations or markdown.\nPrompt: {prompt}"

    if not template_name:
        return f"You are a DevOps AI assistant for {tool_type}. Only return valid code. No explanations or markdown.\nPrompt: {prompt}"
    template = env.get_template(template_name)
    return template.render(prompt=prompt, tool=tool_type, context=context)

def is_unresolved(response: str) -> bool:
    return any(keyword in response.lower() for keyword in [
        "afraid", "not sure", "unable", "can't", "unknown", "contact support", "doesn’t seem"
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
    system_prompt = render_template(task_type, tool_type, req.prompt, req.context)
    temperature = 0.3 if task_type in ["troubleshooting", "architecture"] else 0.2

    async def token_stream():
        try:
            full_response = ""
            stream = await client.chat.completions.create(
                model="gpt-4",
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