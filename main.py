from core.services import ollama_service


def main():
    chat_session()
    
def chat_session():
	#while user input is not "Exit"
	chat_messages = []
	while True:
		user_input = input("You: ")
		if user_input.lower() == "exit":
			break
		chat_request = ollama_service.build_chat_request(user_input)
		chat_messages.append(chat_request.messages[0])
		chat_request.messages = chat_messages
		response = ollama_service.get_chat_response(chat_request)
		chat_messages.append(response.message)
		response_text = parse_chat_response(response)
		print(f"Bot: {response_text}")

	# Placeholder for chat session logic
	pass

def parse_chat_response(chat_response):
	#get the messages f
	message = chat_response.message.content
	return message
	pass

if __name__ == "__main__":
	main()
