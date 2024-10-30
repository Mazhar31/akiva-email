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

# Get the constants collection
Constants_Collection = db.get_collection("constants")
variable_name = "CR_OLD_GREETING_MESSAGE_AF_URL"
updated_value = "https://storage.googleapis.com/msgsndr/HdpmQEFcOyjCw9DFaIyF/media/66f5f0099d49bd2520928f27.mp4"
Constants_Collection.update_one(
    {"variable_name": variable_name},
    {"$set": {"value": updated_value}}
)


# # Fetching CP_PREAMBLE
# preamble = Constants_Collection.find_one({"variable_name": "CP_PREAMBLE"})
# CP_PREAMBLE = preamble['value']

# # Fetching CP_TASK
# cptask = Constants_Collection.find_one({"variable_name": "CP_TASK"})
# CP_TASK = cptask['value']

# # Fetching CP_GREETING
# cpgreetings = Constants_Collection.find_one({"variable_name": "CP_GREETING"})
# CP_GREETING = cpgreetings['value']

# # Fetching CP_GENERAL
# cp_general = Constants_Collection.find_one({"variable_name": "CP_GENERAL"})
# CP_GENERAL = cp_general['value']

# # Fetching CP_TRANSFER_TO_HUMAN
# cp_transfer_to_human = Constants_Collection.find_one({"variable_name": "CP_TRANSFER_TO_HUMAN"})
# CP_TRANSFER_TO_HUMAN = cp_transfer_to_human['value']

# # Fetching CP_OBJECTION
# cp_objection = Constants_Collection.find_one({"variable_name": "CP_OBJECTION"})
# CP_OBJECTION = cp_objection['value']

# # Fetching CP_OTHER
# cp_other = Constants_Collection.find_one({"variable_name": "CP_OTHER"})
# CP_OTHER = cp_other['value']

# # Fetching CR_OTHER_START
# cr_other_start = Constants_Collection.find_one({"variable_name": "CR_OTHER_START"})
# CR_OTHER_START = cr_other_start['value']

# # Fetching CR_OTHER_START_AF_URL
# cr_other_start_af_url = Constants_Collection.find_one({"variable_name": "CR_OTHER_START_AF_URL"})
# CR_OTHER_START_AF_URL = cr_other_start_af_url['value']

# # Fetching CR_OTHER_START_VF_URL
# cr_other_start_vf_url = Constants_Collection.find_one({"variable_name": "CR_OTHER_START_VF_URL"})
# CR_OTHER_START_VF_URL = cr_other_start_vf_url['value']

# # Fetching CR_GENERAL_START
# cr_general_start = Constants_Collection.find_one({"variable_name": "CR_GENERAL_START"})
# CR_GENERAL_START = cr_general_start['value']

# # Fetching CR_GENERAL_START_AF_URL
# cr_general_start_af_url = Constants_Collection.find_one({"variable_name": "CR_GENERAL_START_AF_URL"})
# CR_GENERAL_START_AF_URL = cr_general_start_af_url['value']

# # Fetching CR_GENERAL_START_VF_URL
# cr_general_start_vf_url = Constants_Collection.find_one({"variable_name": "CR_GENERAL_START_VF_URL"})
# CR_GENERAL_START_VF_URL = cr_general_start_vf_url['value']

# # Fetching CR_PURCHASE_NEEDED
# cr_purchase_needed = Constants_Collection.find_one({"variable_name": "CR_PURCHASE_NEEDED"})
# CR_PURCHASE_NEEDED = cr_purchase_needed['value']

# # Fetching CR_PURCHASE_NEEDED_AF_URL
# cr_purchase_needed_af_url = Constants_Collection.find_one({"variable_name": "CR_PURCHASE_NEEDED_AF_URL"})
# CR_PURCHASE_NEEDED_AF_URL = cr_purchase_needed_af_url['value']

# # Fetching CR_PURCHASE_NEEDED_VF_URL
# cr_purchase_needed_vf_url = Constants_Collection.find_one({"variable_name": "CR_PURCHASE_NEEDED_VF_URL"})
# CR_PURCHASE_NEEDED_VF_URL = cr_purchase_needed_vf_url['value']

# # Fetching CR_PACKAGE_NEEDED
# cr_package_needed = Constants_Collection.find_one({"variable_name": "CR_PACKAGE_NEEDED"})
# CR_PACKAGE_NEEDED = cr_package_needed['value']

