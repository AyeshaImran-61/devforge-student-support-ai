from fastapi import FastAPI
from pydantic import BaseModel

from agent import run_agent

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="DEVFORGE Student Support AI Agent",
    description="AI Agent for DEVFORGE Internship Students",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return FileResponse("static/index.html")


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