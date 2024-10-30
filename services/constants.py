from astrapy import DataAPIClient
# import pandas as pd


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

print("\n\n\I am here\n\n\n")

# Step 1: Fetch all variables from the database into a dictionary
variables = {}
for variable in Constants_Collection.find({}):
    variable_name = variable['variable_name']
    value = variable['value']
    variables[variable_name] = value

# Step 2: Define a function to recursively resolve placeholders, with an option to ignore certain placeholders
def resolve_placeholders(variables, ignore_placeholders=None):
    import re
    if ignore_placeholders is None:
        ignore_placeholders = set()
    else:
        ignore_placeholders = set(ignore_placeholders)

    pattern = re.compile(r'\{(\w+)\}')
    unresolved = True

    while unresolved:
        unresolved = False
        for key, value in variables.items():
            placeholders = pattern.findall(value)
            for placeholder in placeholders:
                if placeholder in ignore_placeholders:
                    continue  # Skip placeholders that should be ignored
                if placeholder in variables:
                    # Replace the placeholder with its value
                    value = value.replace(f'{{{placeholder}}}', variables[placeholder])
                    variables[key] = value
                    unresolved = True
                else:
                    raise ValueError(f"Placeholder {{{placeholder}}} not found in variables.")
    return variables

# Step 3: Resolve the placeholders, specifying placeholders to ignore
ignore_list = ['first_name']
processed_variables = resolve_placeholders(variables, ignore_placeholders=ignore_list)

# Fetching CP_PREAMBLE
CP_PREAMBLE = processed_variables['CP_PREAMBLE']

# Fetching CP_TASK
CP_TASK = processed_variables['CP_TASK']

# Fetching CP_GREETING
CP_GREETING = processed_variables['CP_GREETING']

# Fetching CP_GENERAL
CP_GENERAL = processed_variables['CP_GENERAL']

# Fetching CP_TRANSFER_TO_HUMAN
CP_TRANSFER_TO_HUMAN = processed_variables['CP_TRANSFER_TO_HUMAN']

# Fetching CP_OBJECTION
CP_OBJECTION = processed_variables['CP_OBJECTION']

# Fetching CP_POSITIVE
CP_POSITIVE = processed_variables['CP_POSITIVE']

# Fetching CP_NEGATIVE
CP_NEGATIVE = processed_variables['CP_NEGATIVE']

# Fetching CP_MORE_QUESTIONS
CP_MORE_QUESTIONS = processed_variables['CP_MORE_QUESTIONS']

# Fetching CP_OTHER
CP_OTHER = processed_variables['CP_OTHER']

# Fetching CR_OTHER_START
CR_OTHER_START = processed_variables['CR_OTHER_START']

# Fetching CR_OTHER_START_AF_URL
CR_OTHER_START_AF_URL = processed_variables['CR_OTHER_START_AF_URL']

# Fetching CR_OTHER_START_VF_URL
CR_OTHER_START_VF_URL = processed_variables['CR_OTHER_START_VF_URL']

# Fetching CR_GENERAL_START
CR_GENERAL_START = processed_variables['CR_GENERAL_START']

# Fetching CR_GENERAL_START_AF_URL
CR_GENERAL_START_AF_URL = processed_variables['CR_GENERAL_START_AF_URL']

# Fetching CR_GENERAL_START_VF_URL
CR_GENERAL_START_VF_URL = processed_variables['CR_GENERAL_START_VF_URL']

# Fetching CR_PURCHASE_NEEDED
CR_PURCHASE_NEEDED = processed_variables['CR_PURCHASE_NEEDED']

# Fetching CR_PURCHASE_NEEDED_AF_URL
CR_PURCHASE_NEEDED_AF_URL = processed_variables['CR_PURCHASE_NEEDED_AF_URL']

# Fetching CR_PURCHASE_NEEDED_VF_URL
CR_PURCHASE_NEEDED_VF_URL = processed_variables['CR_PURCHASE_NEEDED_VF_URL']