# # Fetching CR_PACKAGE_NEEDED_AF_URL
# cr_package_needed_af_url = Constants_Collection.find_one({"variable_name": "CR_PACKAGE_NEEDED_AF_URL"})
# CR_PACKAGE_NEEDED_AF_URL = cr_package_needed_af_url['value']

# # Fetching CR_PACKAGE_NEEDED_VF_URL
# cr_package_needed_vf_url = Constants_Collection.find_one({"variable_name": "CR_PACKAGE_NEEDED_VF_URL"})
# CR_PACKAGE_NEEDED_VF_URL = cr_package_needed_vf_url['value']

# # Fetching CR_NUMPAYMENTS_NEEDED
# cr_numpayments_needed = Constants_Collection.find_one({"variable_name": "CR_NUMPAYMENTS_NEEDED"})
# CR_NUMPAYMENTS_NEEDED = cr_numpayments_needed['value']

# # Fetching CR_NUMPAYMENTS_NEEDED_AF_URL
# cr_numpayments_needed_af_url = Constants_Collection.find_one({"variable_name": "CR_NUMPAYMENTS_NEEDED_AF_URL"})
# CR_NUMPAYMENTS_NEEDED_AF_URL = cr_numpayments_needed_af_url['value']

# # Fetching CR_NUMPAYMENTS_NEEDED_VF_URL
# cr_numpayments_needed_vf_url = Constants_Collection.find_one({"variable_name": "CR_NUMPAYMENTS_NEEDED_VF_URL"})
# CR_NUMPAYMENTS_NEEDED_VF_URL = cr_numpayments_needed_vf_url['value']

# # Fetching CR_DISPLAY_NEEDED
# cr_display_needed = Constants_Collection.find_one({"variable_name": "CR_DISPLAY_NEEDED"})
# CR_DISPLAY_NEEDED = cr_display_needed['value']

# # Fetching CR_DISPLAY_NEEDED_AF_URL
# cr_display_needed_af_url = Constants_Collection.find_one({"variable_name": "CR_DISPLAY_NEEDED_AF_URL"})
# CR_DISPLAY_NEEDED_AF_URL = cr_display_needed_af_url['value']

# # Fetching CR_DISPLAY_NEEDED_VF_URL
# cr_display_needed_vf_url = Constants_Collection.find_one({"variable_name": "CR_DISPLAY_NEEDED_VF_URL"})
# CR_DISPLAY_NEEDED_VF_URL = cr_display_needed_vf_url['value']

# # Fetching CR_SIGNATURE_NEEDED
# cr_signature_needed = Constants_Collection.find_one({"variable_name": "CR_SIGNATURE_NEEDED"})
# CR_SIGNATURE_NEEDED = cr_signature_needed['value']

# # Fetching CR_SIGNATURE_NEEDED_AF_URL
# cr_signature_needed_af_url = Constants_Collection.find_one({"variable_name": "CR_SIGNATURE_NEEDED_AF_URL"})
# CR_SIGNATURE_NEEDED_AF_URL = cr_signature_needed_af_url['value']

# # Fetching CR_SIGNATURE_NEEDED_VF_URL
# cr_signature_needed_vf_url = Constants_Collection.find_one({"variable_name": "CR_SIGNATURE_NEEDED_VF_URL"})
# CR_SIGNATURE_NEEDED_VF_URL = cr_signature_needed_vf_url['value']

# # Fetching CR_PAYMENT_NEEDED
# cr_payment_needed = Constants_Collection.find_one({"variable_name": "CR_PAYMENT_NEEDED"})
# CR_PAYMENT_NEEDED = cr_payment_needed['value']

# # Fetching CR_PAYMENT_NEEDED_AF_URL
# cr_payment_needed_af_url = Constants_Collection.find_one({"variable_name": "CR_PAYMENT_NEEDED_AF_URL"})
# CR_PAYMENT_NEEDED_AF_URL = cr_payment_needed_af_url['value']

# # Fetching CR_PAYMENT_NEEDED_VF_URL
# cr_payment_needed_vf_url = Constants_Collection.find_one({"variable_name": "CR_PAYMENT_NEEDED_VF_URL"})
# CR_PAYMENT_NEEDED_VF_URL = cr_payment_needed_vf_url['value']

