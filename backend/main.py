from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import ollama
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    model: str = "llama3.1:8b"

@app.post("/chat")
async def chat(request: ChatRequest):
    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    def stream():
        for chunk in ollama.chat(
            model=request.model,
            messages=messages,
            stream=True
        ):
            content = chunk["message"]["content"]
            yield f"data: {json.dumps({'content': content})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/models")
async def list_models():
    result = ollama.list()
    names = [m.model for m in result.models]
    return {"models": names}


LAMP_COUNT = 12

lamp_tool = {
    "type": "function",
    "function": {
        "name": "set_lamps",
        "description": "Set the on/off state for each lamp",
        "parameters": {
            "type": "object",
            "properties": {
                "states": {
                    "type": "array",
                    "items": {"type": "integer", "enum": [0, 1]},
                    "description": f"Array of {LAMP_COUNT} values (0=off, 1=on), indexed from lamp 1 to {LAMP_COUNT}"
                }
            },
            "required": ["states"]
        }
    }
}

class LampRequest(BaseModel):
    message: str
    model: str = "llama3.1:8b"  # add this field

@app.post("/smart-home/lamps")
async def control_lamps(req: LampRequest):

    response = ollama.chat(
        model=req.model,
        messages=[
            {
                "role": "system",
                "content": f"You control {LAMP_COUNT} lamps numbered 1 to {LAMP_COUNT}. Always call set_lamps tool."
            },
            {"role": "user", "content": req.message}
        ],
        tools=[lamp_tool]
    )

    msg = response["message"]

    if msg.get("tool_calls"):
        args = msg["tool_calls"][0]["function"]["arguments"]
        states = args if isinstance(args, dict) else json.loads(args)
        return {"states": states["states"]}

    # fallback: model didn't call the tool
    return {"states": [0] * LAMP_COUNT, "error": "Model did not call tool"}


