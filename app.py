from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
# from typing import Any, Dict, Optional
from pydantic import BaseModel
from services.test import chat_flow_for_intent_section_1, chat_flow_for_intent_section_2, chat_flow_for_intent_section_4
import uuid
import json
from datetime import datetime, timedelta
from astrapy import DataAPIClient
from services.intent_analysis import add_intent_id, get_intent_id_for_session
from services.bubbles import intent_section_1_bubbles
from services import constants
import openai
import os
from fastapi.middleware.cors import CORSMiddleware
import importlib
from fastapi import Request
# from twilio.rest import Client
from email_test import email_chat

import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import openai
import time
import os
import httpx
import asyncio
from dotenv import load_dotenv
import multiprocessing
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from concurrent.futures import ThreadPoolExecutor


app = FastAPI()
openai.api_key =os.getenv("openai_api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from dotenv import load_dotenv
import os

load_dotenv()
# Initialize the Astra DB client
token = os.getenv("datastax_client_API")
print("tokan: ",token)
client = DataAPIClient(token)
url = os.getenv("DB_endpoint")
db = client.get_database_by_api_endpoint(url)

# Collections for session and chat history
session_collection = db.get_collection("session")
chat_history_collection = db.get_collection("user_data_and_chat_history")
complete_history_collection = db.get_collection("complete_history")
user_choices_collection = db.get_collection("user_choices")
initiate_ai_collection = db.get_collection("initiate_ai")
next_needed_collection = db.get_collection("next_needed")


# Define the request models
class StartSessionRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str

class ChatBotRequest(BaseModel):
    session_id: str
    message: str
    modality: str # It can be 'Avatar' or 'Chatbot' or 'SMS' or 'Voice' or 'Whatsapp' or 'Email'

class NewChatBotRequest(BaseModel):
    smsBody: str
    firstName: str
    lastName: str
    email: str
    phone: str
    sessionId: str
    modality: str

class EmailMessageRequest(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    emailBody: str
    sessionId: str
    modality: str

class Initiate_request(BaseModel):
    sessionId: str
    modality: str

class Email_request(BaseModel):
    session_id: str
    message: str
    modality: str # It can be 'Avatar' or 'Chatbot' or 'SMS' or 'Voice' or 'Whatsapp' or 'Email'

class Reply_Email_request(BaseModel):
    email_body: str
    email_id: str # It can be 'Avatar' or 'Chatbot' or 'SMS' or 'Voice' or 'Whatsapp' or 'Email'


@app.post("/start-session/")
async def start_session(request: StartSessionRequest):
    importlib.reload(constants)

    existing_document = chat_history_collection.find_one({"email": request.email})
    
    current_time = datetime.utcnow()
    expiration_time = current_time - timedelta(hours=24)
    chat_history = []

    if existing_document and existing_document.get("last_updated") > expiration_time:
        session_id = existing_document["session_id"]
        initiate_ai_collection.insert_one(
        {
            "session_id": session_id,
            "Initiate": 'True',
            "User_Type": 'Returning'
        }
    )

    else:
        session_id = str(uuid.uuid4())
        initiate_ai_collection.insert_one(
            {
                "session_id": session_id,
                "Initiate": 'True',
                "User_Type": 'New'
            }
        )
        next_needed_collection.insert_one(
            {
                "session_id" : session_id,
                "next_needed": "Purchase"
            }
        )
        
        

    # if existing_document and existing_document.get("last_updated") > expiration_time:
    #     session_id = existing_document["session_id"]
    #     chat_history = json.loads(existing_document.get("history", "[]"))
    #     bot_response = f"Hi {request.first_name}, welcome back! Are you ready to purchase one of our Living Trust Packages or do you have some questions first? B^ {' B^ '.join(f'{key}: {value}' for key, value in intent_section_1_bubbles.items())}"
    #     chat_history.append({"bot": bot_response})
    # else:
    #     session_id = str(uuid.uuid4())
    #     bot_response = f"Hi {request.first_name}, and welcome! I'm AI Kelly, your friendly New York estate law artificial intelligence agent. You can make your estate plan purchase through me and also ask me questions. Your chat history will be recorded to best serve you and for quality control purposes. Please note, I am not an attorney, so I can't give you legal advice, but I can provide lots of information from my training. Are you ready to purchase one of our Living Trust Packages, or do you have some questions first? B^ {''.join(f'{key}: {value}' for key, value in intent_section_1_bubbles.items())}"
    #     chat_history.append({"bot": bot_response})  # Start history with the bot's greeting
    

    # Save session ID to session collection
    session_collection.update_one(
        {"email": request.email},
        {"$set": {"session_id": session_id}},
        upsert=True
    )

    # Save or update chat history and user details in chat_history collection
    chat_history_collection.update_one(
        {"session_id": session_id},
        {
            "$set": {
                "first_name": request.first_name,
                "last_name": request.last_name,
                "email": request.email,
                "phone": request.phone,
                "history": json.dumps(chat_history),  # Save the history as a JSON string
                "last_updated": current_time,
                "is_active": True
            }
        },
        upsert=True
    )

    user_choices_collection.insert_one(
        {
            "session_id": session_id,
            "Trust_Package": None,
            "Payments": None
        }
    )

    add_intent_id(session_id, '1')

    return JSONResponse(content={"session_id": session_id})


# Utility function to summarize chat history
async def summarize_chat_history(chat_history: str) -> str:
    print("\n I am here\n")
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        #messages=[{"role": "system", "content": "Your are provided with a chat history your task is to summarize it as short as possible but you have to keep all the important messages you can summarize them too to make it more short but everything should make a proper sense and the name of the user should also remain in history and please keep the last 3 messages in history if they are not repeating or similar if you find last 3 messages repeating or similar than keep last 3 messages that are entirely different. Important! Just provide the summary not a single word more than that."},
        #          {"role": "user", "content": f"{chat_history}"}],
        messages=[{"role": "system", "content": "You are provided with a chat history. Your task is to summarize it as briefly as possible, keeping all important messages in a shortened form. Ensure everything makes sense and retains the user’s name. Keep the last 3 distinct messages if they are not repetitive. If the last 3 messages are similar or repetitive, retain the last 3 entirely different ones. Provide only the summary."},
                  {"role": "user", "content": f"{chat_history}"}],
        max_tokens=10000,
        temperature=0.3
    )
    # Add the bot's response to the chat history
    bot_response = response.choices[0].message.content
    
    return bot_response

# @app.post("/chatbot/")
async def process_user_input(request: ChatBotRequest):
    # Check if the session ID exists in the session collection
    session_exists = session_collection.find_one({"session_id": request.session_id})
    if not session_exists:
        raise HTTPException(status_code=404, detail="Session does not exist or invalid session ID")
    
    current_time = datetime.utcnow()
    expiration_time = current_time - timedelta(hours=24)
    
    session_data = chat_history_collection.find_one({"session_id": request.session_id, "is_active": True})
    if not session_data or session_data.get("last_updated") <= expiration_time:
        raise HTTPException(status_code=404, detail="Session expired or not found")

    # Load and update the chat history
    chat_history = json.loads(session_data.get("history", "[]"))
    chat_history.append({"user": request.message})
    
    # Retrieve user details
    first_name = session_data.get("first_name")
    last_name = session_data.get("last_name")
    email = session_data.get("email")

    # Check if chat history exceeds 12,000 characters
    full_chat_history_str = json.dumps(chat_history)
    print("\n\n Length : ",len(full_chat_history_str))
    if len(full_chat_history_str) > 5000:
        # Summarize the chat history using GPT
        summarized_chat_history = await summarize_chat_history(full_chat_history_str)
        
        # Store the complete chat history in the 'complete_history' collection
        complete_history_collection.update_one(
            {"session_id": request.session_id},
            {
                "$set": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "session_id": request.session_id,
                    "history": full_chat_history_str,  # Save the full history
                    "last_updated": current_time,
                }
            },
            upsert=True
        )

        # Replace the full history with summarized history in the main collection
        chat_history = [{"bot": summarized_chat_history}]


    intent = get_intent_id_for_session(request.session_id)
    if intent == '1':
        bot_response = chat_flow_for_intent_section_1(request.message, chat_history, first_name, request.session_id, request.modality)
    elif intent == '2':
        bot_response = chat_flow_for_intent_section_2(request.message, chat_history, first_name, request.session_id, request.modality)
    # elif intent == '3':
    #     bot_response = chat_flow_for_intent_section_3(request.message, chat_history, first_name, request.session_id, request.modality)
    elif intent == '4':
        bot_response = chat_flow_for_intent_section_4(request.message, chat_history, first_name, request.session_id, request.modality)

    if bot_response:
        chat_history.append({"bot": bot_response})

        # Serialize and save updated chat history
        chat_history_collection.update_one(
            {"session_id": request.session_id},
            {"$set": {"history": json.dumps(chat_history), "last_updated": current_time}}
        )

        return JSONResponse(content={"response": bot_response})
    else:
        raise HTTPException(status_code=403, detail="AI not Responding")