# # Fetching CR_BOOKING_NEEDED
# cr_booking_needed = Constants_Collection.find_one({"variable_name": "CR_BOOKING_NEEDED"})
# CR_BOOKING_NEEDED = cr_booking_needed['value']

# # Fetching CR_BOOKING_NEEDED_AF_URL
# cr_booking_needed_af_url = Constants_Collection.find_one({"variable_name": "CR_BOOKING_NEEDED_AF_URL"})
# CR_BOOKING_NEEDED_AF_URL = cr_booking_needed_af_url['value']

# # Fetching CR_BOOKING_NEEDED_VF_URL
# cr_booking_needed_vf_url = Constants_Collection.find_one({"variable_name": "CR_BOOKING_NEEDED_VF_URL"})
# CR_BOOKING_NEEDED_VF_URL = cr_booking_needed_vf_url['value']

# # Fetching CR_COMPLETED
# cr_completed = Constants_Collection.find_one({"variable_name": "CR_COMPLETED"})
# CR_COMPLETED = cr_completed['value']

# # Fetching CR_COMPLETED_AF_URL
# cr_completed_af_url = Constants_Collection.find_one({"variable_name": "CR_COMPLETED_AF_URL"})
# CR_COMPLETED_AF_URL = cr_completed_af_url['value']

# # Fetching CR_COMPLETED_VF_URL
# cr_completed_vf_url = Constants_Collection.find_one({"variable_name": "CR_COMPLETED_VF_URL"})
# CR_COMPLETED_VF_URL = cr_completed_vf_url['value']

# # Fetching CR_ADDITIONAL_QUESTIONS
# cr_additional_questions = Constants_Collection.find_one({"variable_name": "CR_ADDITIONAL_QUESTIONS"})
# CR_ADDITIONAL_QUESTIONS = cr_additional_questions['value']

# # Fetching CR_ADDITIONAL_QUESTIONS_AF_URL
# cr_additional_questions_af_url = Constants_Collection.find_one({"variable_name": "CR_ADDITIONAL_QUESTIONS_AF_URL"})
# CR_ADDITIONAL_QUESTIONS_AF_URL = cr_additional_questions_af_url['value']

# # Fetching CR_ADDITIONAL_QUESTIONS_VF_URL
# cr_additional_questions_vf_url = Constants_Collection.find_one({"variable_name": "CR_ADDITIONAL_QUESTIONS_VF_URL"})
# CR_ADDITIONAL_QUESTIONS_VF_URL = cr_additional_questions_vf_url['value']


# # Fetching CR_TRANSFER_TO_HUMAN
# cr_transfer_to_human = Constants_Collection.find_one({"variable_name": "CR_TRANSFER_TO_HUMAN"})
# CR_TRANSFER_TO_HUMAN = cr_transfer_to_human['value']

# # Fetching CR_TRANSFER_TO_HUMAN_AF_URL
# cr_transfer_to_human_af_url = Constants_Collection.find_one({"variable_name": "CR_TRANSFER_TO_HUMAN_AF_URL"})
# CR_TRANSFER_TO_HUMAN_AF_URL = cr_transfer_to_human_af_url['value']

# # Fetching CR_TRANSFER_TO_HUMAN_VF_URL
# cr_transfer_to_human_vf_url = Constants_Collection.find_one({"variable_name": "CR_TRANSFER_TO_HUMAN_VF_URL"})
# CR_TRANSFER_TO_HUMAN_VF_URL = cr_transfer_to_human_vf_url['value']

# # Fetching CR_NEW_GREETING_MESSAGE
# cr_new_greeting_message = Constants_Collection.find_one({"variable_name": "CR_NEW_GREETING_MESSAGE"})
# CR_NEW_GREETING_MESSAGE = cr_new_greeting_message['value']

# # Fetching CR_NEW_GREETING_MESSAGE_AF_URL
# cr_new_greeting_message_af_url = Constants_Collection.find_one({"variable_name": "CR_NEW_GREETING_MESSAGE_AF_URL"})
# CR_NEW_GREETING_MESSAGE_AF_URL = cr_new_greeting_message_af_url['value']

# # Fetching CR_NEW_GREETING_MESSAGE_VF_URL
# cr_new_greeting_message_vf_url = Constants_Collection.find_one({"variable_name": "CR_NEW_GREETING_MESSAGE_VF_URL"})
# CR_NEW_GREETING_MESSAGE_VF_URL = cr_new_greeting_message_vf_url['value']

