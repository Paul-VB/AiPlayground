from dataclasses import dataclass

@dataclass
class Property:
    type: str
    description: str

@dataclass
class Parameters:
	properties: dict[str, Property]
	required: list[str]
	type: str = "object"

@dataclass
class Function:
	name: str
	description: str
	parameters: Parameters

@dataclass
class Tool:
	type: str
	function: Function
