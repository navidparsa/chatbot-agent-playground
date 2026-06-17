from unittest import FunctionTestCase

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import ollama
import json

from smart_home import lamp_system_prompt, extract_tool_call, all_off, build_lamp_tool, FUNCTIONS_DICTIONARY
from schemas import LampStateRequest, ChatRequest

from config import settings
app = FastAPI(
    title="AI Chatbot Agent",
    version="0.1.0",
    description="FastAPI backend with configurable Ollama"
)

# ========================= MIDDLEWARE =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================= OLLAMA CLIENT =========================

ollama_client = ollama.Client(host=settings.ollama_host)


# ========================= HELPERS =========================
def format_stream_chunk(content: str) -> str:
    return f"data: {json.dumps({'content': content})}\n\n"


# ========================= ENDPOINTS =========================
@app.post("/chat")
async def chat(request: ChatRequest):
    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    def stream():
        try:
            for chunk in ollama_client.chat(
                model=request.model,
                messages=messages,
                stream=True,
            ):
                yield format_stream_chunk(chunk["message"]["content"])
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.get("/models")
async def list_models():
    try:
        result = ollama_client.list()
        return {"models": [m.model for m in result.models]}
    except Exception as e:
        return {"models": [], "error": str(e)}


@app.post("/smart-home/control-lamp-state")
async def control_lamps(req: LampStateRequest):
    try:
        response = ollama_client.chat(
            model=req.model,
            messages=[
                {"role": "system", "content": lamp_system_prompt()},
                {"role": "user", "content": req.message},
            ],
            tools=[build_lamp_tool()],
        )
        func_name, args = extract_tool_call(response["message"])
        func = FUNCTIONS_DICTIONARY.get(func_name)
        states = func(**args)
        if states is None:
            return {"states": all_off(), "error": "Model did not call the tool"}
        return {"states": states}
    except Exception as e:
        return {"states": all_off(), "error": f"Failed to control lamps: {e}"}
