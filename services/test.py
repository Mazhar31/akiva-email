# import argparse
# import json
import openai
# from argparse import RawTextHelpFormatter
# import requests
# from typing import Optional
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import warnings
from astrapy import DataAPIClient
from .intent_analysis import add_intent_id
from . bubbles import check_bubbles, find_bubbles_value, intent_section_1_bubbles, intent_section_2_bubbles, payment_bubbles, General_QA_URL_Dict, Objection_QA_URL_Dict, Retainer_QA_URL_Dict
from .inner_intents import inner_intent_analysis_General_QA, inner_intent_analysis_retainer_QA, inner_intent_analysis_objection_QA, handle_greetings
from . import constants
import time

# Define the timeout intervals in seconds
timeouts = [30, 90, 210, 390, 810, 900]  # 1.5 minutes = 90 seconds, 3.5 minutes = 210 seconds, etc.


load_dotenv()

#get API key for GPT from .streamlit/secrets.toml file
openai.api_key =os.getenv("openai_api")

# Initialize the Astra DB client
token = os.getenv("datastax_client_API")
client = DataAPIClient(token)
url = os.getenv("DB_endpoint")
db = client.get_database_by_api_endpoint(url)


next_needed_collection = db.get_collection("next_needed")
user_choices_collection = db.get_collection("user_choices")

def new_logic(modality, session_id, first_name, dict):
    next = next_needed_collection.find_one({"session_id": session_id})
    next_needed = next.get("next_needed")

    response = ''
    video_urls = []
    audio_urls = []
    bubbles = []
    error_messages = []
    retainer_type = ''
    payment_plan = ''
    send_retainer = 'False'
    Send_Booking_Calendar = ''

    print(next_needed)
    if next_needed == 'Purchase':
        next_needed_text = constants.CR_PURCHASE_NEEDED
        next_needed_video_URL = constants.CR_PURCHASE_NEEDED_AF_URL
        next_needed_audio_URL = constants.CR_PURCHASE_NEEDED_VF_URL

    elif next_needed == 'Package':
        next_needed_text = constants.CR_PACKAGE_NEEDED
        next_needed_video_URL = constants.CR_PACKAGE_NEEDED_AF_URL
        next_needed_audio_URL = constants.CR_PACKAGE_NEEDED_VF_URL
    
    elif next_needed == 'Numpayments':
        next_needed_text = constants.CR_NUMPAYMENTS_NEEDED
        next_needed_video_URL = constants.CR_NUMPAYMENTS_NEEDED_AF_URL
        next_needed_audio_URL = constants.CR_NUMPAYMENTS_NEEDED_VF_URL

    elif next_needed == 'Displayed':
        next_needed_text = constants.CR_DISPLAY_NEEDED
        next_needed_video_URL = constants.CR_DISPLAY_NEEDED_AF_URL
        next_needed_audio_URL = constants.CR_DISPLAY_NEEDED_VF_URL

    elif next_needed == 'Signature':
        next_needed_text = constants.CR_SIGNATURE_NEEDED
        next_needed_video_URL = constants.CR_SIGNATURE_NEEDED_AF_URL
        next_needed_audio_URL = constants.CR_SIGNATURE_NEEDED_VF_URL

    elif next_needed == 'Paid':
        next_needed_text = constants.CR_PAYMENT_NEEDED
        next_needed_video_URL = constants.CR_PAYMENT_NEEDED_AF_URL
        next_needed_audio_URL = constants.CR_PAYMENT_NEEDED_VF_URL

    elif next_needed == 'Booking':
        next_needed_text = constants.CR_BOOKING_NEEDED
        next_needed_video_URL = constants.CR_BOOKING_NEEDED_AF_URL
        next_needed_audio_URL = constants.CR_BOOKING_NEEDED_VF_URL
    # need to ask about this
    elif next_needed == 'Completed':
        next_needed_text = constants.CR_IS4_OS_BOOKING_DONE
        next_needed_video_URL = constants.CR_IS4_OS_BOOKING_DONE_AF_URL
        next_needed_audio_URL = constants.CR_IS4_OS_BOOKING_DONE_VF_URL


    if modality == 'Avatar' or modality == 'Voice' or modality == 'Chatbot':
        Text = ''
        for i in dict["Texts"]:
            Text = Text + i
        if dict["Additional_Questions"] == "True":
            response = Text + next_needed_text + constants.CR_ADDITIONAL_QUESTIONS
        else:
            response = Text + next_needed_text

        response = response.replace("{first_name}", first_name)
    
        if modality == 'Avatar':
            if dict["Avatar_URLs"]:
                for i in dict["Avatar_URLs"]:
                    video_urls.append(i)
                video_urls.append(next_needed_video_URL)
                if dict["Additional_Questions"] == "True":
                    video_urls.append(constants.CR_ADDITIONAL_QUESTIONS_AF_URL)
        
        elif modality == 'Voice':
            if dict["Voice_URLs"]:
                for i in dict["Voice_URLs"]:
                    audio_urls.append(i)
                audio_urls.append(next_needed_audio_URL)
                if dict["Additional_Questions"] == "True":
                    audio_urls.append(constants.CR_ADDITIONAL_QUESTIONS_VF_URL)

    else:
        error_messages.append("Sorry I don't recognize this Modality. Can you please re-check.")
         

    res = {
            "Text": response, # from this response dict you will be getting only the text
            "Video_URLs": video_urls,
            "Voice_URLs": audio_urls,
            "Bubbles":bubbles,
            "Command" : error_messages,
            "Retainer_Type" : retainer_type,
            "Payment_Plan" : payment_plan,
            "Send_retainer" : send_retainer,
            "Send_Booking_Calendar" : Send_Booking_Calendar,
        }
    
    return res


