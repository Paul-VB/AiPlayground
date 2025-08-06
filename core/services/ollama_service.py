import requests
from dataclasses import asdict
from core.models.ollama.chat_request import ChatRequest
from core.models.ollama.message import Message

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
OLLAMA_CHAT_MODEL = "gemma3"


def chat(chat_request: ChatRequest):
    response = requests.post(OLLAMA_CHAT_URL, json=asdict(chat_request))
    if not response.ok:
        raise ValueError(f"Error from Ollama: {response.status_code}")

    return response.json()["message"]["content"]


def build_chat_request(message: str, model=OLLAMA_CHAT_MODEL, stream=False):
    userMessage = Message(role="user", content=message)
    chat_request = ChatRequest(model=model, messages=[userMessage], stream=stream)
    return chat_request
