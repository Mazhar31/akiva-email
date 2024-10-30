import openai
from . import constants
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
General_QA_Collection = db.get_collection("general_qa")
Objection_QA_Collection = db.get_collection("objection_qa")
Retainer_QA_Collection = db.get_collection("retainer_qa")

openai.api_key =os.getenv("openai_api")

General_QA_dict = {}
Objection_QA_dict = {}
Retainer_QA_dict = {}

def get_general_qa():
    # Fetch all documents from the 'general_qa' collection
    all_documents = General_QA_Collection.find()
    for doc in all_documents:
        ga_key = doc["GA"]
        General_QA_dict[ga_key] = [doc["Question"], doc["Answer"]]


def get_objection_qa():
    # Fetch all documents from the 'objection_qa' collection
    all_documents = Objection_QA_Collection.find()
    for doc in all_documents:
        ga_key = doc["GA"]
        Objection_QA_dict[ga_key] = [doc["Question"], doc["Answer"]]


def get_retainer_qa():
    # Fetch all documents from the 'retainer_qa' collection
    all_documents = Retainer_QA_Collection.find()
    for doc in all_documents:
        ga_key = doc["GA"]
        Retainer_QA_dict[ga_key] = [doc["Question"], doc["Answer"]]


def intent_analysis_with_GPT(input, system_prompt):
    print("In start")
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": f"User message: {input}"}],
        max_tokens=300,
        temperature=0.1
    )

    # Add the bot's response to the chat history
    bot_response = response.choices[0].message.content
    if bot_response.startswith("'") and bot_response.endswith("'"):
        # Remove the first and last character (the single quotes)
        bot_response = bot_response[1:-1]
    print("returning response")
    return bot_response


# Inner intent analysis for General QA
def find_intent_for_GA(inner_intent, modality, first_name):
    # Check for the modality and construct the response accordingly 
    response = ''
    if inner_intent == "Other":
        response = "Other"

    else:
        response = General_QA_dict[inner_intent][1].replace("{first_name}", first_name)

    return response, inner_intent

def inner_intent_analysis_General_QA(input, modality, first_name):
    get_general_qa()
    # Initialize the base system prompt
    system_prompt = f"You are an assistant designed to classify user questions into one categories related to estate planning. Your task is to analyze the user's question and return the most relevant category code GA# based on the meaning of the question, even if it is phrased differently. Match the user’s question to the closest category based on the core intent behind the question. If the question does not match any of the provided categories, return 'Other'.Here is the list of categories:"

    # Loop through the General_QA_dict and append the categories and example questions to the prompt
    for key, value in General_QA_dict.items():
        question = value[0]  # The first element is the question
        system_prompt += f"If the user’s question is '{question}' or any question that expresses the same core intent, return '{key}'\n"
    
    system_prompt += "If no match is found, return 'Other'."

    
    bot_response = intent_analysis_with_GPT(input, system_prompt)
    
    response, inner_intent = find_intent_for_GA(bot_response, modality, first_name)
    
    return response, inner_intent


# Inner intent analysis for Retainer QA
def find_intent_for_RA(inner_intent, modality, first_name):
    response = ''
    if inner_intent == "Other":
        response = "Other"
    else:
        PROMPT = Retainer_QA_dict[inner_intent][1].replace("{first_name}", first_name)
        response = PROMPT

    return response, inner_intent

def inner_intent_analysis_retainer_QA(input, modality, first_name):
    get_retainer_qa()
    # Initialize the base system prompt
    system_prompt = f"You are an assistant designed to classify user questions into one categories related to estate planning. Your task is to analyze the user's question and return the most relevant category code GA# based on the meaning of the question, even if it is phrased differently. Match the user’s question to the closest category based on the core intent behind the question. If the question does not match any of the provided categories, return 'Other'.Here is the list of categories:"

    # Loop through the General_QA_dict and append the categories and example questions to the prompt
    for key, value in Retainer_QA_dict.items():
        question = value[0]  # The first element is the question
        system_prompt += f"If the user’s question is '{question}' or any question that expresses the same core intent, return '{key}'\n"
    
    system_prompt += "If no match is found, return 'Other'."
    
    bot_response = intent_analysis_with_GPT(input, system_prompt)

    response, inner_intent = find_intent_for_RA(bot_response, modality, first_name)
    return response, inner_intent


# Inner intent analysis for Objection QA
def find_intent_for_OA(inner_intent, modality, first_name):
    PROMPT = Objection_QA_dict[inner_intent][1].replace("{first_name}", first_name)
    if inner_intent == "Other":
        response = "Other"

    else:
        response = PROMPT

    return response, inner_intent

def inner_intent_analysis_objection_QA(input, modality, first_name):
    get_objection_qa()
    # Initialize the base system prompt
    system_prompt = f"You are an assistant designed to classify user questions into one categories related to estate planning. Your task is to analyze the user's question and return the most relevant category code GA# based on the meaning of the question, even if it is phrased differently. Match the user’s question to the closest category based on the core intent behind the question. If the question does not match any of the provided categories, return 'Other'.Here is the list of categories:"

    # Loop through the General_QA_dict and append the categories and example questions to the prompt
    for key, value in Objection_QA_dict.items():
        question = value[0]  # The first element is the question
        system_prompt += f"If the user’s question is '{question}' or any question that expresses the same core intent, return '{key}'\n"
    
    system_prompt += "If no match is found, return 'Other'."

    bot_response = intent_analysis_with_GPT(input, system_prompt)
    response, inner_intent = find_intent_for_OA(bot_response, modality, first_name)
    return response, inner_intent



def handle_greetings(message):
    prompt = constants.CR_GREETING_INNER_INTENT_PROMPT
    response = ''
    analysis = intent_analysis_with_GPT(message, prompt)
    
    if analysis == "Salutation":
        # call gpt
        response = constants.CR_GREETING_SALUTATION, constants.CR_GREETING_SALUTATION_AF_URL, constants.CR_GREETING_SALUTATION_VF_URL
    
    elif analysis == "Polite Concern":
        # call gpt
        response = constants.CR_GREETING_POLITE_CONCERN, constants.CR_GREETING_POLITE_CONCERN_AF_URL, constants.CR_GREETING_POLITE_CONCERN_VF_URL
    
    elif analysis == "Prior Question":
        # hard codede message
        response = constants.CR_GREETING_PRIOR_QUESTION, constants.CR_GREETING_PRIOR_QUESTION_AF_URL, constants.CR_GREETING_PRIOR_QUESTION_VF_URL

    elif analysis == "Asking for Name":
        # hard coded message
        response = constants.CR_GREETING_ASKING_NAME, constants.CR_GREETING_ASKING_NAME_AF_URL, constants.CR_GREETING_ASKING_NAME_VF_URL
    
    elif analysis == "Other":
        # hard coded message
        response = constants.CR_OTHER_START, constants.CR_OTHER_START_AF_URL, constants.CR_OTHER_START_VF_URL
    
    return response
