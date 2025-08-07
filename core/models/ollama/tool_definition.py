from dataclasses import dataclass
from typing import Callable

@dataclass
class ToolParameter:
	type: str
	description: str
	required: bool = False
	enum: list[any] = None  #optional if you want to restrict to specific values

@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, ToolParameter]
    handler: Callable

