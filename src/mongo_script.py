from pymongo import MongoClient
from dotenv import load_dotenv
import datetime
import os
import logging
load_dotenv()

user = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
client = MongoClient(f"mongodb+srv://{user}:{password}@cluster0.tbqu5.mongodb.net/")

db = client.cricket_updates
def insert_to_db(day_updates):
    logging.info("------------------------------")
    logging.info("------------CALLED------------")
    logging.info("------------------------------")
    collection = db[str(datetime.date.today())]
    inserted = collection.insert_one(day_updates)
    return inserted.inserted_id