# @app.get("/chat-history/{session_id}")
# async def get_chat_history(session_id: str):
#     current_time = datetime.utcnow()
#     expiration_time = current_time - timedelta(hours=24)
    
#     session_data = chat_history_collection.find_one({"session_id": session_id, "is_active": True})
#     if not session_data or session_data.get("last_updated") <= expiration_time:
#         raise HTTPException(status_code=404, detail="Session expired or not found")

#     chat_history = json.loads(session_data["history"])
#     return JSONResponse(content={"history": chat_history})



@app.post("/email") 
async def email_reply(request: Email_request):
    # bot_message = await get_backend_response(request.session_id, request.message)
    session_data = chat_history_collection.find_one({"session_id": request.session_id, "is_active": True})
    email = session_data.get("email")
    print("email: ", email)

    check = await email_chat(request.session_id, [email])
    if check:
        JSONResponse(content={"status": "Message sent successfully!"})
    else:
        raise HTTPException(status_code=403, detail="AI not Responding")
    









load_dotenv()
# Your OpenAI API key
openai.api_key = os.getenv("openai_api")
# Global Variables for email access
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
EMAIL_USER = "hamzasuleman975@gmail.com"
EMAIL_PASS = "kctr cxgj gbaj jblg"

# Function to send an initial greeting email
def send_greeting_email(to_email, sent_emails):
    subject = "Welcome to the Email Chat!"
    body = "Hello! How can I assist you today? Please reply to this email to start the chat."
    
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach body to email
        msg.attach(MIMEText(body, 'plain'))

        # Set up the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)

        # Send the email
        text = msg.as_string()
        server.sendmail(EMAIL_USER, to_email, text)
        server.quit()
        print(f"Greeting email sent to {to_email}!")
        
        # Add recipient email to the list
        sent_emails.append(to_email)
        
    except Exception as e:
        print(f"Failed to send greeting email: {e}")

