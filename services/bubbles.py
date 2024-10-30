from astrapy import DataAPIClient

from dotenv import load_dotenv
import os

load_dotenv()
# Initialize the Astra DB client
token = os.getenv("datastax_client_API")
client = DataAPIClient(token)
url = os.getenv("DB_endpoint")
db = client.get_database_by_api_endpoint(url)


# Initialize the collection
General_QA_Collection = db.get_collection("general_qa")
Objection_QA_Collection = db.get_collection("objection_qa")
Retainer_QA_Collection = db.get_collection("retainer_qa")


# Fetch all documents from the 'general_qa' collection
all_documents = General_QA_Collection.find()
General_QA_URL_Dict = {}
for doc in all_documents:
    ga_key = doc["GA"]
    General_QA_URL_Dict[ga_key] = doc["URL"]


# Fetch all documents from the 'objection_qa' collection
all_documents = Objection_QA_Collection.find()
Objection_QA_URL_Dict = {}
for doc in all_documents:
    ga_key = doc["GA"]
    Objection_QA_URL_Dict[ga_key] = doc["URL"]


# Fetch all documents from the 'objection_qa' collection
all_documents = Retainer_QA_Collection.find()
Retainer_QA_URL_Dict = {}
for doc in all_documents:
    ga_key = doc["GA"]
    Retainer_QA_URL_Dict[ga_key] = doc["URL"]



intent_section_1_bubbles = {
    "1": "I'm ready to make a purchase",  
}

intent_section_2_bubbles = {
    "1": "Revocable Living Trust Package",
    "2": "Irrevocable Living Trust Package"
}

intent_section_3_bubbles = {}

intent_section_4_bubbles = {}

intent_section_5_bubbles = {}

payment_bubbles = {
    "1": "Full Payment",
    "2": "2 Installments",
    "3": "3 Installments"
}

intent_section_7_bubbles = {}



def find_bubbles_value(user_input, dict):
    if user_input in dict:  # Check if key exists in the provided dictionary
        return dict[user_input]  # Return the value associated with key
    else:
        return None


# Function to check for bubbles
def check_bubbles(bubble_dict):
    if bubble_dict:  # Checks if the dictionary is not empty
        return True
    else:
        return False