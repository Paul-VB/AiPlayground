from dataclasses import dataclass, field
from core.models.ollama.message import Message
from core.models.ollama.tool import Tool


@dataclass
class ChatRequest:
    model: str
    messages: list[Message]
    stream: bool = False
    tools: list[Tool] = field(default_factory=list)