# # Fetching CR_OLD_GREETING_MESSAGE
# cr_old_greeting_message = Constants_Collection.find_one({"variable_name": "CR_OLD_GREETING_MESSAGE"})
# CR_OLD_GREETING_MESSAGE = cr_old_greeting_message['value']

# # Fetching CR_OLD_GREETING_MESSAGE_AF_URL
# cr_old_greeting_message_af_url = Constants_Collection.find_one({"variable_name": "CR_OLD_GREETING_MESSAGE_AF_URL"})
# CR_OLD_GREETING_MESSAGE_AF_URL = cr_old_greeting_message_af_url['value']

# # Fetching CR_OLD_GREETING_MESSAGE_VF_URL
# cr_old_greeting_message_vf_url = Constants_Collection.find_one({"variable_name": "CR_OLD_GREETING_MESSAGE_VF_URL"})
# CR_OLD_GREETING_MESSAGE_VF_URL = cr_old_greeting_message_vf_url['value']

# # Fetching CP_COMMAND_AND_CONTROL
# cp_command_and_control = Constants_Collection.find_one({"variable_name": "CP_COMMAND_AND_CONTROL"})
# CP_COMMAND_AND_CONTROL = cp_command_and_control['value']

# # Fetching CP_IS1_SYSTEM_PROMPT
# cp_is1_system_prompt = Constants_Collection.find_one({"variable_name": "CP_IS1_SYSTEM_PROMPT"})
# CP_IS1_SYSTEM_PROMPT = cp_is1_system_prompt['value']

# # Fetching CR_IS1_PURCHASE
# cr_is1_purchase = Constants_Collection.find_one({"variable_name": "CR_IS1_PURCHASE"})
# CR_IS1_PURCHASE = cr_is1_purchase['value']

# # Fetching CR_IS1_PURCHASE_AF_URL
# cr_is1_purchase_af_url = Constants_Collection.find_one({"variable_name": "CR_IS1_PURCHASE_AF_URL"})
# CR_IS1_PURCHASE_AF_URL = cr_is1_purchase_af_url['value']

# # Fetching CR_IS1_PURCHASE_VF_URL
# cr_is1_purchase_vf_url = Constants_Collection.find_one({"variable_name": "CR_IS1_PURCHASE_VF_URL"})
# CR_IS1_PURCHASE_VF_URL = cr_is1_purchase_vf_url['value']

# # Fetching CP_IS2_SYSTEM_PROMPT
# cp_is2_system_prompt = Constants_Collection.find_one({"variable_name": "CP_IS2_SYSTEM_PROMPT"})
# CP_IS2_SYSTEM_PROMPT = cp_is2_system_prompt[f'value']

# # Fetching CP_IS2_TRUST_PACKAGE_PROMPT
# cp_is2_trust_package_prompt = Constants_Collection.find_one({"variable_name": "CP_IS2_TRUST_PACKAGE_PROMPT"})
# CP_IS2_TRUST_PACKAGE_PROMPT = cp_is2_trust_package_prompt['value']

# # Fetching CR_IS2_TRUST_PACKAGE
# cr_is2_trust_package = Constants_Collection.find_one({"variable_name": "CR_IS2_TRUST_PACKAGE"})
# CR_IS2_TRUST_PACKAGE = cr_is2_trust_package['value']

# # Fetching CR_IS2_TRUST_PACKAGE_AF_URL
# cr_is2_trust_package_af_url = Constants_Collection.find_one({"variable_name": "CR_IS2_TRUST_PACKAGE_AF_URL"})
# CR_IS2_TRUST_PACKAGE_AF_URL = cr_is2_trust_package_af_url['value']

# # Fetching CR_IS2_TRUST_PACKAGE_VF_URL
# cr_is2_trust_package_vf_url = Constants_Collection.find_one({"variable_name": "CR_IS2_TRUST_PACKAGE_VF_URL"})
# CR_IS2_TRUST_PACKAGE_VF_URL = cr_is2_trust_package_vf_url['value']

# # Fetching CP_IS2_PAYMENTS_PROMPT
# cp_is2_payments_prompt = Constants_Collection.find_one({"variable_name": "CP_IS2_PAYMENTS_PROMPT"})
# CP_IS2_PAYMENTS_PROMPT = cp_is2_payments_prompt['value']

