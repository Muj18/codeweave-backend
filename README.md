# codeweave-backend

A FastAPI backend for CodeWeave – a DevOps & GenAI assistant using OpenAI.

## Setup

```bash
git clone https://github.com/Ahmed-Bensalem/codeweave-backend.git
cd codeweave-backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Setup

OPENAI_API_KEY=your-openai-key
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
EMAIL_RECIPIENT=support@yourdomain.com

## Running the app

```bash
uvicorn main:app --reload
```
The API will be available at:
http://localhost:8000