# Fetching CR_PACKAGE_NEEDED
CR_PACKAGE_NEEDED = processed_variables['CR_PACKAGE_NEEDED']

# Fetching CR_PACKAGE_NEEDED_AF_URL
CR_PACKAGE_NEEDED_AF_URL = processed_variables['CR_PACKAGE_NEEDED_AF_URL']

# Fetching CR_PACKAGE_NEEDED_VF_URL
CR_PACKAGE_NEEDED_VF_URL = processed_variables['CR_PACKAGE_NEEDED_VF_URL']

# Fetching CR_NUMPAYMENTS_NEEDED
CR_NUMPAYMENTS_NEEDED = processed_variables['CR_NUMPAYMENTS_NEEDED']

# Fetching CR_NUMPAYMENTS_NEEDED_AF_URL
CR_NUMPAYMENTS_NEEDED_AF_URL = processed_variables['CR_NUMPAYMENTS_NEEDED_AF_URL']

# Fetching CR_NUMPAYMENTS_NEEDED_VF_URL
CR_NUMPAYMENTS_NEEDED_VF_URL = processed_variables['CR_NUMPAYMENTS_NEEDED_VF_URL']

# Fetching CR_DISPLAY_NEEDED
CR_DISPLAY_NEEDED = processed_variables['CR_DISPLAY_NEEDED']

# Fetching CR_DISPLAY_NEEDED_AF_URL
CR_DISPLAY_NEEDED_AF_URL = processed_variables['CR_DISPLAY_NEEDED_AF_URL']

# Fetching CR_DISPLAY_NEEDED_VF_URL
CR_DISPLAY_NEEDED_VF_URL = processed_variables['CR_DISPLAY_NEEDED_VF_URL']

# Fetching CR_SIGNATURE_NEEDED
CR_SIGNATURE_NEEDED = processed_variables['CR_SIGNATURE_NEEDED']

# Fetching CR_SIGNATURE_NEEDED_AF_URL
CR_SIGNATURE_NEEDED_AF_URL = processed_variables['CR_SIGNATURE_NEEDED_AF_URL']

# Fetching CR_SIGNATURE_NEEDED_VF_URL
CR_SIGNATURE_NEEDED_VF_URL = processed_variables['CR_SIGNATURE_NEEDED_VF_URL']

# Fetching CR_PAYMENT_NEEDED
CR_PAYMENT_NEEDED = processed_variables['CR_PAYMENT_NEEDED']

# Fetching CR_PAYMENT_NEEDED_AF_URL
CR_PAYMENT_NEEDED_AF_URL = processed_variables['CR_PAYMENT_NEEDED_AF_URL']

# Fetching CR_PAYMENT_NEEDED_VF_URL
CR_PAYMENT_NEEDED_VF_URL = processed_variables['CR_PAYMENT_NEEDED_VF_URL']

# Fetching CR_BOOKING_NEEDED
CR_BOOKING_NEEDED = processed_variables['CR_BOOKING_NEEDED']

# Fetching CR_BOOKING_NEEDED_AF_URL
CR_BOOKING_NEEDED_AF_URL = processed_variables['CR_BOOKING_NEEDED_AF_URL']

# Fetching CR_BOOKING_NEEDED_VF_URL
CR_BOOKING_NEEDED_VF_URL = processed_variables['CR_BOOKING_NEEDED_VF_URL']

# Fetching CR_COMPLETED
CR_COMPLETED = processed_variables['CR_COMPLETED']

# Fetching CR_COMPLETED_AF_URL
CR_COMPLETED_AF_URL = processed_variables['CR_COMPLETED_AF_URL']

# Fetching CR_COMPLETED_VF_URL
CR_COMPLETED_VF_URL = processed_variables['CR_COMPLETED_VF_URL']

