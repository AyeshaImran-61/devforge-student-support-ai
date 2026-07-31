# DEVFORGE Student Support AI Agent

An AI-powered student support assistant built using FastAPI, LangGraph, LangChain, and Ollama Cloud.

---

## Features

- AI-powered student support
- LangGraph workflow
- Question classification
- Safe response for unrelated questions
- Ollama Cloud integration
- FastAPI REST API
- Interactive Swagger documentation

---

## Tech Stack

- Python
- FastAPI
- LangChain
- LangGraph
- Ollama Cloud
- OpenAI SDK (Ollama-compatible API)
- Uvicorn

---

## Project Structure

```
devforge-student-support-ai/
│
├── main.py
├── agent.py
├── requirements.txt
├── render.yaml
├── README.md
├── .env.example
├── .gitignore
└── .venv/
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/devforge-student-support-ai.git
```

Move into the project

```bash
cd devforge-student-support-ai
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

Example:

```env
OLLAMAAPIKEY=YOUR_API_KEY
OLLAMA_MODEL=gpt-oss:20b-cloud
```

---

## Run the Project

```bash
uvicorn main:app --reload
```

---

## API Endpoints

### GET /

Returns a welcome message.

### GET /health

Returns application health.

### POST /chat

Accepts a student question and returns the AI response.

### GET /docs

Swagger API documentation.

---

## LangGraph Workflow

```
User Question
      │
      ▼
Question Classification
      │
      ├──────────────┐
      ▼              ▼
AI Support      Safe Response
      │              │
      └──────┬───────┘
             ▼
        Final Response
```

---

## Security

- API keys stored in environment variables
- `.env` excluded from GitHub
- `.env.example` included for setup

---

## Deployment

Backend deployment target:

- Render Web Service

Environment Variables:

- OLLAMAAPIKEY
- OLLAMA_MODEL

Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Author

Ayesha Imran

University of Faisalabad

Bachelor of Artificial Intelligence

DEVFORGE Internship Project