from astrapy import DataAPIClient
import pandas as pd
from dotenv import load_dotenv

import os

load_dotenv()
# Initialize the Astra DB client
token = os.getenv("datastax_client_API")
client = DataAPIClient(token)
url = os.getenv("DB_endpoint")
db = client.get_database_by_api_endpoint(url)



variables_dict = {
    "CP_PREAMBLE": "You are a chatbot that classifies user intent into one of the following enumerated categories:",
    "CP_TASK": "Your task is to analyze the user's message and return only one of the following specific enumerated options:",
    
    "CP_GREETING": """
            Greeting: Given a user message, determine if it contains a polite or casual greeting such as 'hi,' 'hello,' 'hey,' 'good morning,' 'what's up," or similar, or if it expresses polite concern for health or well-being, such as 'How are you?' 'How's it going?' 'Hope you're doing well,' or similar phrases, or  if the user is asking whether they have already asked a question or made an inquiry, such as 'Did I already ask this?' or 'Have I asked this before?', or if the user is asking for their own name, such as 'What’s my name?' or 'Do you know my name?'
       """,
    "CP_GENERAL": """ 
            General: The user has not indicated an intent to purchase, and wants information related to our Trust Packages, 
            our product details, pricing, company information, your name, company name, company location, our privacy policy, payment options, use of artificial intelligence in our business, 
            estate planning in general, estate planning documents such as trust, will, 
            power of attorney, health care proxy, living will, 
            HIPAA authorization, probate, estate administration, small estates, testamentary substitutes, types of asset ownership, surrogate's court
            types of trusts, estate planning attorneys, mistakes to avoid in estate planning, lifetime gifting, benefits of estate planning, and the like.
       """,
    "CP_TRANSFER_TO_HUMAN": "Transfer To Human: If user is asking to talk to a human or requestion to connect with a real person or human.",
    "CP_OBJECTION": "Objection: The user is raising objections or concerns about their qualification, the need for an estate plan, the need for a trust, the making of a purchase, a clause in the Retainer Agreement, their choice of trust, pricing, or any other intent not to proceed.",
    "CP_OTHER": "Other: The user's message does not fit into any of the above categories.",
    
    "CR_OTHER_START": """
            I'm sorry {first_name}, as an AI, I'm only trained on very specific tasks. That is not a request I recognize. I will log the request so that a human can review and see if we should add it to my training. So please accept my apologies for the time being. In the meantime, would you please try to express your request differently? 
       """,
    "CR_OTHER_START_AF_URL": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb647748bae486c699775f.mp4',
    "CR_OTHER_START_VF_URL": '',
    
    "CR_GENERAL_START": " I hope I’ve answered your question, {first_name}.",
    "CR_GENERAL_START_AF_URL": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ede1df30045630d8a2c86b.mp4', 
    "CR_GENERAL_START_VF_URL": '',
    
    "CR_PURCHASE_NEEDED": " Please let me know if you are ready to purchase one of our Living Trust Packages.",
    "CR_PURCHASE_NEEDED_AF_URL": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64774e95566935f26da4.mp4',
    "CR_PURCHASE_NEEDED_VF_URL": '',
    
    "CR_PACKAGE_NEEDED": " Please let me know which Living Trust Package you’ve decided to purchase: the Revocable Living Trust Package or the Irrevocable Living Trust Package.",
    "CR_PACKAGE_NEEDED_AF_URL": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64760fbb9121f13ba88c.mp4',
    "CR_PACKAGE_NEEDED_VF_URL": '',
    
    "CR_NUMPAYMENTS_NEEDED": " Please let me know if you would like to make your Living Trust Package purchase in one, two, or three payments.",
    "CR_NUMPAYMENTS_NEEDED_AF_URL": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64776c2b341ba655775e.mp4',
    "CR_NUMPAYMENTS_NEEDED_VF_URL": '',
    
    "CR_DISPLAY_NEEDED": " Please let me know when you have displayed your Retainer Agreement for your review.",
    "CR_DISPLAY_NEEDED_AF_URL": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb6477b8d5547f12dcc6f2.mp4',
    "CR_DISPLAY_NEEDED_VF_URL": '',
    
    "CR_SIGNATURE_NEEDED": " Please let me know when you have signed your Retainer Agreement.",
    "CR_SIGNATURE_NEEDED_AF_URL": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb647748bae430c1997763.mp4',
    "CR_SIGNATURE_NEEDED_VF_URL": '',
    
    "CR_PAYMENT_NEEDED": " Please let me know when you have made your payment.",
    "CR_PAYMENT_NEEDED_AF_URL": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb6477707cef563c179101.mp4',
    "CR_PAYMENT_NEEDED_VF_URL": '',
    
    "CR_BOOKING_NEEDED": " Please let me know when you have booked your Onboarding meeting.",
    "CR_BOOKING_NEEDED_AF_URL": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb6477707ceffbf5179100.mp4',
    "CR_BOOKING_NEEDED_VF_URL": '',
    
    "CR_COMPLETED": " Thank you for completing your Living Trust package purchase. Our Human Onboarding Specialist is looking forward to meeting you!",
    "CR_COMPLETED_AF_URL": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb6477707cef861f179102.mp4',
    "CR_COMPLETED_VF_URL": '',
    
    "CR_ADDITIONAL_QUESTIONS": " Let me know, {first_name}, if you have any additional questions.",
    "CR_ADDITIONAL_QUESTIONS_AF_URL": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64774e95567ea7f26da3.mp4',
    "CR_ADDITIONAL_QUESTIONS_VF_URL": '',
    
    "CR_TRANSFER_TO_HUMAN": """
            I understand that you would like to speak to a Human, {first_name}. That's a valid concern. The good news is we have some great humans for you to speak to! 
            It has been my pleasure assisting you. Please call 888-992-7979 and give them reference number 101, and our Human Onboarding 
            Specialists will extend to you our special 30% AI pricing discount as a courtesy for trying out our AI system. 
            Our goal is to make this a great experience for you, and I sincerely hope I have done that! 
            If you have any further questions, please feel free to ask.
    """,
    "CR_TRANSFER_TO_HUMAN_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb647748bae455fa99775e.mp4",
    "CR_TRANSFER_TO_HUMAN_VF_URL": "",
    
    "CR_NEW_GREETING_MESSAGE": "Hi {first_name}, and welcome! I'm AI Kelly, your friendly New York estate law artificial intelligence agent. You can make your estate plan purchase through me and also ask me questions. Your chat history will be recorded to best serve you and for quality control purposes. Please note, I am not an attorney, so I can't give you legal advice, but I can provide lots of information from my training.", # updated
    "CR_NEW_GREETING_MESSAGE_AF_URL": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5f00933c027e262ce9e84.mp4', 
    "CR_NEW_GREETING_MESSAGE_VF_URL": '',
    
    "CR_OLD_GREETING_MESSAGE": "Hi {first_name}, welcome back!", # updated
    "CR_OLD_GREETING_MESSAGE_AF_URL": 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5f0099d49bd2520928f27.mp4',
    "CR_OLD_GREETING_MESSAGE_VF_URL": '',
    
    "CP_COMMAND_AND_CONTROL": "Whats my name, repeat, did i asked this question already, are you alive, are you going to take over the world",
    
    "CP_IS1_SYSTEM_PROMPT" : """
        {CP_PREAMBLE}\n
        {CP_GREETING}\n
        {CP_COMMAND_AND_CONTROL}\n
        {CP_GENERAL}\n
        {CP_TRANSFER_TO_HUMAN}\n
        {CP_OBJECTION}\n
        Retainer Q&A :  If user is asking user about his agreement, or retainer.\n
        Purchase: The user is expressing intent to buy or that they are ready to make a purchase.\n            
        {CP_POSITIVE}\n
        {CP_NEGATIVE}\n
        {CP_MORE_QUESTIONS}\n
        {CP_OTHER}\n
        {CP_TASK}\n
        Greeting, General, Transfer To Human, Retainer Q&A, Objection, Purchase, Positive, Negative, More Question, or Other.
    """,
    
    "CR_IS1_PURCHASE": "That’s great, {first_name}! I’m excited that you’ve decided to make a purchase today!",
    "CR_IS1_PURCHASE_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb6477c7fd50d454ab4b01.mp4",
    "CR_IS1_PURCHASE_VF_URL": "",
    
    "CP_IS2_SYSTEM_PROMPT": """
        {CP_PREAMBLE}\n
        {CP_GREETING}\n
        {CP_GENERAL}\n
        {CP_TRANSFER_TO_HUMAN}\n
        {CP_OBJECTION}\n
        Trust Package: The user is giving the name of one of the trust packages (revocable and irrevocable), or user is telling the that he is selecting revocable or irrevocable trust package.\n
        Retainer Q&A :  If user is asking user about his agreement, or retainer.\n
        Payments: The user is telling their choice about how many payments they would like. Uner may give only a number or in words or may give a sentence which tells how many payments they would like to make. For example, they may reply with just the number 1 or 2 or 3 or 4 or 5 or 6 or in words like one or two or three upto so on or they may say i want 3/three payments or something like that.\n
        {CP_POSITIVE}\n
        {CP_NEGATIVE}\n
        {CP_MORE_QUESTIONS}\n
        {CP_OTHER}\n
        {CP_TASK}\n
        Greeting, General, Transfer To Human, Objection, Trust Package, Retainer Q&A, Payments, Positive, Negative, More Question, or Other.
   """,

    "CP_IS2_TRUST_PACKAGE_PROMPT": """
            {CP_PREAMBLE}
            Revocable Living Trust Package: If user is telling that he wants to buy Revocable or Revocable Trust Package
            Irrevocable Living Trust Package: If user is telling that he wants to buy Irrevocable or Irrevocable Trust Package
            {CP_TASK} 
                'Revocable Living Trust Package' or 
                'Irrevocable Living Trust Package'.
       """,
    "CR_IS2_TRUST_PACKAGE": "Thank you for that information, {first_name}.",
    "CR_IS2_TRUST_PACKAGE_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ede1df32bfcaed194ba42d.mp4",
    "CR_IS2_TRUST_PACKAGE_VF_URL": "",
    
    "CP_IS2_PAYMENTS_PROMPT": """
            {CP_PREAMBLE}
            1: if user is asking or telling that he wants to make full payment at once or one payment or 1 or One.
            2: if user is asking or telling to divide the payments into or just saying 2 or two.
            3: if user is asking or telling to devide the payments into or just saying 3 or three.
            4: if user is asking or telling to devide the payments into or just saying 4 or four.
            5: if user is asking or telling to devide the payments into or just saying 5 or five.
            6: if user is asking or telling to devide the payments into or just saying 6 or six.
            7: if user is asking or telling to devide the payments into more than 6 or less than 1
            {CP_TASK} 
                1, 
                2, 
                3, 
                4, 
                5, 
                6 or 
                7.
       """,
    "CR_IS2_PAYMENTS": """
            Thank you for that information, {first_name}. I am now going to send you a link to your retainer agreement by email and text. 
            Also, I have some good news, {first_name}. If you purchase your NY Estate Law .ai Living Trust Package in the next 15 minutes, 
            I’m authorized to give you an additional 10% off as a thank you for being an early adopter of our AI technology."
    """,
    "CR_IS2_PAYMENTS_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64774e95569f30f26da2.mp4",
    "CR_IS2_PAYMENTS_VF_URL": "",
    
    "CR_IS2_INVALID_NUM_PAYMENTS": "My apologies, but I am only programmed to approve a request of up to six monthly payments. Kindly choose between 1 and 6 payments. If you need a longer payment plan, please request to be transferred to a human, where you can discuss this with one of our wonderful Human Onboarding Specialists.",
    "CR_IS2_INVALID_NUM_PAYMENTS_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64777172d71334738e39.mp4",
    "CR_IS2_INVALID_NUM_PAYMENTS_VF_URL": "",
    
    "CP_IS4_SYSTEM_PROMPT": """
        {CP_PREAMBLE}\n
        {CP_GREETING}\n
        {CP_GENERAL}\n
        {CP_TRANSFER_TO_HUMAN}\n
        {CP_OBJECTION}\n
        Retainer Q&A :  If user is asking user about his agreement, or retainer.\n
        Issue with Task: User indicates there is some issue with completing the task. Return one of the following: Email not received, Link doesn't work, No available times to book appointment, Trouble making payment, Invoice not received, Retainer not received.\n
        Change Trust Package: If user's messages indicates that they want to change their Trust Package.\n
        Change Payment Plan: If user asks that he wants to change his payment plan or payment division or something like that.\n
        Change Other Info: If user is asking for help in changing their other information like name, email, phone, zip, address anything other than Trust Package or Payment Plan\n
        {CP_POSITIVE}\n
        {CP_NEGATIVE}\n
        {CP_MORE_QUESTIONS}\n
        {CP_OTHER}\n
        {CP_TASK}\n
            Greeting, General, Transfer To Human, Objection, Retainer Q&A, Issue with Task,  Change Trust Package, Change Payment Plan, Change Other Info, Positive, Negative, More Question, or Other.
    """,
    
    "CR_IS4_TASK_ISSUE": "I'm sorry you're having trouble, I will attempt to repeat my last task. If you continue to experience issues, please call 888-992-7979 to speak with one of our wonderful human Onboarding Specialists who will be able to assist you further.",
    "CR_IS4_TASK_ISSUE_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f0718bd5d0a8df05cd78cf.mp4",
    "CR_IS4_TASK_ISSUE_VF_URL": "",
    
    "CR_IS4_AGREEMENT_DISPLAYED": "Perfect! Once you have signed and made your payment, we'll get you booked with a Human Onboarding Specialist.",
    "CR_IS4_AGREEMENT_DISPLAYED_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb6476707cef5b3d1790ff.mp4",
    "CR_IS4_AGREEMENT_DISPLAYED_VF_URL": "",
    
    "CR_IS4_AGREEMENT_SIGNATURE_DONE": "Excellent! I have sent you an Email with invoice link, Once you have made your payment, we'll get your onboarding appointment booked.",
    "CR_IS4_AGREEMENT_SIGNATURE_DONE_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ede1dfaeed8e3ae28e478b.mp4",
    "CR_IS4_AGREEMENT_SIGNATURE_DONE_VF_URL": "",
    
    "CR_IS4_AGREEMENT_PAID": """
           Thank you, {first_name}, for placing your trust in NY Estate Law .ai. 
            You’ve now begun your Estate Planning journey and are on your way to achieving peace of mind! 
            \n\nNow it’s time to schedule your appointment with one of our Human Onboarding Specialists. 
            Your Human Onboarding appointment should only take 10-15 minutes. 
            I am sending you the Calendar Booking link by email and text. When you receive the link, please click it and select a date and time that is convenient for you. 
       """,
    "CR_IS4_AGREEMENT_PAID_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f044efacfd664ce67857ca.mp4",
    "CR_IS4_AGREEMENT_PAID_VF_URL": "",
    "CR_IS4_OS_BOOKING_DONE": "Now that you've booked your Onboarding Specialist appointment, you and I are all wrapped up! My name is AI Kelley, and it has been my pleasure serving you. On behalf of everyone at NY Estate Law .ai, I want to thank you for your business. Our goal is to make this a great experience for you, and I sincerely hope I have done that!",
    "CR_IS4_OS_BOOKING_DONE_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f03e764b96a9a2a4c4c7d2.mp4",
    "CR_IS4_OS_BOOKING_DONE_VF_URL": "",
    
    "CR_IS4_BOOKING_COMPLETED": "Awesome. You're going to love meeting your NY Estate Law .ai attorney and I know they are looking forward to meeting you. Please gather all your unique questions together and get ready for an incredible experience!",
    "CR_IS4_BOOKING_COMPLETED_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ede1df7bf4ab1c7f119b31.mp4",
    "CR_IS4_BOOKING_COMPLETED_VF_URL": "",
    
    "CR_IS4_CHANGE_TRUST_PACKAGE": "Not a problem.",
    "CR_IS4_CHANGE_TRUST_PACKAGE_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb6477707cef1c98179103.mp4",
    "CR_IS4_CHANGE_TRUST_PACKAGE_VF_URL": "",
    
    "CR_IS4_CHANGE_PAYMENT_PLAN": "No problem.",
    "CR_IS4_CHANGE_PAYMENT_PLAN_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64760fbb91a6473ba88d.mp4",
    "CR_IS4_CHANGE_PAYMENT_PLAN_VF_URL": "",
    
    "CR_IS4_CHANGE_OTHER_INFO_START": """
        Certainly. I am not currently programmed to take updated information.
        However, there are two ways to do that. You can continue with the current info and then tell your Onboarding Specialist of the change you would like to make.
        Or, on the web pages, you can go to Step 3 and edit your info and put correct info in and save. Please note that if you change your email or phone number, this will restart the purchase process.
    """,
    "CR_IS4_CHANGE_OTHER_INFO_START_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66ede1df7bf4abfbb5119b32.mp4",
    "CR_IS4_CHANGE_OTHER_INFO_START_VF_URL": "",
    
    "CR_IS4_OTHER": "I’m sorry, {first_name}. As an AI, I’m only trained on very specific tasks. That is not a request I recognize. I will log the request so that a human can review it and see if it should be added to my training. Please accept my apologies for the time being. In the meantime, would you please try to express your request differently or let me know if you have any further questions about your Retainer Agreement?",
    "CR_IS4_OTHER_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66eb64770fbb91d43d3ba88e.mp4",
    "CR_IS4_OTHER_VF_URL": "",
    
    "CR_ERROR_APPOLOGY": "Please accept my apologies, we're still working out some of the bugs in our new AI service. The issue has been logged and will be corrected. In the meantime, please rephrase your question and I'll see if I can answer it. You can also call 888-992-7979 for assistance from one of our wonderful human Onboarding Specialists.",
    "CR_ERROR_APPOLOGY_AF_URL": "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f03db8d5d0a82f31ccd47e.mp4",
    "CR_ERROR_APPOLOGY_VF_URL": "",

    "CR_GREETING_INNER_INTENT_PROMPT" : '''
        {CP_PREAMBLE}
        Salutation: If user message contains a polite or casual greeting such as 'hi,' 'hello,' 'hey,' 'good morning,' 'what's up," or similar, respond with 'Salutation'
        Polite Concern: "Given this user message, determine if it expresses polite concern for health or well-being, such as 'How are you?' 'How's it going?' 'Hope you're doing well,' or similar phrases. If the message expresses concern for well-being, respond with 'Polite Concern.' 
        Prior Question: Given this user message, determine if the user is asking whether they have already asked a question or made an inquiry. If the message involves checking if they've already asked something (e.g., 'Did I already ask this?' or 'Have I asked this before?'), respond with 'Prior Question.'
        Asking for Name: Given this user message, determine if the user is asking for their own name or thier personal information, such as 'What’s my name?' or 'Do you know my me or my name?' or something else personal about him or someone else personal inforamtion, respond with 'Asking for Name.'
        {CP_OTHER}
        {CP_TASK} 
        Salutation, Polite Concern, Prior Question, Asking for Name, or Other.
    ''',

    "CR_GREETING_SALUTATION" : "Hi. It's a wonderful day here in AI land, I hope it's a wonderful day for your too.",
    "CR_GREETING_SALUTATION_AF_URL" : 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5f009c293c426b13f2841.mp4',
    "CR_GREETING_SALUTATION_VF_URL" : '',

    "CR_GREETING_POLITE_CONCERN" : "I'm well thanks (as well as an AI can be that is), thanks for asking.",
    "CR_GREETING_POLITE_CONCERN_AF_URL" : 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5f0099d49bd3c34928f26.mp4',
    "CR_GREETING_POLITE_CONCERN_VF_URL" : '',

    "CR_GREETING_PRIOR_QUESTION" : "As a trained AI, I'm not currently trained to lookup prior questions, however, you can feel free to ask me again.",
    "CR_GREETING_PRIOR_QUESTION_AF_URL" : 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5f009aed0c7651c0a026c.mp4',
    "CR_GREETING_PRIOR_QUESTION_VF_URL" : '',

    "CR_GREETING_ASKING_NAME" : "As a trained AI, I am currently trained to refrain from repeating back a potential client's private information, however, you can rest assured that the information you entered when you initiating the AI has been safely captured and stored and will be available to our wonderful team of humans.",
    "CR_GREETING_ASKING_NAME_AF_URL" : 'https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5f0099d49bd6ac7928f28.mp4',
    "CR_GREETING_ASKING_NAME_VF_URL" : '',
}


# Get the constants collection
Constants_Collection = db.get_collection("constants")



# Loop through constants_dict and insert each variable name and value into the database
for variable_name, value in variables_dict.items():
    Constants_Collection.insert_one(
        {
            "variable_name": variable_name,
            "value": value
        }
    )