# Fetching CR_ADDITIONAL_QUESTIONS
CR_ADDITIONAL_QUESTIONS = processed_variables['CR_ADDITIONAL_QUESTIONS']

# Fetching CR_ADDITIONAL_QUESTIONS_AF_URL
CR_ADDITIONAL_QUESTIONS_AF_URL = processed_variables['CR_ADDITIONAL_QUESTIONS_AF_URL']

# Fetching CR_ADDITIONAL_QUESTIONS_VF_URL
CR_ADDITIONAL_QUESTIONS_VF_URL = processed_variables['CR_ADDITIONAL_QUESTIONS_VF_URL']

# Fetching CR_TRANSFER_TO_HUMAN
CR_TRANSFER_TO_HUMAN = processed_variables['CR_TRANSFER_TO_HUMAN']

# Fetching CR_TRANSFER_TO_HUMAN_AF_URL
CR_TRANSFER_TO_HUMAN_AF_URL = processed_variables['CR_TRANSFER_TO_HUMAN_AF_URL']

# Fetching CR_TRANSFER_TO_HUMAN_VF_URL
CR_TRANSFER_TO_HUMAN_VF_URL = processed_variables['CR_TRANSFER_TO_HUMAN_VF_URL']

# Fetching CR_NEW_GREETING_MESSAGE
CR_NEW_GREETING_MESSAGE = processed_variables['CR_NEW_GREETING_MESSAGE']

# Fetching CR_NEW_GREETING_MESSAGE_AF_URL
CR_NEW_GREETING_MESSAGE_AF_URL = processed_variables['CR_NEW_GREETING_MESSAGE_AF_URL']

# Fetching CR_NEW_GREETING_MESSAGE_VF_URL
CR_NEW_GREETING_MESSAGE_VF_URL = processed_variables['CR_NEW_GREETING_MESSAGE_VF_URL']

# Fetching CR_OLD_GREETING_MESSAGE
CR_OLD_GREETING_MESSAGE = processed_variables['CR_OLD_GREETING_MESSAGE']

# Fetching CR_OLD_GREETING_MESSAGE_AF_URL
CR_OLD_GREETING_MESSAGE_AF_URL = processed_variables['CR_OLD_GREETING_MESSAGE_AF_URL']

# Fetching CR_OLD_GREETING_MESSAGE_VF_URL
CR_OLD_GREETING_MESSAGE_VF_URL = processed_variables['CR_OLD_GREETING_MESSAGE_VF_URL']

# Fetching CP_COMMAND_AND_CONTROL
CP_COMMAND_AND_CONTROL = processed_variables['CP_COMMAND_AND_CONTROL']

# Fetching CP_IS1_SYSTEM_PROMPT
CP_IS1_SYSTEM_PROMPT = processed_variables['CP_IS1_SYSTEM_PROMPT']

# Fetching CR_IS1_PURCHASE
CR_IS1_PURCHASE = processed_variables['CR_IS1_PURCHASE']

# Fetching CR_IS1_PURCHASE_AF_URL
CR_IS1_PURCHASE_AF_URL = processed_variables['CR_IS1_PURCHASE_AF_URL']

# Fetching CR_IS1_PURCHASE_VF_URL
CR_IS1_PURCHASE_VF_URL = processed_variables['CR_IS1_PURCHASE_VF_URL']

# Fetching CP_IS2_SYSTEM_PROMPT
CP_IS2_SYSTEM_PROMPT = processed_variables['CP_IS2_SYSTEM_PROMPT']

# Fetching CP_IS2_TRUST_PACKAGE_PROMPT
CP_IS2_TRUST_PACKAGE_PROMPT = processed_variables['CP_IS2_TRUST_PACKAGE_PROMPT']

# Fetching CR_IS2_TRUST_PACKAGE
CR_IS2_TRUST_PACKAGE = processed_variables['CR_IS2_TRUST_PACKAGE']

