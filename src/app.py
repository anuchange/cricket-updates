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
        os.chdir('./src/cric_scrapper')
        subprocess.run(['scrapy', 'crawl', 'cricbuzz'], check=True)
        logging.info("Scrapy job completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.info(f"Error running Scrapy: {e}")

# Initialize the scheduler
scheduler = BackgroundScheduler()

try:
    hr = 15
    mnt = 0
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

# Vercel routes
@app.route("/api/cron-jobs")
def trigger_render():
    try:
        # This will wake up your Render container
        response = requests.get("https://pavilion-post.onrender.com/")
        return {"status": "success", "message": "Render container triggered"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

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
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 


