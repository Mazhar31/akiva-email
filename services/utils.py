from app import ChatBotRequest, process_user_input, json

async def get_response(session_id, message):
    chatbot_request = ChatBotRequest(
        session_id=session_id,
        message=message,
        modality="Chatbot"
    )
    response = await process_user_input(chatbot_request)
    response_content = response.body  # Get the raw response body
    decoded_response = response_content.decode()  # Decode the response bytes
    parsed_response = json.loads(decoded_response)  # Parse the JSON string
    bot_message = parsed_response["response"]["Text"]
    return bot_message