# Fetching CR_IS2_TRUST_PACKAGE_AF_URL
CR_IS2_TRUST_PACKAGE_AF_URL = processed_variables['CR_IS2_TRUST_PACKAGE_AF_URL']

# Fetching CR_IS2_TRUST_PACKAGE_VF_URL
CR_IS2_TRUST_PACKAGE_VF_URL = processed_variables['CR_IS2_TRUST_PACKAGE_VF_URL']

# Fetching CP_IS2_PAYMENTS_PROMPT
CP_IS2_PAYMENTS_PROMPT = processed_variables['CP_IS2_PAYMENTS_PROMPT']
# Fetching CR_IS2_PAYMENTS
CR_IS2_PAYMENTS = processed_variables['CR_IS2_PAYMENTS']

# Fetching CR_IS2_PAYMENTS_AF_URL
CR_IS2_PAYMENTS_AF_URL = processed_variables['CR_IS2_PAYMENTS_AF_URL']

# Fetching CR_IS2_PAYMENTS_VF_URL
CR_IS2_PAYMENTS_VF_URL = processed_variables['CR_IS2_PAYMENTS_VF_URL']

# Fetching CR_IS2_INVALID_NUM_PAYMENTS
CR_IS2_INVALID_NUM_PAYMENTS = processed_variables['CR_IS2_INVALID_NUM_PAYMENTS']

# Fetching CR_IS2_INVALID_NUM_PAYMENTS_AF_URL
CR_IS2_INVALID_NUM_PAYMENTS_AF_URL = processed_variables['CR_IS2_INVALID_NUM_PAYMENTS_AF_URL']

# Fetching CR_IS2_INVALID_NUM_PAYMENTS_VF_URL
CR_IS2_INVALID_NUM_PAYMENTS_VF_URL = processed_variables['CR_IS2_INVALID_NUM_PAYMENTS_VF_URL']

# Fetching CP_IS4_SYSTEM_PROMPT
CP_IS4_SYSTEM_PROMPT = processed_variables['CP_IS4_SYSTEM_PROMPT']

# Fetching CR_IS4_TASK_ISSUE
CR_IS4_TASK_ISSUE = processed_variables['CR_IS4_TASK_ISSUE']

# Fetching CR_IS4_TASK_ISSUE_AF_URL
CR_IS4_TASK_ISSUE_AF_URL = processed_variables['CR_IS4_TASK_ISSUE_AF_URL']

# Fetching CR_IS4_TASK_ISSUE_VF_URL
CR_IS4_TASK_ISSUE_VF_URL = processed_variables['CR_IS4_TASK_ISSUE_VF_URL']

# Fetching CR_IS4_AGREEMENT_DISPLAYED
CR_IS4_AGREEMENT_DISPLAYED = processed_variables['CR_IS4_AGREEMENT_DISPLAYED']

# Fetching CR_IS4_AGREEMENT_DISPLAYED_AF_URL
CR_IS4_AGREEMENT_DISPLAYED_AF_URL = processed_variables['CR_IS4_AGREEMENT_DISPLAYED_AF_URL']

# Fetching CR_IS4_AGREEMENT_DISPLAYED_VF_URL
CR_IS4_AGREEMENT_DISPLAYED_VF_URL = processed_variables['CR_IS4_AGREEMENT_DISPLAYED_VF_URL']
# set next_needed = "signature"

# Fetching CR_IS4_AGREEMENT_SIGNATURE_DONE
CR_IS4_AGREEMENT_SIGNATURE_DONE = processed_variables['CR_IS4_AGREEMENT_SIGNATURE_DONE']

# Fetching CR_IS4_AGREEMENT_SIGNATURE_DONE_AF_URL
CR_IS4_AGREEMENT_SIGNATURE_DONE_AF_URL = processed_variables['CR_IS4_AGREEMENT_SIGNATURE_DONE_AF_URL']

