from core.services import ollama_service


def main():
    chat_session()
    
def chat_session():
	#while user input is not "Exit"
	while True:
		user_input = input("You: ")
		if user_input.lower() == "exit":
			break
		chat_request = ollama_service.build_chat_request(user_input)
		response = ollama_service.get_chat_response(chat_request)
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
