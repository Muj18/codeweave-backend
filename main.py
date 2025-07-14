from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Set up CORS (adjust allow_origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["https://codeweave.co"] in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define input schema for /generate route
class GenerateRequest(BaseModel):
    tool: str
    prompt: str

# Route: POST /generate
@app.post("/generate")
async def generate_code(payload: GenerateRequest):
    tool = payload.tool
    prompt = payload.prompt

    system_msg = (
        "You are a DevOps and GenAI assistant. Return production-ready code only. "
        "Use correct formats: HCL, YAML, Python, etc. No markdown or explanations."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2000
        )
        code = response.choices[0].message.content
        return {"code": code}
    except Exception as e:
        return {"error": str(e)}
