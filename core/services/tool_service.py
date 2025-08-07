from core.models.ollama import tool
from core.models.ollama.tool_definition import ToolDefinition, ToolParameter

# Declare each tool in its own function

def get_weather_tool():
	def handler(location, unit):
		return f"Weather in {location} is 22°{unit[0].upper()}"
	return ToolDefinition(
		name="get_weather",
		description="Get current weather for a location",
		parameters={
			"location": ToolParameter("string", "City name"),
			"unit": ToolParameter("string", "Temperature unit (celsius or fahrenheit)"),
		},
		handler=handler,
	)

# Add more tool functions here...

tools_that_exist = [
	get_weather_tool(),
	# add more tool functions here...
]


def to_ollama_tool(tool_def: ToolDefinition) -> tool:
	thereAreAnyRequriedParams = any(param.required for param in tool_def.parameters.values())
    
	ollama_tool = {
		"type": "function",
		"function": {
			"name": tool_def.name,
			"description": tool_def.description,
			"parameters": {
				"type": "object",
				"properties": {
					name: {
						"type": parameter.type,
						"description": parameter.description,
      					**({"enum": parameter.enum} if parameter.enum else {})
					} for name, parameter in tool_def.parameters.items()
				},
    			**({"required": [name for name, param in tool_def.parameters.items() if param.required]} if thereAreAnyRequriedParams else {}),
			},
		},
	}
	return ollama_tool