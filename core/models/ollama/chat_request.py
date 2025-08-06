from dataclasses import dataclass
from typing import List
from core.models.ollama.message import Message


@dataclass
class ChatRequest:
    model: str
    messages: List[Message]
    stream: bool = False
