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
def send_greetings_to_recipients(recipient_emails, sent_emails):
    with multiprocessing.Pool() as pool:
        pool.starmap(send_greeting_email, [(email, sent_emails) for email in recipient_emails])

# Function to get the latest email body and filter by the last 30 minutes in local time
def get_unread_emails(sent_emails):
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
                                    emails_data.append((from_, subject, body))
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode()
                            emails_data.append((from_, subject, body))
                        
                        print(f"Processing email from {sender_email} sent at {msg_datetime}")

        mail.close()
        mail.logout()

        return emails_data

    except Exception as e:
        print(f"Failed to receive email: {e}")
        return []

# Function to send email via SMTP
def send_email(subject, body, to_email):
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


def get_backend_response(email_body):
    # Prepare the request data
    print("In get_backend_response with email_body", email_body)
    request_data = {
        "session_id": "8ff6d888-bbfc-4948-a103-30b440908cc8",
        "message": email_body,
        "modality": "Chatbot"
    }

    # Use a synchronous client
    with httpx.Client(timeout=None) as client:
        # Make the POST request to the chatbot endpoint
        response = client.post("http://localhost:8000/chatbot/", json=request_data)

        print("Response from get_backend_response", response)
        
        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            print("Print response_data[response][Text]", response_data["response"]["Text"])
            return response_data["response"]["Text"]
        else:
            raise Exception(f"Error from backend: {response.status_code} - {response.text}")




# Function to process a single email
def process_email(email_data):
    from_email, subject, email_body = email_data
    print(f"Processing email from: {from_email}")
    print(f"Subject: {subject}")
    print(f"Body: {email_body}")

    # Get GPT's response to the email
    gpt_response = get_backend_response(email_body)



    send_email(f"Re: {subject}", gpt_response, from_email)


def email_chat(email):
    with multiprocessing.Manager() as manager:
        sent_emails = manager.list()

        # Step 1: Send an initial greeting to a list of users
        recipient_emails = email  # Add more emails as needed
        send_greetings_to_recipients(recipient_emails, sent_emails)

        # Step 2: Begin the chat loop
        while True:
            print("Checking for new emails...")

            # Get all unread emails from the tracked senders within the last 3 minutes
            unread_emails = get_unread_emails(sent_emails)

            if unread_emails:
                # Process emails in parallel
                with multiprocessing.Pool() as pool:
                    pool.map(process_email, unread_emails)

            # Delay to avoid overloading the server with frequent checks
            time.sleep(10)

# Run the email chat system
if __name__ == "__main__":
    multiprocessing.freeze_support()  # Add this line for Windows compatibility
    email_chat(["mazharshafiq96@gmail.com"])