# Fetching CR_IS4_AGREEMENT_SIGNATURE_DONE_VF_URL
CR_IS4_AGREEMENT_SIGNATURE_DONE_VF_URL = processed_variables['CR_IS4_AGREEMENT_SIGNATURE_DONE_VF_URL']
# set next_needed = "paid"

# Fetching CR_IS4_AGREEMENT_PAID
CR_IS4_AGREEMENT_PAID = processed_variables['CR_IS4_AGREEMENT_PAID']

# Fetching CR_IS4_AGREEMENT_PAID_AF_URL
CR_IS4_AGREEMENT_PAID_AF_URL = processed_variables['CR_IS4_AGREEMENT_PAID_AF_URL']

# Fetching CR_IS4_AGREEMENT_PAID_VF_URL
CR_IS4_AGREEMENT_PAID_VF_URL = processed_variables['CR_IS4_AGREEMENT_PAID_VF_URL']
# set next_needed = "booking"

# Fetching CR_IS4_OS_BOOKING_DONE
CR_IS4_OS_BOOKING_DONE = processed_variables['CR_IS4_OS_BOOKING_DONE']

# Fetching CR_IS4_OS_BOOKING_DONE_AF_URL
CR_IS4_OS_BOOKING_DONE_AF_URL = processed_variables['CR_IS4_OS_BOOKING_DONE_AF_URL']

# Fetching CR_IS4_OS_BOOKING_DONE_VF_URL
CR_IS4_OS_BOOKING_DONE_VF_URL =processed_variables['CR_IS4_OS_BOOKING_DONE_VF_URL']
# set next_needed = "completed"

# Fetching CR_IS4_BOOKING_COMPLETED
CR_IS4_BOOKING_COMPLETED = processed_variables['CR_IS4_BOOKING_COMPLETED']

# Fetching CR_IS4_BOOKING_COMPLETED_AF_URL
CR_IS4_BOOKING_COMPLETED_AF_URL = processed_variables['CR_IS4_BOOKING_COMPLETED_AF_URL']

# Fetching CR_IS4_BOOKING_COMPLETED_VF_URL
CR_IS4_BOOKING_COMPLETED_VF_URL =processed_variables['CR_IS4_BOOKING_COMPLETED_VF_URL']

# Fetching CR_IS4_CHANGE_TRUST_PACKAGE
CR_IS4_CHANGE_TRUST_PACKAGE = processed_variables['CR_IS4_CHANGE_TRUST_PACKAGE']

# Fetching CR_IS4_CHANGE_TRUST_PACKAGE_AF_URL
CR_IS4_CHANGE_TRUST_PACKAGE_AF_URL = processed_variables['CR_IS4_CHANGE_TRUST_PACKAGE_AF_URL']

# Fetching CR_IS4_CHANGE_TRUST_PACKAGE_VF_URL
CR_IS4_CHANGE_TRUST_PACKAGE_VF_URL = processed_variables['CR_IS4_CHANGE_TRUST_PACKAGE_VF_URL']

# Fetching CR_IS4_CHANGE_PAYMENT_PLAN
CR_IS4_CHANGE_PAYMENT_PLAN =processed_variables['CR_IS4_CHANGE_PAYMENT_PLAN']

# Fetching CR_IS4_CHANGE_PAYMENT_PLAN_AF_URL
CR_IS4_CHANGE_PAYMENT_PLAN_AF_URL = processed_variables['CR_IS4_CHANGE_PAYMENT_PLAN_AF_URL']

# Fetching CR_IS4_CHANGE_PAYMENT_PLAN_VF_URL
CR_IS4_CHANGE_PAYMENT_PLAN_VF_URL = processed_variables['CR_IS4_CHANGE_PAYMENT_PLAN_VF_URL']

# Fetching CR_IS4_CHANGE_OTHER_INFO_START
CR_IS4_CHANGE_OTHER_INFO_START = processed_variables['CR_IS4_CHANGE_OTHER_INFO_START']

