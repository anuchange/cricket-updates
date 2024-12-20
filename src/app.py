from flask import Flask, request, jsonify, send_from_directory
import os
import subprocess
import time
from src.onboarding_and_emails import send_emails, onboarding
from src.llm_call import llm_call
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import sys
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__, static_folder='static')
# Initialize the scheduler
scheduler = BackgroundScheduler()

@app.route('/')
def home():

    logging.info("Hit Home")
    # Check for the secret token
    cron_secret = request.headers.get('X-Cron-Secret')
    if cron_secret and cron_secret == os.environ.get('CRON_JOB_KEY'):
        # print("Getting Inside")
        # Only start the scheduler if it's the cron job
        try:
            # 1. Run scraping
            logging.info("Starting scraping...")
            run_scrapy()
            logging.info("Scraping completed")
            
            # 2. Run LLM processing
            logging.info("Starting LLM processing...")
            call_init = llm_call()
            call_init.cricket_content()
            logging.info("LLM processing completed")
            
            # 3. Send emails
            logging.info("Starting email sending...")
            send_emails()
            logging.info("Emails sent")
            # print("In try")
            # hr = time.gmtime().tm_hour
            # mnt = time.gmtime().tm_min + 1
            # print(hr, mnt, type(hr), type(mnt))
            # # Scheduling the scrapy job to run every day
            # scrapy_trigger = CronTrigger(hour=hr, minute=mnt)
            # scheduler.add_job(run_scrapy, scrapy_trigger)
            # print("Scrapy job done")
            # # Scheduling the llm call
            # call_init = llm_call()
            # email_trigger = CronTrigger(hour=hr, minute=mnt+2)
            # scheduler.add_job(call_init.cricket_content, email_trigger)    
            # print("LLm call done")
            # # Schedule the send_emails job to run after the Scrapy job
            # email_trigger = CronTrigger(hour=hr, minute=mnt+7)
            # scheduler.add_job(send_emails, email_trigger)
            # print("Sent emails")

        except:
            logging.info("Outside try")
            logging.info("We regret to inform that we can't send updates mail today!")
    
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
        os.chdir('./src/cric_scrapper')
        subprocess.run(['scrapy', 'crawl', 'cricbuzz'], check=True)
        logging.info("Scrapy job completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.info(f"Error running Scrapy: {e}")




# # Vercel routes
# def ping_render():
#     # Configure shorter timeouts and retries
#     session = requests.Session()
#     retry_strategy = Retry(
#         total=1,
#         backoff_factor=1,
#         status_forcelist=[500, 502, 503, 504]
#     )
#     adapter = HTTPAdapter(max_retries=retry_strategy)
#     session.mount("http://", adapter)
#     session.mount("https://", adapter)
    
#     try:
#         # Set a very short timeout
#         response = session.get("https://pavilion-post.onrender.com/", timeout=5)
#         return True
#     except Exception as e:
#         print(f"Error pinging Render: {str(e)}")
#         return False

# @app.route("/api/cron-jobs")
# def trigger_render():
#     # Use ThreadPoolExecutor to run the request in background
#     with ThreadPoolExecutor() as executor:
#         future = executor.submit(ping_render)
#         # Don't wait for the response
#         return {"status": "success", "message": "Render container trigger initiated"}, 200
    
def ping_render():
    session = requests.Session()
    retry_strategy = Retry(
        total=1,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    try:
        # Add a secret token in headers
        headers = {'X-Cron-Secret': os.environ.get('CRON_JOB_KEY')}
        response = session.get("https://pavilion-post.onrender.com/", headers=headers, timeout=5)
        return True
    except Exception as e:
        print(f"Error pinging Render: {str(e)}")
        return False

@app.route("/api/cron-jobs")
def trigger_render():
    ping_render()
    return {"status": "success", "message": "Render container trigger initiated"}, 200

# can't run this because cron time is limited to 60 seconds
# def run_all_jobs():
#     try:
#         # Run scraping
#         logging.info("Scrapy starting")
#         # logging.info(os.getcwd())
#         # os.chdir('./src/cric_scrapper')
#         # logging.info(os.getcwd())
#         # logging.info("_________________")
#         # logging.info(os.listdir())

#         # Print initial working directory
#         print(f"Initial directory: {os.getcwd()}")
        
#         # Change to the directory with scrapy.cfg
#         os.chdir('./src/cric_scrapper')
#         print(f"Changed to directory: {os.getcwd()}")
        
#         # List all files to verify location
#         print("Files in current directory:", os.listdir())
        
#         # Print Python executable and path
#         print("Python executable:", sys.executable)
#         print("Python path:", sys.path)
        
#         # Try using python -m scrapy instead of direct scrapy command
#         result = subprocess.run([sys.executable, '-m', 'scrapy', 'crawl', 'cricbuzz'], 
#                               capture_output=True,
#                               text=True)
#         print("Spider output:", result.stdout)
#         print("Spider error:", result.stderr)

#         # Add root directory to Python path
#         root_path = '/var/task'
#         if root_path not in sys.path:
#             sys.path.insert(0, root_path)
        
#         print("Updated Python path:", sys.path)
        
#         # Change directory and run spider
#         os.chdir('/var/task/src/cric_scrapper')
#         print(f"Current directory: {os.getcwd()}")

#         # Import and run spider directly
#         from scrapy.crawler import CrawlerProcess
#         from scrapy.utils.project import get_project_settings
        
#         # Import your spider (adjust the import path as needed)
#         from src.cric_scrapper.cric_scrapper.spiders.cricbuzz import CricbuzzSpider
        
#         try:
#             # Get project settings
#             settings = get_project_settings()
            
#             # Create crawler process
#             process = CrawlerProcess(settings)
            
#             # Add spider to crawler
#             process.crawl(CricbuzzSpider)
            
#             # Run the spider
#             process.start()
            
#             print("Spider completed successfully")
            
#         except Exception as e:
#             print("Spider error:", str(e))
#             import traceback
#             traceback.print_exc()

        
#         result = subprocess.run([sys.executable, '-m', 'scrapy', 'crawl', 'your_spider_name'], 
#                               capture_output=True,
#                               text=True)
#         print("Spider output:", result.stdout)
#         print("Spider error:", result.stderr)


#         # subprocess.run(['scrapy', 'crawl', 'cricbuzz'], check=True)
#         logging.info("Scraping completed")
        
#         # Wait  minutes
#         # time.sleep(20)
        
#         # Run LLM processing
#         call_init = llm_call()
#         call_init.cricket_content()
#         logging.info("LLM processing completed")
        
#         # Wait 5 minutes
#         # time.sleep(60)
        
#         # Send emails
#         send_emails()
#         logging.info("Emails sent")
        
#         return jsonify({"status": "success", "message": "All jobs completed"}), 200
#     except Exception as e:
#         logging.error(f"Job error: {e}")
#         return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use PORT environment variable or default to 5000 for local development
    # Start the scheduler
    scheduler.start()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 


