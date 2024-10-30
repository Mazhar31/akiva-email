import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
from email.header import decode_header
import os
from dotenv import load_dotenv

load_dotenv()

# Your OpenAI API key (no need to set it again here unless it's used elsewhere)
# Global Variables for email access
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
EMAIL_USER = "hamzasuleman975@gmail.com"
EMAIL_PASS = "kctr cxgj gbaj jblg"

# Function to send an initial greeting email (converted to async)
async def send_greeting_email(to_email, message):
    subject = "AI Kelly!"
    body = message
    
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
        return True

    except Exception as e:
        print(f"Failed to send greeting email: {e}")
        return False
