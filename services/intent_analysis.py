from astrapy import DataAPIClient
from dotenv import load_dotenv
import os

load_dotenv()
# Initialize the Astra DB client
token = os.getenv("datastax_client_API")
client = DataAPIClient(token)
url = os.getenv("DB_endpoint")
db = client.get_database_by_api_endpoint(url)



# Collections for session and chat history
intent_collection = db.get_collection("chat_intent")


def add_intent_id(session_id, intent_id):
    existing_session = intent_collection.find_one({"session_id": session_id})
    
    if existing_session:
        # If the session_id exists, update the intent_id
        intent_collection.update_one(
            {"session_id": session_id},
            {"$set": {"intent_id": intent_id}}
        )
    else:
        # If the session_id does not exist, insert a new document
        data_to_insert = {
            "session_id": session_id,
            "intent_id": intent_id
        }
        intent_collection.insert_one(data_to_insert)


def get_intent_id_for_session(session_id):
    session = intent_collection.find_one({"session_id": session_id})
    intent_id = session['intent_id']
    return intent_id