def calculate_running_time (function):
    def wrapper(*args,**kwargs):
        before = time.time()
        value= function(*args, **kwargs)
        after = time.time()
        fname= function.__name__
        print (f"{fname} took {after-before} seconds to execute!")
        return value
    return wrapper


def timeout(name):
    start_time = time.time()
    current_timeout_index = 0
    
    while current_timeout_index < len(timeouts):
        elapsed_time = time.time() - start_time
        
        if elapsed_time >= timeouts[current_timeout_index]:
            print(f"Hey {name}, please let me know if you have any more questions or need additional time to sign the retainer agreement.")
            current_timeout_index += 1


def small_chats_with_GPT(chat_history):
    system_prompt = '''
    You are a friendly AI for NYEstateLaw.ai.
    You are to converse as if you were a friendly and sympathetic human, but so that we are fully transparent with our clients, you will not hide the fact that you are an AI, and will affirmatively and proudly answer questions posed to you about being an AI. 
    You can see user name from the above bot response to call user with his/her name if required. You can just give answer to user's small talks like greeting or genral small talks. Don't ask user questions like: If you have any questions or need information about our Living Trust Packages, feel free to ask! or If there's anything else you'd like to chat about or if you have questions regarding our services, just let me know! or anything similar, just answer to user question which is the last user message in user's prompt
    Please just answer to user's question according to the rules defined above
    '''
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        #messages=[{"role": "system", "content": "You can see user name from the above bot response to call user with his/her name if required. You can just give answer to user's small talks like greeting or genral small talks like 'how are you?' or something like this."},
        #          {"role": "user", "content": f"{chat_history}"}],
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": f"{chat_history}"}],
        max_tokens=300,
        temperature=0.1
    )

    # Add the bot's response to the chat history
    bot_response = response.choices[0].message.content
    
    return bot_response


def intent_analysis_with_GPT(input, system_prompt):
      
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": f"User message: {input}"}],
        max_tokens=300,
        temperature=0.1
    )

    # Add the bot's response to the chat history
    bot_response = response.choices[0].message.content
    return bot_response


def log_user_request(session_id, message):

    data_to_insert = {
        "session_id" : session_id,
        "user_request": message,
        "time_stamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Get current time stamp
        "resolution_code": 'New',
        "resolution_person": 'Akiva'
    }
    # Collections for session and chat history
    other_collection = db.get_collection("other")
    other_collection.insert_one(data_to_insert)


