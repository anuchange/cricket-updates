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
    collection = db[str(datetime.date.today())]
    inserted = collection.insert_one(day_updates)
    logging.info("------------------------------")
    logging.info("------------INSERTED------------")
    logging.info("------------------------------")
    return inserted.inserted_id

def retrieve_from_db(collection_name):
    if not isinstance(collection_name,str):
        collection_name = str(collection_name)
    collection = db[collection_name]
    logging.info("------------------------------")
    logging.info("------------RETRIEVED------------")
    logging.info("------------------------------")
    return collection.find_one()

summary_db = client.cricket_summaries
def insert_to_summary_db(day_updates):
    collection = summary_db[str(datetime.date.today())]
    inserted = collection.insert_one(day_updates)
    logging.info("------------------------------")
    logging.info("------------INSERTED------------")
    logging.info("------------------------------")
    return inserted.inserted_id

def retrieve_from_summary_db(collection_name):
    if not isinstance(collection_name,str):
        collection_name = str(collection_name)
    collection = summary_db[collection_name]
    logging.info("------------------------------")
    logging.info("------------RETRIEVED------------")
    logging.info("------------------------------")
    return collection.find_one()