# Function to send greeting emails to a list of recipients
async def send_greetings_to_recipients(recipient_emails, sent_emails):
    # with multiprocessing.Pool() as pool:
    #     pool.starmap(send_greeting_email, [(email, sent_emails) for email in recipient_emails])

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        await asyncio.gather(
            *[loop.run_in_executor(executor, send_greeting_email, email, sent_emails) for email in recipient_emails]
        )

# Function to get the latest email body and filter by the last 30 minutes in local time
def get_unread_emails(session_id, sent_emails):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")
        
        status, messages = mail.search(None, 'UNSEEN')
        mail_ids = messages[0].split()

        if len(mail_ids) == 0:
            print("No unread emails.")
            return []

        emails_data = []
        now = datetime.now(timezone.utc)
        thirty_minutes_ago = now - timedelta(minutes=30)

        for email_id in reversed(mail_ids):  # Process newest emails first
            status, msg_data = mail.fetch(email_id, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    msg_date = msg.get("Date")
                    try:
                        msg_datetime = parsedate_to_datetime(msg_date)
                        if msg_datetime.tzinfo is None:
                            msg_datetime = msg_datetime.replace(tzinfo=timezone.utc)
                        else:
                            msg_datetime = msg_datetime.astimezone(timezone.utc)
                    except Exception as e:
                        print(f"Error parsing date for email: {e}")
                        continue

                    time_diff = now - msg_datetime

                    if time_diff > timedelta(minutes=30):
                        return emails_data  # Stop processing and return collected emails

                    from_ = msg.get("From")
                    sender_email = from_.split('<')[-1].split('>')[0]

                    if sender_email in sent_emails:
                        subject = msg.get("Subject")
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    emails_data.append((from_, subject, body, session_id))
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode()
                            emails_data.append((from_, subject, body, session_id))
                        
                        print(f"Processing email from {sender_email} sent at {msg_datetime}")

        mail.close()
        mail.logout()

        return emails_data

    except Exception as e:
        print(f"Failed to receive email: {e}")
        return []

# Function to send email via SMTP
def send_email(subject, body, to_email):
    print("In send_email > body, to_email", body, to_email)
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach body to email
        msg.attach(MIMEText(body, 'plain'))

        # Set up the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)

        print("Before msg.as_string")
        print("Printing msg: ", msg)
        # Send the email
        text = msg.as_string()
        print("after msg.as_string")
        server.sendmail(EMAIL_USER, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to get GPT response for the given email body
# def get_chatgpt_response(email_body):
#     response = openai.chat.completions.create(
#       model="gpt-3.5-turbo",
#       messages=[
#         {"role": "system", "content": "You are an email assistant."},
#         {"role": "user", "content": email_body}
#       ]
#     )
#     return response.choices[0].message.content


# async def get_backend_response(email_body):
#     # Prepare the request data
#     print("In get_backend_response with email_body", email_body)
#     request_data = {
#         "session_id": "8ff6d888-bbfc-4948-a103-30b440908cc8",
#         "message": email_body,
#         "modality": "Email"
#     }

#     async with httpx.AsyncClient() as client:
#         # Make the POST request to the chatbot endpoint
#         response = await client.post("http://localhost:8000/chatbot/", json=request_data)

#         print("Response from get_backend_response", response)
        
#         # Check if the response is successful
#         if response.status_code == 200:
#             response_data = response.json()
#             return response_data["response"]
#         else:
#             raise Exception(f"Error from backend: {response.status_code} - {response.text}")


# def get_backend_response(email_body):
#     # Prepare the request data
#     print("In get_backend_response with email_body", email_body)
#     request_data = {
#         "session_id": "8ff6d888-bbfc-4948-a103-30b440908cc8",
#         "message": email_body,
#         "modality": "Chatbot"
#     }

#     # Use a synchronous client
#     with httpx.Client(timeout=None) as client:
#         # Make the POST request to the chatbot endpoint
#         response = client.post("http://localhost:8000/chatbot/", json=request_data)

#         print("Response from get_backend_response", response)
        
#         # Check if the response is successful
#         if response.status_code == 200:
#             response_data = response.json()
#             print("Print response_data[response][Text]", response_data["response"]["Text"])
#             return response_data["response"]["Text"]
#         else:
#             raise Exception(f"Error from backend: {response.status_code} - {response.text}")




# Function to process a single email
async def process_email(email_data):
    from_email, subject, email_body, session_id = email_data
    print(f"Processing email from: {from_email}")
    print(f"Subject: {subject}")
    print(f"Body: {email_body}")

    print("email_data: ", email_data)

    chatbot_request = ChatBotRequest(
        session_id=session_id,
        message=email_body,
        modality="Chatbot"
    )

    # Get GPT's response to the email
    response =  asyncio.run(process_user_input(chatbot_request))
    response_content = response.body
    decoded_response = response_content.decode()
    parsed_response = json.loads(decoded_response)
    bot_message = parsed_response["response"]["Text"]



    send_email(f"Re: {subject}", bot_message, from_email)


async def email_chat(session_id, email):
    with multiprocessing.Manager() as manager:
        sent_emails = manager.list()

        # Step 1: Send an initial greeting to a list of users
        recipient_emails = email  # Add more emails as needed
        await send_greetings_to_recipients(recipient_emails, sent_emails)

        # Step 2: Begin the chat loop
        while True:
            print("Checking for new emails...")

            # Get all unread emails from the tracked senders within the last 3 minutes
            unread_emails = await get_unread_emails(session_id, sent_emails)

            if unread_emails:
                # Process emails in parallel
                # with multiprocessing.Pool() as pool:
                #     pool.map(process_email, unread_emails)
                with ThreadPoolExecutor() as executor:
                    loop = asyncio.get_event_loop()
                    await asyncio.gather(
                        *[loop.run_in_executor(executor, process_email, email) for email in unread_emails]
                )

            # Delay to avoid overloading the server with frequent checks
            # time.sleep(10)
            await asyncio.sleep(10)

# Run the email chat system
# if __name__ == "__main__":
#     multiprocessing.freeze_support()  # Add this line for Windows compatibility
#     email_chat(["mazharshafiq96@gmail.com"])