# # Fetching CR_IS2_PAYMENTS
# cr_is2_payments = Constants_Collection.find_one({"variable_name": "CR_IS2_PAYMENTS"})
# CR_IS2_PAYMENTS = cr_is2_payments['value']

# # Fetching CR_IS2_PAYMENTS_AF_URL
# cr_is2_payments_af_url = Constants_Collection.find_one({"variable_name": "CR_IS2_PAYMENTS_AF_URL"})
# CR_IS2_PAYMENTS_AF_URL = cr_is2_payments_af_url['value']

# # Fetching CR_IS2_PAYMENTS_VF_URL
# cr_is2_payments_vf_url = Constants_Collection.find_one({"variable_name": "CR_IS2_PAYMENTS_VF_URL"})
# CR_IS2_PAYMENTS_VF_URL = cr_is2_payments_vf_url['value']

# # Fetching CR_IS2_INVALID_NUM_PAYMENTS
# cr_is2_invalid_num_payments = Constants_Collection.find_one({"variable_name": "CR_IS2_INVALID_NUM_PAYMENTS"})
# CR_IS2_INVALID_NUM_PAYMENTS = cr_is2_invalid_num_payments['value']

# # Fetching CR_IS2_INVALID_NUM_PAYMENTS_AF_URL
# cr_is2_invalid_num_payments_af_url = Constants_Collection.find_one({"variable_name": "CR_IS2_INVALID_NUM_PAYMENTS_AF_URL"})
# CR_IS2_INVALID_NUM_PAYMENTS_AF_URL = cr_is2_invalid_num_payments_af_url['value']

# # Fetching CR_IS2_INVALID_NUM_PAYMENTS_VF_URL
# cr_is2_invalid_num_payments_vf_url = Constants_Collection.find_one({"variable_name": "CR_IS2_INVALID_NUM_PAYMENTS_VF_URL"})
# CR_IS2_INVALID_NUM_PAYMENTS_VF_URL = cr_is2_invalid_num_payments_vf_url['value']

# #set next_needed ="displayed"


# # Fetching CP_IS4_SYSTEM_PROMPT
# is4_systemprompt = Constants_Collection.find_one({"variable_name": "CP_IS4_SYSTEM_PROMPT"})
# CP_IS4_SYSTEM_PROMPT = is4_systemprompt['value']

# # Fetching CR_IS4_TASK_ISSUE
# task_issue = Constants_Collection.find_one({"variable_name": "CR_IS4_TASK_ISSUE"})
# CR_IS4_TASK_ISSUE = task_issue['value']

# # Fetching CR_IS4_TASK_ISSUE_AF_URL
# task_issue_af_url = Constants_Collection.find_one({"variable_name": "CR_IS4_TASK_ISSUE_AF_URL"})
# CR_IS4_TASK_ISSUE_AF_URL = task_issue_af_url['value']

# # Fetching CR_IS4_TASK_ISSUE_VF_URL
# task_issue_vf_url = Constants_Collection.find_one({"variable_name": "CR_IS4_TASK_ISSUE_VF_URL"})
# CR_IS4_TASK_ISSUE_VF_URL = task_issue_vf_url['value']

# # Fetching CR_IS4_AGREEMENT_DISPLAYED
# agreement_displayed = Constants_Collection.find_one({"variable_name": "CR_IS4_AGREEMENT_DISPLAYED"})
# CR_IS4_AGREEMENT_DISPLAYED = agreement_displayed['value']

# # Fetching CR_IS4_AGREEMENT_DISPLAYED_AF_URL
# agreement_displayed_af_url = Constants_Collection.find_one({"variable_name": "CR_IS4_AGREEMENT_DISPLAYED_AF_URL"})
# CR_IS4_AGREEMENT_DISPLAYED_AF_URL = agreement_displayed_af_url['value']

# # Fetching CR_IS4_AGREEMENT_DISPLAYED_VF_URL
# agreement_displayed_vf_url = Constants_Collection.find_one({"variable_name": "CR_IS4_AGREEMENT_DISPLAYED_VF_URL"})
# CR_IS4_AGREEMENT_DISPLAYED_VF_URL = agreement_displayed_vf_url['value']
# # set next_needed = "signature"

