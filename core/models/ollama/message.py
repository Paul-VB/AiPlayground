from dataclasses import dataclass, field
from core.models.ollama.tool_call import ToolCall

@dataclass
class Message:
	role: str
	content: str
	tool_calls: list[ToolCall] = field(default_factory=list)