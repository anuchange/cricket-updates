import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
sys.path.append("\\".join(os.getcwd().split("\\")[:-2]))
from dotenv import load_dotenv
from create_summary_email import create_email
import logging
load_dotenv()

# Email configuration
sender_email = os.environ['SENDER_EMAIL']
sender_email_key = os.environ['SENDER_EMAIL_KEY']


def new_user_send_email(receiver_email):

    file_name = 'welcome.html'
    email_dir = "\\".join(os.getcwd().split("\\")[:-1])+'\\data\\'+file_name

    # Read HTML content from file with UTF-8 encoding
    with open(email_dir, 'r', encoding='utf-8') as file:
        html_content = file.read()

    msg = MIMEMultipart()
    msg['Subject'] = 'Welcome to the Pavilion Post Family! 🎉'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.attach(MIMEText(html_content, "html"))

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_email_key)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        logging.info("Email sent successfully!")
    except Exception as e:
        logging.info("Email is not Sent.")
        logging.info(f"Error: {e}")

    return


def existing_users_send_emails(receiver_email_list):

    # Read HTML content from date
    html_content = create_email()

    for receiver_email in receiver_email_list:
        msg = MIMEMultipart()
        msg['Subject'] = "Today's newsletter from you own Pavilion Post Family!"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.attach(MIMEText(html_content, "html"))

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_email_key)
                server.sendmail(sender_email, receiver_email, msg.as_string())

            logging.info("Email sent successfully!")
        except Exception as e:
            logging.info("Email is not Sent.")
            logging.info(f"Error: {e}")

    return
