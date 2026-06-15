from typing import List
from pydantic import BaseModel
from config import settings


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    model: str = settings.ollama_default_model


class LampStateRequest(BaseModel):
    message: str
    model: str = settings.ollama_default_model