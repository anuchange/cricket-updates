import os
from groq import Groq
import sys
sys.path.append("\\".join(os.getcwd().split("\\")[:-1]))
import mongo_script
import datetime
import logging
import json
from time import sleep

# Set your GROQ API key
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
model_name = "llama-3.2-11b-vision-preview"

class llm_call:

    def __init__(self):

        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

    def response_generation(self, message):

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model=model_name
        )

        return chat_completion.choices[0].message.content
    
    def process_latest_news(self, news_list):

        news_summaries = []
        for latest_news in news_list:
            summary = {}
            news_title = latest_news['title']
            news = latest_news['news']
            message = f"Your role is a 'Summarization Machine', which will summarize text in 50-60 words, keeping all important points. Given news of the cricket: {news}. If there is no news, then summary can be we don't have news but will keep you posted."
            news_summary = self.response_generation(message)
            summary[news_title] = news_summary
            news_summaries.append(summary)
            sleep(6) 

        return news_summaries

    def process_scores(self, score_list):

        match_summaries = []
        for scores_details in score_list:
            score_summary = {}
            score_title = scores_details['title']
            match_summary = scores_details['summary']
            message = f"Your role is a 'Cricket Match Updater', which will write match details in 20-30 words, keeping all important points. Given match summary: {match_summary} of the cricket match"
            news_summary = self.response_generation(message)
            score_summary[score_title] = news_summary
            match_summaries.append(score_summary)
            sleep(6) 

        return match_summaries

    def cricket_content(self):

        date_today = str(datetime.date.today())
        # date_today = '2024-10-28'
        try:
            data_retrieved = mongo_script.retrieve_from_db(date_today)
        except Exception as e:
            logging.info("Data is not scrapped properly.")
            logging.info(f"Error: {e}")


        print("--------------------------")
        # print(data_retrieved)
        print("--------------------------")

        news_list = data_retrieved['latest_news_section']
        score_list = data_retrieved['match_details']
        news_summaries = self.process_latest_news(news_list)
        match_summaries = self.process_scores(score_list)
        data = {}
        data['latest_news_section'] = news_summaries
        data['match_details'] = match_summaries

        try:
            inserted_id = mongo_script.insert_to_summary_db(data)
            logging.info(f"Inserted into db with id:{inserted_id}")
        except Exception as e:
            logging.info("Problem inserting data into MongoDB")
            logging.info(f"Error: {e}")

        # Writing JSON data
        # file_name = 'summariesdata.json'
        # data_dir = "\\".join(os.getcwd().split("\\")[:-1]) + '\\data\\' + file_name
        # with open(data_dir, 'w') as json_file:
        #     json.dump(data, json_file, indent=4) 