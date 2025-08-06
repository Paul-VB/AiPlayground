from dataclasses import dataclass
from datetime import datetime
from core.models.ollama.message import Message


@dataclass
class ChatResponse:
    model: str
    created_at: datetime
    message: Message
    done: bool