def chat_flow_for_intent_section_1(message, chat_history, first_name, session_id, modality):
    print("\nWe are in chat_flow_for_intent_section_1\n")
    system_prompt = constants.CP_IS1_SYSTEM_PROMPT
    analysis = ''
    res = None
    try:
        if message == "1":  # or if null
            analysis = "Purchase"
        
        elif message == "I^":
            try:
                initiate_ai_collection = db.get_collection("initiate_ai")
                data = initiate_ai_collection.find_one({"session_id": session_id})
                    
                initiate_ai_collection.update_one(
                    {"session_id": session_id},
                    {
                        "$set":{'User_Type' : "old",}
                    },
                    upsert=True
                )

                if data.get('User_Type') == 'New':
                    initial_text = constants.CR_NEW_GREETING_MESSAGE
                    dict = {
                        "Texts" : [initial_text],
                        "Avatar_URLs" : [constants.CR_NEW_GREETING_MESSAGE_AF_URL],
                        "Voice_URLs" : [constants.CR_NEW_GREETING_MESSAGE_VF_URL],
                        "Additional_Questions" : "False"
                    }
                    
                    res = new_logic(modality, session_id, first_name, dict)
                    text = res["Text"] + " Or do you have some questions first?"
                    res["Bubbles"] = [intent_section_1_bubbles]
                    res["Text"] = text

                else:
                    initial_text = constants.CR_OLD_GREETING_MESSAGE
                    dict = {
                        "Texts" : [initial_text],
                        "Avatar_URLs" : [constants.CR_OLD_GREETING_MESSAGE_AF_URL],
                        "Voice_URLs" : [constants.CR_OLD_GREETING_MESSAGE_VF_URL],
                        "Additional_Questions" : "True"
                    }
                    res = new_logic(modality, session_id, first_name, dict)
                    res["Bubbles"] = [intent_section_1_bubbles]
            except Exception as e:
                print(e)
        
        else:
            analysis = intent_analysis_with_GPT(message, system_prompt)
            print(f"\n\n\nAnalysis : {analysis}")

        
        if analysis == "Greeting":
            initial_text, video_url, audio_url =  handle_greetings(message)
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [video_url],
                "Voice_URLs" : [audio_url],
                "Additional_Questions" : "True"
            }
            res = new_logic(modality, session_id, first_name, dict)
            res["Bubbles"] = [intent_section_1_bubbles]

        elif analysis == "Purchase":
            initial_text =  constants.CR_IS1_PURCHASE
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [constants.CR_IS1_PURCHASE_AF_URL],
                "Voice_URLs" : [constants.CR_IS1_PURCHASE_VF_URL],
                "Additional_Questions" : "True"
            }
            
            next_needed_collection.update_one(
                {"session_id": session_id},
                {"$set": {"next_needed": "Package"}}
            )

            res = new_logic(modality, session_id, first_name, dict)
            
            res["Bubbles"] = [intent_section_2_bubbles]
            add_intent_id(session_id, '2')

        elif analysis == "Transfer To Human":
            initial_text =  constants.CR_TRANSFER_TO_HUMAN
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [constants.CR_TRANSFER_TO_HUMAN_AF_URL],
                "Voice_URLs" : [],
                "Additional_Questions" : "False"
            }
            res = new_logic(modality, session_id, first_name, dict)
            res["Bubbles"] = [intent_section_1_bubbles]
            
        elif analysis == "General":
            result, inner_intent = inner_intent_analysis_General_QA(message, modality, first_name)
            
            if inner_intent == "Other":
                initial_text =  constants.CR_OTHER_START
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_OTHER_START_AF_URL],
                    "Voice_URLs" : [constants.CR_OTHER_START_VF_URL],
                    "Additional_Questions" : "True"
                }

                res = new_logic(modality, session_id, first_name, dict)
                
                res["Bubbles"] = [intent_section_1_bubbles]
                log_user_request(session_id, message)
            
            else:
                print("result : ", result)
                
                initial_text = result + constants.CR_GENERAL_START
                try:
                    dict = {
                        "Texts" : [initial_text],
                        "Avatar_URLs" : [General_QA_URL_Dict[inner_intent], constants.CR_GENERAL_START_AF_URL],
                        "Voice_URLs" : [],
                        "Additional_Questions" : "True"
                    }

                    res = new_logic(modality, session_id, first_name, dict)
                
                    res["Bubbles"] = [intent_section_1_bubbles]

                except Exception as e:
                    print("\n\n",e)

        elif analysis == "Objection":
            result, inner_intent = inner_intent_analysis_objection_QA(message, modality, first_name)
            
            if inner_intent == "Other":
                initial_text =  constants.CR_OTHER_START
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_OTHER_START_AF_URL],
                    "Voice_URLs" : [constants.CR_OTHER_START_VF_URL],
                    "Additional_Questions" : "True"
                }
                log_user_request(session_id, message)
                res = new_logic(modality, session_id, first_name, dict)
            else:
                initial_text = result + constants.CR_GENERAL_START
                
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [Objection_QA_URL_Dict[inner_intent], constants.CR_GENERAL_START_AF_URL],
                    "Voice_URLs" : [],
                    "Additional_Questions" : "True"
                }

                res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "Retainer Q&A":
            result, inner_intent = inner_intent_analysis_retainer_QA(message, modality, first_name)
            
            if inner_intent == "Other":
                initial_text =  constants.CR_OTHER_START
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_OTHER_START_AF_URL],
                    "Voice_URLs" : [constants.CR_OTHER_START_VF_URL],
                    "Additional_Questions" : "True"
                }
                log_user_request(session_id, message)
                res = new_logic(modality, session_id, first_name, dict)
            else:
                initial_text = result + constants.CR_GENERAL_START
                
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [Retainer_QA_URL_Dict[inner_intent], constants.CR_GENERAL_START_AF_URL],
                    "Voice_URLs" : [],
                    "Additional_Questions" : "True"
                }

                res = new_logic(modality, session_id, first_name, dict)
        
        elif analysis == "Positive":
            next = next_needed_collection.find_one({"session_id": session_id})
            next_needed = next.get("next_needed")
            print("Next needed : ", next_needed)

            if next_needed == 'Purchase':
                next_needed_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"next_needed": "Package"}}
                )
                initial_text =  "Awesome! "
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_IS4_AGREEMENT_DISPLAYED_AF_URL],
                    "Voice_URLs" : [constants.CR_IS4_AGREEMENT_DISPLAYED_VF_URL],
                    "Additional_Questions" : "True"
                }
                res = new_logic(modality, session_id, first_name, dict)
                res["Bubbles"] = [intent_section_2_bubbles]
                add_intent_id(session_id, '2')
            
            else:
                initial_text =  "Glad to hear that!"
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [],
                    "Voice_URLs" : [],
                    "Additional_Questions" : "False"
                }
                res = new_logic(modality, session_id, first_name, dict)
            
        elif analysis == "Negative":
            initial_text =  constants.CR_NEGATIVE_MESSAGE
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [],
                "Voice_URLs" : [],
                "Additional_Questions" : "False"
            }
            res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "More Question":
            initial_text =  constants.CR_MORE_QUESTIONS
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [],
                "Voice_URLs" : [],
                "Additional_Questions" : "False"
            }
            res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "Other":
            print("1")
            initial_text =  constants.CR_OTHER_START
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [constants.CR_OTHER_START_AF_URL],
                "Voice_URLs" : [constants.CR_OTHER_START_VF_URL],
                "Additional_Questions" : "True"
            }
            print("1")
            res = new_logic(modality, session_id, first_name, dict)
            
            res["Bubbles"] = [intent_section_1_bubbles]
            log_user_request(session_id, message)

        return res
    except Exception as e:
        print(e)


