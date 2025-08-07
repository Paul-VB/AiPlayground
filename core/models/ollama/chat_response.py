from dataclasses import dataclass
from core.models.ollama.message import Message


@dataclass
class ChatResponse:
    model: str
    created_at: str
    message: Message
    done: bool
