# chatbot-agent-lab

A full-stack AI laboratory for practicing LLM chatbot development and agentic AI (tool calling).

## Stack

- **Frontend:** Angular 21.2.0, Tailwind CSS v4, RxJS/Signals
- **Backend:** FastAPI (Python)
- **AI:** Ollama (`llama3.1:8b`, `gemma3:12b`)

## Features

- 💬 **Chat** — Conversational interface with dynamic model switching
- 🏠 **Smart Home Agent** — Natural language lamp control via function calling

## Getting Started

### Prerequisites
- Node.js, Python 3.10+, [Ollama](https://ollama.ai) running locally

### Install & Run
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start

Or run both concurrently from the project root:

bash
npm install
npm run dev

## Project Structure


chatbot-agent-lab/
├── backend/        # FastAPI app
├── frontend/       # Angular app
└── README.md

## Routes

| Path | Description |
|------|-------------|
| `/chat` | LLM chat interface |
| `/lamps` | Smart home agent |


Adjust the `backend/` and `frontend/` folder names if yours differ.