# Fetching CR_IS4_CHANGE_OTHER_INFO_START_AF_URL
CR_IS4_CHANGE_OTHER_INFO_START_AF_URL = processed_variables['CR_IS4_CHANGE_OTHER_INFO_START_AF_URL']

# Fetching CR_IS4_CHANGE_OTHER_INFO_START_VF_URL
CR_IS4_CHANGE_OTHER_INFO_START_VF_URL = processed_variables['CR_IS4_CHANGE_OTHER_INFO_START_VF_URL']

# Fetching CR_IS4_OTHER
CR_IS4_OTHER = processed_variables['CR_IS4_OTHER']

# Fetching CR_IS4_OTHER_AF_URL
CR_IS4_OTHER_AF_URL = processed_variables['CR_IS4_OTHER_AF_URL']

# Fetching CR_IS4_OTHER_VF_URL
CR_IS4_OTHER_VF_URL = processed_variables['CR_IS4_OTHER_VF_URL']

# Fetching CR_ERROR_APPOLOGY
CR_ERROR_APPOLOGY = processed_variables['CR_ERROR_APPOLOGY']

# Fetching CR_ERROR_APPOLOGY_AF_URL
CR_ERROR_APPOLOGY_AF_URL = processed_variables['CR_ERROR_APPOLOGY_AF_URL']

# Fetching CR_ERROR_APPOLOGY_VF_URL
CR_ERROR_APPOLOGY_VF_URL = processed_variables['CR_ERROR_APPOLOGY_VF_URL']

CR_GREETING_INNER_INTENT_PROMPT = processed_variables['CR_GREETING_INNER_INTENT_PROMPT']

CR_GREETING_SALUTATION = processed_variables['CR_GREETING_SALUTATION']
CR_GREETING_SALUTATION_AF_URL = processed_variables['CR_GREETING_SALUTATION_AF_URL']
CR_GREETING_SALUTATION_VF_URL = processed_variables['CR_GREETING_SALUTATION_VF_URL']

CR_GREETING_POLITE_CONCERN = processed_variables['CR_GREETING_POLITE_CONCERN']
CR_GREETING_POLITE_CONCERN_AF_URL = processed_variables['CR_GREETING_POLITE_CONCERN_AF_URL']
CR_GREETING_POLITE_CONCERN_VF_URL = processed_variables['CR_GREETING_POLITE_CONCERN_VF_URL']

CR_GREETING_PRIOR_QUESTION = processed_variables['CR_GREETING_PRIOR_QUESTION']
CR_GREETING_PRIOR_QUESTION_AF_URL = processed_variables['CR_GREETING_PRIOR_QUESTION_AF_URL']
CR_GREETING_PRIOR_QUESTION_VF_URL = processed_variables['CR_GREETING_PRIOR_QUESTION_VF_URL']

CR_GREETING_ASKING_NAME = processed_variables['CR_GREETING_ASKING_NAME']
CR_GREETING_ASKING_NAME_AF_URL = processed_variables['CR_GREETING_ASKING_NAME_AF_URL']
CR_GREETING_ASKING_NAME_VF_URL = processed_variables['CR_GREETING_ASKING_NAME_VF_URL']


CR_NEGATIVE_MESSAGE = "No Problem, you can ask me more questions if you need clarification on something."
CR_NEGATIVE_MESSAGE_AF_URL = ''
CR_NEGATIVE_MESSAGE_VF_URL = ''

CR_MORE_QUESTIONS = "Super, please let me know your question."
CR_MORE_QUESTIONS_AF_URL = ''
CR_MORE_QUESTIONS_VF_URL = ''

CR_POSITIVE_MESSAGE = "Glad to hear that."
CR_POSITIVE_MESSAGE_AF_URL = ''
CR_POSITIVE_MESSAGE_VF_URL = ''