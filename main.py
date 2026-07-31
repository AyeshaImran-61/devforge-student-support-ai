from fastapi import FastAPI
from pydantic import BaseModel

from agent import run_agent

app = FastAPI(
    title="DEVFORGE Student Support AI Agent",
    description="AI Agent for DEVFORGE Internship Students",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "Welcome to DEVFORGE Student Support AI Agent!",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    response = run_agent(request.message)

    return {
        "response": response
    }