def chat_flow_for_intent_section_2(message, chat_history, first_name, session_id, modality):
    print("\nWe are in chat_flow_for_intent_section_2\n")
    system_prompt = constants.CP_IS2_SYSTEM_PROMPT
    analysis = ''
    res = None
    try:
        user_choices = user_choices_collection.find_one({"session_id": session_id})
        # valid_trust_list = ['1', '2']
        # valid_payment_list = ["1", "2", "3", "4", "5", "6", "one", "two", "three"]
        trust_package = user_choices.get("Trust_Package")
        payments = user_choices.get("Payments")
        # if message in valid_trust_list and trust_package is None:
        #     analysis = "Trust Package"
        # elif message in valid_payment_list and payments is None:
        #     analysis = "Payments"
        # else:
        #     analysis = intent_analysis_with_GPT(message, system_prompt)
        #     updated_query = f"User message: {message}\n\n Chat History: {chat_history}"
        if message == "I^":
            initiate_ai_collection = db.get_collection("initiate_ai")
            data = initiate_ai_collection.find_one({"session_id": session_id})
                
            initiate_ai_collection.update_one(
                {"session_id": session_id},
                {
                    "$set":{'User_Type' : "old",}
                },
                upsert=True
            )

            if data.get('User_Type') == 'New':
                initial_text = constants.CR_NEW_GREETING_MESSAGE
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_NEW_GREETING_MESSAGE_AF_URL],
                    "Voice_URLs" : [constants.CR_NEW_GREETING_MESSAGE_VF_URL],
                    "Additional_Questions" : "False"
                }
                res = new_logic(modality, session_id, first_name, dict)
                text = res["Text"] + " Or do you have some questions first?"
                res["Bubbles"] = [intent_section_1_bubbles]
                res["Text"] = text

            else:
                initial_text = constants.CR_OLD_GREETING_MESSAGE
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_OLD_GREETING_MESSAGE_AF_URL],
                    "Voice_URLs" : [constants.CR_OLD_GREETING_MESSAGE_VF_URL],
                    "Additional_Questions" : "True"
                }
                res = new_logic(modality, session_id, first_name, dict)
                res["Bubbles"] = [intent_section_1_bubbles]
        
        else:
            analysis = intent_analysis_with_GPT(message, system_prompt)
            updated_query = f"User message: {message}\n\n Chat History: {chat_history}"
            print(f"\n\n\nAnalysis : {analysis}")


        if analysis == "Greeting":
            initial_text, video_url, audio_url =  handle_greetings(message)
            print(initial_text)
                
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [video_url],
                "Voice_URLs" : [audio_url],
                "Additional_Questions" : "True"   
            }

            res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "General":
            result, inner_intent = inner_intent_analysis_General_QA(message, modality, first_name)
            if inner_intent == "Other":
                initial_text =  constants.CR_OTHER_START
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_OTHER_START_AF_URL],
                    "Voice_URLs" : [constants.CR_OTHER_START_VF_URL],
                    "Additional_Questions" : "True"
                }
                res = new_logic(modality, session_id, first_name, dict)
                log_user_request(session_id, message)
            
            else:
                initial_text = result + constants.CR_GENERAL_START
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [General_QA_URL_Dict[inner_intent], constants.CR_GENERAL_START_AF_URL],
                    "Voice_URLs" : [],
                    "Additional_Questions" : "True"
                }
                res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "Objection":
            result, inner_intent = inner_intent_analysis_objection_QA(message, modality, first_name)
            
            if inner_intent == "Other":
                initial_text =  constants.CR_OTHER_START
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_OTHER_START_AF_URL],
                    "Voice_URLs" : [constants.CR_OTHER_START_VF_URL],
                    "Additional_Questions" : "True"
                }
                log_user_request(session_id, message)
                res = new_logic(modality, session_id, first_name, dict)
            else:
                initial_text = result + constants.CR_GENERAL_START
                
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [Objection_QA_URL_Dict[inner_intent], constants.CR_GENERAL_START_AF_URL],
                    "Voice_URLs" : [],
                    "Additional_Questions" : "True"
                }

                res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "Transfer To Human":
            initial_text =  constants.CR_TRANSFER_TO_HUMAN
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [constants.CR_TRANSFER_TO_HUMAN_AF_URL],
                "Voice_URLs" : [],
                "Additional_Questions" : "False"
            }
            res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "Other":
            initial_text =  constants.CR_OTHER_START
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [constants.CR_OTHER_START_AF_URL],
                "Voice_URLs" : [constants.CR_OTHER_START_VF_URL],
                "Additional_Questions" : "True"
            }
            res = new_logic(modality, session_id, first_name, dict)
            log_user_request(session_id, message)

        elif analysis == "Trust Package":
            # if message in valid_trust_list:
            #     selected_trust = intent_section_2_bubbles[message]
            # else:
            #     prompt = constants.CP_IS2_TRUST_PACKAGE_PROMPT
            #     selected_trust = intent_analysis_with_GPT(message, prompt)
            
            prompt = constants.CP_IS2_TRUST_PACKAGE_PROMPT
            selected_trust = intent_analysis_with_GPT(message, prompt)
            
            next_needed_collection.update_one(
                {"session_id": session_id},
                {"$set": {"next_needed": "Numpayments"}}
            )

            user_choices_collection.update_one(
                {"session_id": session_id},
                {"$set": {"Trust_Package": selected_trust}}
            )
            initial_text =  constants.CR_IS2_TRUST_PACKAGE
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [constants.CR_IS2_TRUST_PACKAGE_AF_URL],
                "Voice_URLs" : [],
                "Additional_Questions" : "True"
            }
            res = new_logic(modality, session_id, first_name, dict)
            res["Bubbles"] = [payment_bubbles]

        elif analysis == "Positive":
            initial_text =  constants.CR_POSITIVE_MESSAGE
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [],
                "Voice_URLs" : [],
                "Additional_Questions" : "True"
            }
            res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "Negative":
            initial_text =  constants.CR_NEGATIVE_MESSAGE
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [],
                "Voice_URLs" : [],
                "Additional_Questions" : "False"
            }
            res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "More Question":
            initial_text =  constants.CR_MORE_QUESTIONS
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [],
                "Voice_URLs" : [],
                "Additional_Questions" : "False"
            }
            res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "Retainer Q&A":
            result, inner_intent = inner_intent_analysis_retainer_QA(message, modality, first_name)
            
            if inner_intent == "Other":
                initial_text =  constants.CR_OTHER_START
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_OTHER_START_AF_URL],
                    "Voice_URLs" : [constants.CR_OTHER_START_VF_URL],
                    "Additional_Questions" : "True"
                }
                log_user_request(session_id, message)
                res = new_logic(modality, session_id, first_name, dict)
            else:
                initial_text = result + constants.CR_GENERAL_START
                
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [Retainer_QA_URL_Dict[inner_intent], constants.CR_GENERAL_START_AF_URL],
                    "Voice_URLs" : [],
                    "Additional_Questions" : "True"
                }

                res = new_logic(modality, session_id, first_name, dict)
   
        elif analysis == "Payments":
            # if message in valid_payment_list:
            #     selected_payment = message
            # else:
            #     prompt = constants.CP_IS2_PAYMENTS_PROMPT
            #     selected_payment = intent_analysis_with_GPT(message, prompt)
            prompt = constants.CP_IS2_PAYMENTS_PROMPT
            selected_payment = intent_analysis_with_GPT(message, prompt)
            if selected_payment.startswith("'") and selected_payment.endswith("'"):
                # Remove the first and last character (the single quotes)
                selected_payment = selected_payment[1:-1]

            print("Selected Payment : ", selected_payment)
            if selected_payment == "7":
                initial_text = constants.CR_IS2_INVALID_NUM_PAYMENTS
                video_urls = [constants.CR_IS2_INVALID_NUM_PAYMENTS_AF_URL]
                audio_urls = [constants.CR_IS2_INVALID_NUM_PAYMENTS_AF_URL]
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : video_urls,
                    "Voice_URLs" : audio_urls,
                    "Additional_Questions" : "False"
                }
                res = new_logic(modality, session_id, first_name, dict)
                res["Bubbles"] = [payment_bubbles]

                
            else:
                print("Selected Payments : ", selected_payment)
                user_choices_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"Payments": selected_payment}}
                )
                
                initial_text =  constants.CR_IS2_PAYMENTS
                video_urls = [constants.CR_IS2_PAYMENTS_AF_URL]
                audio_urls = [constants.CR_IS2_PAYMENTS_VF_URL]
                
                next_needed_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"next_needed": "Displayed"}}
                )

                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : video_urls,
                    "Voice_URLs" : audio_urls,
                    "Additional_Questions" : "True"
                }

                res = new_logic(modality, session_id, first_name, dict)

                add_intent_id(session_id, '4')
                retainer_type = user_choices.get('Trust_Package')
                payment = user_choices.get('Payments')
                
                res['Retainer_Type'] = retainer_type
                res['Payment_Plan'] = selected_payment
                res['Send_retainer'] = 'True'
   
        return res
    except Exception as e:
        print(e)