# # Fetching CR_IS4_AGREEMENT_SIGNATURE_DONE
# agreement_signature_done = Constants_Collection.find_one({"variable_name": "CR_IS4_AGREEMENT_SIGNATURE_DONE"})
# CR_IS4_AGREEMENT_SIGNATURE_DONE = agreement_signature_done['value']

# # Fetching CR_IS4_AGREEMENT_SIGNATURE_DONE_AF_URL
# agreement_signature_done_af_url = Constants_Collection.find_one({"variable_name": "CR_IS4_AGREEMENT_SIGNATURE_DONE_AF_URL"})
# CR_IS4_AGREEMENT_SIGNATURE_DONE_AF_URL = agreement_signature_done_af_url['value']

# # Fetching CR_IS4_AGREEMENT_SIGNATURE_DONE_VF_URL
# agreement_signature_done_vf_url = Constants_Collection.find_one({"variable_name": "CR_IS4_AGREEMENT_SIGNATURE_DONE_VF_URL"})
# CR_IS4_AGREEMENT_SIGNATURE_DONE_VF_URL = agreement_signature_done_vf_url['value']
# # set next_needed = "paid"

# # Fetching CR_IS4_AGREEMENT_PAID
# agreement_paid = Constants_Collection.find_one({"variable_name": "CR_IS4_AGREEMENT_PAID"})
# CR_IS4_AGREEMENT_PAID = agreement_paid['value']

# # Fetching CR_IS4_AGREEMENT_PAID_AF_URL
# agreement_paid_af_url = Constants_Collection.find_one({"variable_name": "CR_IS4_AGREEMENT_PAID_AF_URL"})
# CR_IS4_AGREEMENT_PAID_AF_URL = agreement_paid_af_url['value']

# # Fetching CR_IS4_AGREEMENT_PAID_VF_URL
# agreement_paid_vf_url = Constants_Collection.find_one({"variable_name": "CR_IS4_AGREEMENT_PAID_VF_URL"})
# CR_IS4_AGREEMENT_PAID_VF_URL = agreement_paid_vf_url['value']
# # set next_needed = "booking"

# # Fetching CR_IS4_OS_BOOKING_DONE
# os_booking_done = Constants_Collection.find_one({"variable_name": "CR_IS4_OS_BOOKING_DONE"})
# CR_IS4_OS_BOOKING_DONE = os_booking_done['value']

# # Fetching CR_IS4_OS_BOOKING_DONE_AF_URL
# os_booking_done_af_url = Constants_Collection.find_one({"variable_name": "CR_IS4_OS_BOOKING_DONE_AF_URL"})
# CR_IS4_OS_BOOKING_DONE_AF_URL = os_booking_done_af_url['value']

# # Fetching CR_IS4_OS_BOOKING_DONE_VF_URL
# os_booking_done_vf_url = Constants_Collection.find_one({"variable_name": "CR_IS4_OS_BOOKING_DONE_VF_URL"})
# CR_IS4_OS_BOOKING_DONE_VF_URL = os_booking_done_vf_url['value']
# # set next_needed = "completed"

# # Fetching CR_IS4_BOOKING_COMPLETED
# booking_completed = Constants_Collection.find_one({"variable_name": "CR_IS4_BOOKING_COMPLETED"})
# CR_IS4_BOOKING_COMPLETED = booking_completed['value']

# # Fetching CR_IS4_BOOKING_COMPLETED_AF_URL
# booking_completed_af_url = Constants_Collection.find_one({"variable_name": "CR_IS4_BOOKING_COMPLETED_AF_URL"})
# CR_IS4_BOOKING_COMPLETED_AF_URL = booking_completed_af_url['value']

# # Fetching CR_IS4_BOOKING_COMPLETED_VF_URL
# booking_completed_vf_url = Constants_Collection.find_one({"variable_name": "CR_IS4_BOOKING_COMPLETED_VF_URL"})
# CR_IS4_BOOKING_COMPLETED_VF_URL = booking_completed_vf_url['value']

# # Fetching CR_IS4_CHANGE_TRUST_PACKAGE
# change_trust_package = Constants_Collection.find_one({"variable_name": "CR_IS4_CHANGE_TRUST_PACKAGE"})
# CR_IS4_CHANGE_TRUST_PACKAGE = change_trust_package['value']

