import os
import sys
sys.path.append(os.getcwd()+"\\emails")
import src.emails.email_sender as es
import src.mongo_script as ms
import logging

def onboarding(user_email):
    if not isinstance(user_email, str):
        user_email = str(user_email)

    # insert user in db
    ms.insert_user(user_email)

    # send email to new user
    es.new_user_send_email(user_email)

    logging.info("--------------------------------------")
    logging.info("----------ONBOARDING COMPLETE---------")
    logging.info("--------------------------------------")

    return

def send_emails():

    # getting all users
    email_list = ms.get_all_users()

    # send email to all users
    es.existing_users_send_emails(email_list)

    #print for terminal
    print("-------EMAILS SENT SUCCESSFULLY-------")
    logging.info("--------------------------------------")
    logging.info("-------EMAILS SENT SUCCESSFULLY-------")
    logging.info("--------------------------------------")

