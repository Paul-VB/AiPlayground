from dataclasses import dataclass

@dataclass
class Function:
    name: str
    arguments: dict

@dataclass
class ToolCall:
    function: Function