# # Fetching CR_IS4_CHANGE_TRUST_PACKAGE_AF_URL
# change_trust_package_af_url = Constants_Collection.find_one({"variable_name": "CR_IS4_CHANGE_TRUST_PACKAGE_AF_URL"})
# CR_IS4_CHANGE_TRUST_PACKAGE_AF_URL = change_trust_package_af_url['value']

# # Fetching CR_IS4_CHANGE_TRUST_PACKAGE_VF_URL
# change_trust_package_vf_url = Constants_Collection.find_one({"variable_name": "CR_IS4_CHANGE_TRUST_PACKAGE_VF_URL"})
# CR_IS4_CHANGE_TRUST_PACKAGE_VF_URL = change_trust_package_vf_url['value']
# # set next_needed = "package"
# # send to IS2

# # Fetching CR_IS4_CHANGE_PAYMENT_PLAN
# change_payment_plan = Constants_Collection.find_one({"variable_name": "CR_IS4_CHANGE_PAYMENT_PLAN"})
# CR_IS4_CHANGE_PAYMENT_PLAN = change_payment_plan['value']

# # Fetching CR_IS4_CHANGE_PAYMENT_PLAN_AF_URL
# change_payment_plan_af_url = Constants_Collection.find_one({"variable_name": "CR_IS4_CHANGE_PAYMENT_PLAN_AF_URL"})
# CR_IS4_CHANGE_PAYMENT_PLAN_AF_URL = change_payment_plan_af_url['value']

# # Fetching CR_IS4_CHANGE_PAYMENT_PLAN_VF_URL
# change_payment_plan_vf_url = Constants_Collection.find_one({"variable_name": "CR_IS4_CHANGE_PAYMENT_PLAN_VF_URL"})
# CR_IS4_CHANGE_PAYMENT_PLAN_VF_URL = change_payment_plan_vf_url['value']
# # set next_needed = "numpayments"
# # send to IS2

# # Fetching CR_IS4_CHANGE_OTHER_INFO_START
# change_other_info_start = Constants_Collection.find_one({"variable_name": "CR_IS4_CHANGE_OTHER_INFO_START"})
# CR_IS4_CHANGE_OTHER_INFO_START = change_other_info_start['value']

# # Fetching CR_IS4_CHANGE_OTHER_INFO_START_AF_URL
# change_other_info_start_af_url = Constants_Collection.find_one({"variable_name": "CR_IS4_CHANGE_OTHER_INFO_START_AF_URL"})
# CR_IS4_CHANGE_OTHER_INFO_START_AF_URL = change_other_info_start_af_url['value']

# # Fetching CR_IS4_CHANGE_OTHER_INFO_START_VF_URL
# change_other_info_start_vf_url = Constants_Collection.find_one({"variable_name": "CR_IS4_CHANGE_OTHER_INFO_START_VF_URL"})
# CR_IS4_CHANGE_OTHER_INFO_START_VF_URL = change_other_info_start_vf_url['value']

# # Fetching CR_IS4_OTHER
# other = Constants_Collection.find_one({"variable_name": "CR_IS4_OTHER"})
# CR_IS4_OTHER = other['value']

# # Fetching CR_IS4_OTHER_AF_URL
# other_af_url = Constants_Collection.find_one({"variable_name": "CR_IS4_OTHER_AF_URL"})
# CR_IS4_OTHER_AF_URL = other_af_url['value']

# # Fetching CR_IS4_OTHER_VF_URL
# other_vf_url = Constants_Collection.find_one({"variable_name": "CR_IS4_OTHER_VF_URL"})
# CR_IS4_OTHER_VF_URL = other_vf_url['value']

# # Fetching CR_ERROR_APPOLOGY
# error_apology = Constants_Collection.find_one({"variable_name": "CR_ERROR_APPOLOGY"})
# CR_ERROR_APPOLOGY = error_apology['value']

# # Fetching CR_ERROR_APPOLOGY_AF_URL
# error_apology_af_url = Constants_Collection.find_one({"variable_name": "CR_ERROR_APPOLOGY_AF_URL"})
# CR_ERROR_APPOLOGY_AF_URL = error_apology_af_url['value']

# # Fetching CR_ERROR_APPOLOGY_VF_URL
# error_apology_vf_url = Constants_Collection.find_one({"variable_name": "CR_ERROR_APPOLOGY_VF_URL"})
# CR_ERROR_APPOLOGY_VF_URL = error_apology_vf_url['value']
