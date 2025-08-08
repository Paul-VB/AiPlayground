from core.models.ollama.tool_definition import ToolDefinition, ToolParameter
from core.services import vector_db_service

# Declare each tool in its own function

def get_weather_tool():
	def handler(location, unit):
		return f"Weather in {location} is 22°{unit[0].upper()}"
	return ToolDefinition(
		name="get_weather",
		description="Get current weather for a location",
		parameters={
			"location": ToolParameter("string", "City name"),
			"unit": ToolParameter("string", "Temperature unit", enum=["celsius", "fahrenheit"]),
		},
		handler=handler,
	)

def get_pauls_2016_history_report_tool():
	def handler(query):
		return vector_db_service.query_against_resource(query, "pauls 2016 history report")
	return ToolDefinition(
		name="pauls_2016_history_report",
		description="get inormation related to Paul's 2016 history report",
		parameters={
			"query": ToolParameter("string", "Query to search in Paul's 2016 history report"),
		},
		handler=handler,
	)

# Add more tool functions here...

tools_that_exist = [
	get_weather_tool(),
	get_pauls_2016_history_report_tool(),
	# add more tool functions here...
]


def to_ollama_tool(tool_def):
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

def execute_tool(tool_call):
	# Find the tool definition by name
	correct_tool_def = None
	for tool_def in tools_that_exist:
		if tool_def.name == tool_call.function.name:
			correct_tool_def = tool_def
			break

	#call the tool
	tool_call_result = correct_tool_def.handler(**tool_call.function.arguments)
	return tool_call_result
