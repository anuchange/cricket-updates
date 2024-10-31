from flask import Flask, request, jsonify, send_from_directory
import os
import subprocess
from onboarding_and_emails import send_emails, onboarding
from llm_call import llm_call
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/sign-in')
def sign_in():
    return send_from_directory(app.static_folder, 'sign-in.html')

@app.route('/api/onboard', methods=['POST'])
def handle_onboard():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400

        # Calling onboarding function
        onboarding(email)
        
        return jsonify({'message': 'Registration successful'}), 201
    
    except Exception as e:
        logging.info(f"Error during onboarding: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Handling scrapy automatic run
def run_scrapy():
    try:
        os.chdir('./cric_scrapper')
        subprocess.run(['scrapy', 'crawl', 'cricbuzz'], check=True)
        logging.info("Scrapy job completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.info(f"Error running Scrapy: {e}")

# Initialize the scheduler
scheduler = BackgroundScheduler()

try:
    hr = 3
    mnt = 4
    # Scheduling the scrapy job to run every day
    scrapy_trigger = CronTrigger(hour=hr, minute=mnt)
    scheduler.add_job(run_scrapy, scrapy_trigger)

    # Scheduling the llm call
    call_init = llm_call()
    email_trigger = CronTrigger(hour=hr, minute=mnt+2)
    scheduler.add_job(call_init.cricket_content, email_trigger)    

    # Schedule the send_emails job to run after the Scrapy job
    email_trigger = CronTrigger(hour=hr, minute=mnt+7)
    scheduler.add_job(send_emails, email_trigger)

except:

    logging.info("We regret to inform that we can't send updates mail today!")

# Start the scheduler
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True, port=5000)