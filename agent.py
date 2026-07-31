from typing import TypedDict

from langgraph.graph import StateGraph, END

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMAAPIKEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

client = OpenAI(
    api_key=OLLAMA_API_KEY,
    base_url="https://ollama.com/v1"
)


# -----------------------------
# State
# -----------------------------
class AgentState(TypedDict):
    message: str
    response: str
    is_related: bool


# -----------------------------
# Node 1: Classifier
# -----------------------------
TECH_KEYWORDS = [
    "python",
    "fastapi",
    "langchain",
    "langgraph",
    "github",
    "render",
    "ai",
    "machine learning",
    "deployment",
    "assignment",
    "project",
    "internship",
    "devforge",
]


def classify_question(state: AgentState):
    message = state["message"].lower()

    related = any(keyword in message for keyword in TECH_KEYWORDS)

    state["is_related"] = related

    return state


# -----------------------------
# Node 2: AI Support
# -----------------------------
def ai_support(state: AgentState):
    print("API Key Exists:", bool(OLLAMA_API_KEY))
    print("Model:", OLLAMA_MODEL)
    print("Base URL:", client.base_url)     
    response = client.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the DEVFORGE Student Support AI Agent. "
                    "Help students with Python, AI Engineering, FastAPI, "
                    "LangChain, LangGraph, GitHub, Render deployment, "
                    "assignments and internship learning."
                ),
            },
            {
                "role": "user",
                "content": state["message"],
            },
        ],
    )

    state["response"] = response.choices[0].message.content

    return state


# -----------------------------
# Node 3: Safe Response
# -----------------------------
def safe_response(state: AgentState):
    state["response"] = (
        "I'm designed to help DEVFORGE internship students with "
        "Python, AI Engineering, FastAPI, LangChain, LangGraph, "
        "GitHub, Render deployment, and project guidance."
    )

    return state


# -----------------------------
# Conditional Routing
# -----------------------------
def route(state: AgentState):
    if state["is_related"]:
        return "ai_support"

    return "safe_response"


# -----------------------------
# Build Graph
# -----------------------------
builder = StateGraph(AgentState)

builder.add_node("classifier", classify_question)
builder.add_node("ai_support", ai_support)
builder.add_node("safe_response", safe_response)

builder.set_entry_point("classifier")

builder.add_conditional_edges(
    "classifier",
    route,
    {
        "ai_support": "ai_support",
        "safe_response": "safe_response",
    },
)

builder.add_edge("ai_support", END)
builder.add_edge("safe_response", END)

graph = builder.compile()


# -----------------------------
# Function used by FastAPI
# -----------------------------
def run_agent(message: str):
    result = graph.invoke(
        {
            "message": message,
            "response": "",
            "is_related": False,
        }
    )

    return result["response"]