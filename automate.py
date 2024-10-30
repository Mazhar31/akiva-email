import os
import pandas as pd
import csv
from services.inner_intents import General_QA_dict, Retainer_QA_dict, Objection_QA_dict
from update_QA_Dict import Flow_QA_dict
from services.test import chat_flow_for_intent_section_1, chat_flow_for_intent_section_2, chat_flow_for_intent_section_4 
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from astrapy import DataAPIClient
import json

load_dotenv()
# Initialize the Astra DB client
token = os.getenv("datastax_client_API")
client = DataAPIClient(token)
url = os.getenv("DB_endpoint")
db = client.get_database_by_api_endpoint(url)

# Collections for session and chat history
intent_collection = db.get_collection("chat_intent")
session_collection = db.get_collection("session")
chat_history_collection = db.get_collection("user_data_and_chat_history")
complete_history_collection = db.get_collection("complete_history")
user_choices_collection = db.get_collection("user_choices")
initiate_ai_collection = db.get_collection("initiate_ai")
next_needed_collection = db.get_collection("next_needed")



SESSION_ID = 'fe178d50-a109-4104-8a12-6250c351714b'
FIRST_NAME = 'string4'
MODALITY = 'Chatbot'


def get_intent_id_for_session(session_id):
    session = intent_collection.find_one({"session_id": session_id})
    intent_id = session['intent_id']
    return intent_id


def process_user_input(message, chat_history, first_name, session_id, modality):
    # Check if the session ID exists in the session collection
    session_exists = session_collection.find_one({"session_id": session_id})
    if not session_exists:
        raise Exception(status_code=404, detail="Session does not exist or invalid session ID")
    
    current_time = datetime.utcnow()
    expiration_time = current_time - timedelta(hours=24)
    
    session_data = chat_history_collection.find_one({"session_id": session_id, "is_active": True})
    if not session_data or session_data.get("last_updated") <= expiration_time:
        raise Exception(status_code=404, detail="Session expired or not found")

    intent = get_intent_id_for_session(session_id)
    if intent == '1':
        response = chat_flow_for_intent_section_1(message, chat_history, first_name, session_id, modality)
    elif intent == '2':
        response = chat_flow_for_intent_section_2(message, chat_history, first_name, session_id, modality)
    # elif intent == '3':
    #     bot_response = chat_flow_for_intent_section_3(message, chat_history, first_name, session_id, modality)
    elif intent == '4':
        response = chat_flow_for_intent_section_4(message, chat_history, first_name, session_id, modality)
    
    #print("\n\n\nresponse : ", response)
    if response:
        # response_content = response.body  # Get the raw response body
        # decoded_response = response_content.decode()  # Decode the response bytes
        # parsed_response = json.loads(decoded_response)  # Parse the JSON string
        # bot_response = parsed_response["response"]["Text"]
        return response

    return "AI not responding"



if not os.path.exists('./mismatches'):
    os.makedirs('./mismatches')


questions_df = pd.read_csv('./question.csv', encoding='ISO-8859-1')


#print("Columns in the DataFrame:", questions_df.columns.tolist())


with open('./mismatched_results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Index", "Version", "Sequence Number", "Question", "Expected Answer", "Chatbot Response"])


    for index, row in questions_df.iterrows():
        question_version = row['Suggested Question'] 
        sequence = row['Sequence Number']  
        index_name = row['Index'] 

        
        if index_name.startswith('GA'):
            expected_answer = General_QA_dict.get(index_name, ["", ""])[1]
        elif index_name.startswith('RA'):
            expected_answer = Retainer_QA_dict.get(index_name, ["", ""])[1]
        elif index_name.startswith('OA'):
            expected_answer = Objection_QA_dict.get(index_name, ["", ""])[1]
        elif index_name.startswith('FA'):
            expected_answer = Flow_QA_dict.get(index_name, ["", ""])[1]
        else:
            print(f"No matching dictionary for index: {index_name}")
            continue  

        #print(f"Expected answer for {question_version}: {expected_answer}")

        
        chatbot_response = process_user_input(question_version, "", FIRST_NAME, SESSION_ID, MODALITY)

        
        if chatbot_response is None:
            print(f"No response for question: {question_version}.")  
            continue  

        
        chatbot_response_text = chatbot_response['Text'].strip()

        # additional_text = f"I hope I’ve answered your question, {FIRST_NAME}. Please let me know if you are ready to purchase one of our Living Trust Packages. Let me know, {FIRST_NAME}, if you have any additional questions."
        # if additional_text in chatbot_response_text:
        #     chatbot_response_text = chatbot_response_text.replace(additional_text, '').strip()

        # print(f"Chatbot response for {question_version}: {chatbot_response_text}") 

       
        # if chatbot_response_text.lower() != expected_answer.lower().strip():
        #     print(f"Mismatch found for question: {question_version}")
           
        #     writer.writerow([index_name, question_version, sequence, question_version, expected_answer, chatbot_response_text])
        
        if expected_answer in chatbot_response_text or expected_answer == chatbot_response_text:
            print("\nGot the match")        
        
        elif expected_answer not in chatbot_response_text or expected_answer != chatbot_response_text:
            print(f"Mismatch found for question: {question_version}")
            writer.writerow([index_name, question_version, sequence, question_version, expected_answer, chatbot_response_text])
        
        


print("Mismatched responses have been logged in 'mismatched_results.csv'.")