def chat_flow_for_intent_section_4(message, chat_history, first_name, session_id, modality):
    print("\nWe are in chat_flow_for_intent_section_4\n")
    user_choices = user_choices_collection.find_one({"session_id": session_id})
    analysis = ''
    res = None
    system_prompt = constants.CP_IS4_SYSTEM_PROMPT
    try:
        if message == "I^":
            initiate_ai_collection = db.get_collection("initiate_ai")
            data = initiate_ai_collection.find_one({"session_id": session_id})
                
            initiate_ai_collection.update_one(
                {"session_id": session_id},
                {
                    "$set":{'User_Type' : "old",}
                },
                upsert=True
            )

            if data.get('User_Type') == 'New':
                initial_text = constants.CR_NEW_GREETING_MESSAGE
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_NEW_GREETING_MESSAGE_AF_URL],
                    "Voice_URLs" : [constants.CR_NEW_GREETING_MESSAGE_VF_URL],
                    "Additional_Questions" : "False"
                }
                res = new_logic(modality, session_id, first_name, dict)
                text = res["Text"] + " Or do you have some questions first?"
                res["Bubbles"] = [intent_section_1_bubbles]
                res["Text"] = text

            else:
                initial_text = constants.CR_OLD_GREETING_MESSAGE
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_OLD_GREETING_MESSAGE_AF_URL],
                    "Voice_URLs" : [constants.CR_OLD_GREETING_MESSAGE_VF_URL],
                    "Additional_Questions" : "True"
                }
                res = new_logic(modality, session_id, first_name, dict)
                res["Bubbles"] = [intent_section_1_bubbles]
               
        else:
            analysis = intent_analysis_with_GPT(message, system_prompt)
            updated_query = f"User message: {message}\n\n Chat History: {chat_history}"
            print(f"\n\n\nAnalysis : {analysis}")

        if analysis == "Greeting":
            initial_text, video_url, audio_url = handle_greetings(message)
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [video_url],
                "Voice_URLs" : [audio_url],
                "Additional_Questions" : "True"
            }
            res = new_logic(modality, session_id, first_name, dict)
                     
        elif analysis == "General":
            result, inner_intent = inner_intent_analysis_General_QA(message, modality, first_name)
            
            if inner_intent == "Other":
                initial_text =  constants.CR_OTHER_START
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_OTHER_START_AF_URL],
                    "Voice_URLs" : [constants.CR_OTHER_START_VF_URL],
                    "Additional_Questions" : "True"
                }
                log_user_request(session_id, message)
                res = new_logic(modality, session_id, first_name, dict)
            else:
                initial_text = result + constants.CR_GENERAL_START
                
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [General_QA_URL_Dict[inner_intent], constants.CR_GENERAL_START_AF_URL],
                    "Voice_URLs" : [],
                    "Additional_Questions" : "True"
                }

                res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "Retainer Q&A":
            result, inner_intent = inner_intent_analysis_retainer_QA(message, modality, first_name)
            
            if inner_intent == "Other":
                initial_text =  constants.CR_OTHER_START
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_OTHER_START_AF_URL],
                    "Voice_URLs" : [constants.CR_OTHER_START_VF_URL],
                    "Additional_Questions" : "True"
                }
                log_user_request(session_id, message)
                res = new_logic(modality, session_id, first_name, dict)
            else:
                initial_text = result + constants.CR_GENERAL_START
                
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [Retainer_QA_URL_Dict[inner_intent], constants.CR_GENERAL_START_AF_URL],
                    "Voice_URLs" : [],
                    "Additional_Questions" : "True"
                }

                res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "Transfer To Human":
            initial_text =  constants.CR_TRANSFER_TO_HUMAN
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [constants.CR_TRANSFER_TO_HUMAN_AF_URL],
                "Voice_URLs" : [],
                "Additional_Questions" : "False"
            }
            res = new_logic(modality, session_id, first_name, dict)
        
        elif analysis == "Positive":
            # prompt = """
            #     here is the list of tasks user need to do and in the same order:
            #     1) Purchase
            #     2) Package
            #     3) Numpayments
            #     4) Displayed
            #     5) Signature
            #     6) Paid
            #     7) Booking

            #     I will provide you user input and what was next needed so on the basis of user input you have to tell that what is next needed now. The thing is that if user message is only yes or done or something from which we can not tell that for what user is telling us then we will assume that user is replying for the current next needed and then you have to responde with next step name from the list above. For exmaple next needed = 'Displayed' and user message = yes or yes agreement is displayed. Then you have to responde with 'Signature' or if next needed = 'Signature' and user message = yes or yes i have done the signature. Then you have to responde with 'Paid', same is the case with booking.
            #     On the other hand if user message contains the information that i have done this or i have finished this task then you have to responde with next task from the list to that task. For example next needed = Purchase, but user message = 'I have signed the agreement' so from this message we know that user has signed and then you have to responde with 'Paid'. Make sure that you reply with the next word from the list to that task about which user is saying that he has done it only if user making a jump.

            #     Make sure that you only responde with the single word from these not anything else: 
            #     Purchase, Package, Numpayments, Displayed, Signature, Paid, Booking
            # """
            prompt = """
                here is the list of tasks user need to do and in the same order:
                1) Purchase
                2) Package
                3) Numpayments
                4) Displayed
                5) Signature
                6) Paid
                7) Booking

                You will be provided with user input and next needed so on the basis of user input you have to tell that what is next needed now. The thing is that if user message is only saying yes or done or something from which we can not tell that for what user is telling us then we will assume that user is replying for the current state and next needed will be the same and you have to return the same next needed which was provided you in user's prompt and if user is telling that i have done this task then you have to return whatever he has done as next needed.
                For Example:
                If user input is: 'Yes', next_needed is: 'Displayed' then you have to reply with same next needed 'Displayed'.
                if user input is: 'I have signed it or I have signed the agreement', next_needed is: 'Signed' then you have to reply with same next needed 'Signed'.
                If user input is: 'I have done the payment', next_needed is: 'Signature'. So from user message we can easily see that user has skipped a step so you should return 'Paid' which is what user has done.

                So basically if you get a clear picture from the user messsage that what he has done you will return what he has done from the list other wise return the same next_needed user provide you in his input.

                Make sure that you only responde with the single word from these not anything else: 
                Purchase, Package, Numpayments, Displayed, Signature, Paid, Booking
            """
            
    
            next = next_needed_collection.find_one({"session_id": session_id})
            next_needed = next.get("next_needed")
            print("Next needed : ", next_needed)
            updated_query = f"next needed = {next_needed} and user input = {message}"
            next_needed = intent_analysis_with_GPT(updated_query, prompt)
            print("Gpt suggested next needed = ", next_needed)
            
            if next_needed == 'Displayed':
                next_needed_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"next_needed": "Signature"}}
                )
                initial_text =  constants.CR_IS4_AGREEMENT_DISPLAYED
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_IS4_AGREEMENT_DISPLAYED_AF_URL],
                    "Voice_URLs" : [constants.CR_IS4_AGREEMENT_DISPLAYED_VF_URL],
                    "Additional_Questions" : "True"
                }
                res = new_logic(modality, session_id, first_name, dict)
            
            elif next_needed == 'Signature':
                next_needed_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"next_needed": "Paid"}}
                )
                initial_text =  constants.CR_IS4_AGREEMENT_SIGNATURE_DONE
                
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_IS4_AGREEMENT_SIGNATURE_DONE_AF_URL],
                    "Voice_URLs" : [constants.CR_IS4_AGREEMENT_SIGNATURE_DONE_VF_URL],
                    "Additional_Questions" : "True"
                }
                
                res = new_logic(modality, session_id, first_name, dict)

            elif next_needed == 'Paid':
                next_needed_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"next_needed": "Booking"}}
                )
                initial_text =  constants.CR_IS4_AGREEMENT_PAID  
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_IS4_AGREEMENT_PAID_AF_URL],
                    "Voice_URLs" : [constants.CR_IS4_AGREEMENT_PAID_VF_URL],
                    "Additional_Questions" : "True"
                }
                res = new_logic(modality, session_id, first_name, dict)
                res["Send_Booking_Calendar"] = 'os'

            elif next_needed == 'Booking':
                next_needed_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"next_needed": "Completed"}}
                )
                initial_text =  constants.CR_IS4_BOOKING_COMPLETED  
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_IS4_BOOKING_COMPLETED_AF_URL],
                    "Voice_URLs" : [constants.CR_IS4_BOOKING_COMPLETED_VF_URL],
                    "Additional_Questions" : "True"
                }
                res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "Negative":
            initial_text =  constants.CR_NEGATIVE_MESSAGE
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [],
                "Voice_URLs" : [],
                "Additional_Questions" : "False"
            }
            res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "More Question":
            initial_text =  constants.CR_MORE_QUESTIONS
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [],
                "Voice_URLs" : [],
                "Additional_Questions" : "False"
            }
            res = new_logic(modality, session_id, first_name, dict)
        
        elif analysis == "Issue with Task":
            ISSUE_WITH_TASK_PROMPT = """You have to see and tell that user is having issue with his retainer, payment, invoice, booking calender or not receiving any of these.
            user can write a text like i did not got the booking link. or payment is not getting done. or i am facing an issue while make a reservation or booking or call.
            User might tell in a indirect way so you have to handle that smartly and tell that what we need to send again to help user getting fixed the problem. We can resend 2 things only.
            - Booking Calender
            - Retainer Agreement 
            The sequence is that user first tell us his coice for the trust package, then he tells us payment plan he wants and then we send the retainer agreement, then user signs the agreement and receieves an invoice, once user do the payment and inform we will send a booking link so that user can book the appointment.
            If user mentions that he is having issue at any of these points then you have to reply with just the name of the step.
            -> Trust Package
            -> Payments
            -> Retainer Agreement
            -> Invoice
            -> Booking
            You have to reply with just the option you think is best fit from the above list.
            """
            analysis = intent_analysis_with_GPT(message, ISSUE_WITH_TASK_PROMPT)
            if analysis == "Trust Package":
                initial_text =  constants.CR_IS4_TASK_ISSUE
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_IS4_TASK_ISSUE_AF_URL],
                    "Voice_URLs" : [constants.CR_IS4_TASK_ISSUE_VF_URL],
                    "Additional_Questions" : "True"
                }
                res = new_logic(modality, session_id, first_name, dict)
            
            elif analysis == "Payments":
                initial_text =  constants.CR_IS4_TASK_ISSUE
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_IS4_TASK_ISSUE_AF_URL],
                    "Voice_URLs" : [constants.CR_IS4_TASK_ISSUE_VF_URL],
                    "Additional_Questions" : "True"
                }
                res = new_logic(modality, session_id, first_name, dict)
            
            elif analysis == "Retainer Agreement":
                initial_text =  constants.CR_IS4_TASK_ISSUE
                next_needed_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"next_needed": "Displayed"}}
                )
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_IS4_TASK_ISSUE_AF_URL],
                    "Voice_URLs" : [constants.CR_IS4_TASK_ISSUE_VF_URL],
                    "Additional_Questions" : "True"
                }
                res = new_logic(modality, session_id, first_name, dict)
                retainer_type = user_choices.get('Trust_Package')
                payment_plan = user_choices.get('Payments')
                res['Retainer_Type'] = selected_trust
                res['Payment_Plan'] = payment_plan
                res['Send_retainer'] = 'True'
                    
            elif analysis == "Invoice":
                initial_text =  "I am so sorry to hear that you are facing this issue with your invoice. I am sending you a new retainer agreement, please sign the agreement and get the invoice again. Thanks!"
                next_needed_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"next_needed": "Displayed"}}
                )
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_IS4_TASK_ISSUE_AF_URL],
                    "Voice_URLs" : [constants.CR_IS4_TASK_ISSUE_VF_URL],
                    "Additional_Questions" : "True"
                }
                res = new_logic(modality, session_id, first_name, dict)
                retainer_type = user_choices.get('Trust_Package')
                payment_plan = user_choices.get('Payments')
                res['Retainer_Type'] = selected_trust
                res['Payment_Plan'] = payment_plan
                res['Send_retainer'] = 'True'

            elif analysis == "Booking":
                initial_text =  "I am so sorry to hear that you are facing this issue with booking link. I am emailing you the booking link again. Please check you inbox or spam. Thanks!"
                next_needed_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"next_needed": "Booking"}}
                )
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_IS4_TASK_ISSUE_AF_URL],
                    "Voice_URLs" : [constants.CR_IS4_TASK_ISSUE_VF_URL],
                    "Additional_Questions" : "True"
                }
                res = new_logic(modality, session_id, first_name, dict)
                res["Send_Booking_Calendar"] = 'os'

            else:
                initial_text =  constants.CR_IS4_TASK_ISSUE    
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_IS4_TASK_ISSUE_AF_URL],
                    "Voice_URLs" : [constants.CR_IS4_TASK_ISSUE_VF_URL],
                    "Additional_Questions" : "True"
                }
                res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "Objection":
            result, inner_intent = inner_intent_analysis_objection_QA(message, modality, first_name)
            
            if inner_intent == "Other":
                initial_text =  constants.CR_OTHER_START
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_OTHER_START_AF_URL],
                    "Voice_URLs" : [constants.CR_OTHER_START_VF_URL],
                    "Additional_Questions" : "True"
                }
                log_user_request(session_id, message)
                res = new_logic(modality, session_id, first_name, dict)
            else:
                initial_text = result + constants.CR_GENERAL_START
                
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [Objection_QA_URL_Dict[inner_intent], constants.CR_GENERAL_START_AF_URL],
                    "Voice_URLs" : [],
                    "Additional_Questions" : "True"
                }

                res = new_logic(modality, session_id, first_name, dict)
        
        elif analysis == "Change Trust Package":
            if message in ["1", "2"]:
                selected_trust = intent_section_2_bubbles[message]
            else:
                prompt = constants.CP_IS2_TRUST_PACKAGE_PROMPT
                selected_trust = intent_analysis_with_GPT(message, prompt)

            user_choices_collection.update_one(
                {"session_id": session_id},
                {"$set": {"Trust_Package": selected_trust}}
            )
            
            initial_text = constants.CR_IS4_CHANGE_TRUST_PACKAGE
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [constants.CR_IS4_CHANGE_TRUST_PACKAGE_AF_URL],
                "Voice_URLs" : [constants.CR_IS4_CHANGE_TRUST_PACKAGE_VF_URL],
                "Additional_Questions" : "True"
            }
            res = new_logic(modality, session_id, first_name, dict)
            #retainer_type = user_choices.get('Trust_Package')
            payment_plan = user_choices.get('Payments')
            
            res['Retainer_Type'] = selected_trust
            res['Payment_Plan'] = payment_plan
            res['Send_retainer'] = 'True'

        elif analysis == "Change Payment Plan":
            if message in ["1", "2", "3", "4", "5", "6"]:
                selected_payment = message
            else:
                prompt = constants.CP_IS2_PAYMENTS_PROMPT
                selected_payment = intent_analysis_with_GPT(message, prompt)
    
            if selected_payment == "7":
                initial_text = constants.CR_IS2_INVALID_NUM_PAYMENTS
                video_urls = [constants.CR_IS2_INVALID_NUM_PAYMENTS_AF_URL]
                audio_urls = [constants.CR_IS2_INVALID_NUM_PAYMENTS_AF_URL]
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : video_urls,
                    "Voice_URLs" : audio_urls,
                    "Additional_Questions" : "False"
                }
                next_needed_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"next_needed": "Numpayments"}}
                )
                res = new_logic(modality, session_id, first_name, dict)
                res["Bubbles"] = [payment_bubbles]
                next_needed_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"next_needed": "Displayed"}}
                )
            else:
                initial_text = constants.CR_IS4_CHANGE_PAYMENT_PLAN
                dict = {
                    "Texts" : [initial_text],
                    "Avatar_URLs" : [constants.CR_IS4_CHANGE_PAYMENT_PLAN_AF_URL],
                    "Voice_URLs" : [constants.CR_IS4_CHANGE_PAYMENT_PLAN_VF_URL],
                    "Additional_Questions" : "False"
                }
                res = new_logic(modality, session_id, first_name, dict)
                retainer_type = user_choices.get('Trust_Package')
                #payment_plan = user_choices.get('Payments')
                
                res['Retainer_Type'] = retainer_type
                res['Payment_Plan'] = selected_payment
                res['Send_retainer'] = 'True'

        elif analysis == 'Change Other Info':
            initial_text = constants.CR_IS4_CHANGE_OTHER_INFO_START
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [constants.CR_IS4_CHANGE_OTHER_INFO_START_AF_URL],
                "Voice_URLs" : [constants.CR_IS4_CHANGE_OTHER_INFO_START_VF_URL],
                "Additional_Questions" : "True"
            }
            res = new_logic(modality, session_id, first_name, dict)

        elif analysis == "Other":
            initial_text =  constants.CR_OTHER_START
            dict = {
                "Texts" : [initial_text],
                "Avatar_URLs" : [constants.CR_OTHER_START_AF_URL],
                "Voice_URLs" : [constants.CR_OTHER_START_VF_URL],
                "Additional_Questions" : "True"
            }

            res = new_logic(modality, session_id, first_name, dict)

        return res
    except Exception as e:
        print(e)
