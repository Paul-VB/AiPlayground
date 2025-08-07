import requests
from dataclasses import asdict
from dacite import from_dict, Config
from core.models.ollama.chat_request import ChatRequest
from core.models.ollama.chat_response import ChatResponse
from core.models.ollama.message import Message
from core.services import tool_service

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
OLLAMA_CHAT_MODEL = "llama3.1:8b"

def chat(chat_request: ChatRequest) -> ChatResponse:
	_inject_tools(chat_request)
	initial_response = _get_chat_response(chat_request)
	# if initial_response.tool_calls is empty, then we dont need to call tools and we can just return the message content
	if not initial_response.message.tool_calls:
		chat_request.tools = []
		tooless_response = _get_chat_response(chat_request)
		return tooless_response

	#for testing, i just wanna see the tool calls
	print("Tool calls to execute:") 
	for tool_call in initial_response.message.tool_calls:
		print(f"Tool name: {tool_call.function.name}")
		print(f"Arguments: {tool_call.function.arguments}")
		print("---")
	# You can add actual execution logic here later


def build_chat_request(message: str, model=OLLAMA_CHAT_MODEL, stream=False) -> ChatRequest:
	userMessage = Message(role="user", content=message)
	chat_request = ChatRequest(model=model, messages=[userMessage], stream=stream)
	return chat_request

def _inject_tools(chat_request: ChatRequest):
	for tool in tool_service.tools_that_exist:	
		ollama_tool = tool_service.to_ollama_tool(tool)
		chat_request.tools.append(ollama_tool)

def _get_chat_response(chat_request: ChatRequest) -> ChatResponse:
	http_response = requests.post(OLLAMA_CHAT_URL, json=asdict(chat_request))
	if not http_response.ok:
		raise ValueError(f"Error from Ollama: {http_response.status_code}")
	chatResponse = from_dict(data_class=ChatResponse, data=http_response.json(), config=Config(strict=False))
	return chatResponse

