from typing import TypedDict, List

from langgraph.graph import StateGraph, END

import os

from dotenv import load_dotenv
from openai import OpenAI

from faq import FAQS

from langchain_community.document_loaders import DirectoryLoader, TextLoader

from rag import search_knowledge

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMAAPIKEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")


if not OLLAMA_API_KEY:
    raise ValueError(
        "OLLAMAAPIKEY is missing. Please add it to your .env file."
    )

if not OLLAMA_MODEL:
    raise ValueError(
        "OLLAMA_MODEL is missing. Please add it to your .env file."
    )
    
client = OpenAI(
    api_key=OLLAMA_API_KEY,
    base_url="https://ollama.com/v1"
)

# -----------------------------
# Load Knowledge Base
# -----------------------------
try:
    loader = DirectoryLoader(
        "knowledge",
        glob="*.txt",
        loader_cls=TextLoader
    )

    documents = loader.load()

    KNOWLEDGE = "\n\n".join(doc.page_content for doc in documents)

    print(f"Loaded {len(documents)} knowledge files.")

except Exception as e:
    KNOWLEDGE = ""
    print("Knowledge Base Error:", e)

# -----------------------------
# State
# -----------------------------
class AgentState(TypedDict):
    message: str
    response: str
    is_related: bool
    history: List[dict]
    is_faq: bool
  

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


def faq_node(state: AgentState):
    message = state["message"].lower()

    for question, answer in FAQS.items():
        if question in message:
            state["response"] = answer
            state["is_faq"] = True
            return state

    state["is_faq"] = False
    return state


# -----------------------------
# Node 2: AI Support
# -----------------------------
def ai_support(state: AgentState):

    try:

        rag = search_knowledge(state["message"])

        if rag:
            context = rag["content"]
            source = rag["source"]
        else:
            context = "No relevant DEVFORGE knowledge found."
            source = "AI Knowledge"

        response = client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are the DEVFORGE Student Support AI.

Use the following knowledge to answer the user's question.

Knowledge Source:
{source}

Knowledge:
{context}

If the answer is not available in the knowledge, answer using your own AI knowledge.

Always answer professionally.

Always use Markdown formatting.

Use headings.

Use bullet points.

Use numbered steps whenever explaining.

Use tables if comparing concepts.

Wrap code inside Markdown code blocks.

Be concise but informative.

At the end of every answer write:

---
**Source:** {source}
"""
                },

                *state["history"],

                {
                    "role": "user",
                    "content": state["message"],
                },
            ],
        )

        state["response"] = response.choices[0].message.content

    except Exception as e:

        state["response"] = (
            "❌ Unable to contact the AI model.\n\n"
            f"Error: {str(e)}"
        )

    return state
# Keep only last 10 messages
    state["history"] = state["history"][-10:]
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



def format_response(state: AgentState):

    state["response"] = (
        "🎓 DEVFORGE Student Support AI\n\n"
        + state["response"]
        + "\n\n✅ Need more help? Ask another DEVFORGE-related question."
    )

    return state

# -----------------------------
# Conditional Routing
# -----------------------------
def route(state: AgentState):

    if state["is_faq"]:
        return "faq"

    if state["is_related"]:
        return "ai_support"

    return "safe_response"


# -----------------------------
# Build Graph
# -----------------------------
builder = StateGraph(AgentState)

builder.add_node("classifier", classify_question)
builder.add_node("faq", faq_node)
builder.add_node("ai_support", ai_support)
builder.add_node("safe_response", safe_response)
builder.add_node("formatter", format_response)

builder.set_entry_point("classifier")


builder.add_conditional_edges(
    "classifier",
    route,
    {
        "faq": "formatter",
        "ai_support": "ai_support",
        "safe_response": "safe_response",
    },
)

builder.add_edge("ai_support", "formatter")
builder.add_edge("safe_response", "formatter")
builder.add_edge("formatter", END)

graph = builder.compile()


# -----------------------------
# Function used by FastAPI
# -----------------------------
conversation_history = []

def run_agent(message: str):
    global conversation_history

    result = graph.invoke(
        {
            "message": message,
            "response": "",
            "is_related": False,
            "is_faq": False,
            "history": conversation_history,
            
        }
    )

    conversation_history = result["history"]

    return result["response"]