from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()

# ✅ Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your real domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class PromptRequest(BaseModel):
    tool: str
    prompt: str

@app.post("/generate")
def generate_code(req: PromptRequest):
    system_msg = f"You are a DevOps AI assistant for {req.tool}. Only return valid code (no markdown or explanation)."
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": req.prompt}
        ],
        temperature=0.2,
        max_tokens=1500
    )

    return {"code": response.choices[0].message.content}
