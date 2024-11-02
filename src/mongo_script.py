from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
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

    # Delete all existing collections in the database by retrieving all existing collection names
    existing_collections = db.list_collection_names()
    if existing_collections:
        for collection_name in existing_collections:
            db.drop_collection(collection_name)
            logging.info(f"Deleted existing collection: {collection_name}")
    else:
        logging.info("No existing collections to delete.")

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

    # Delete all existing collections in the database by retrieving all existing collection names
    existing_collections = summary_db.list_collection_names()
    if existing_collections:
        for collection_name in existing_collections:
            db.drop_collection(collection_name)
            logging.info(f"Deleted existing collection: {collection_name}")
    else:
        logging.info("No existing collections to delete.")

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

user_db = client.user_data  
def insert_user(email):
    collection = user_db['subscribed_users']

    # Check if the email already exists
    try: 
        existing_user = collection.find_one({'email': email})
        if existing_user:
            logging.info("Email already exists.")
            return False  
    except:
        logging.info('User not exist, continuing to register user!')
    # Insert new user with subscribed date
    user_data = {
        'email': email,
        'date_added': datetime.datetime.now() 
    }
    
    try:
        collection.insert_one(user_data)
        logging.info("User added successfully.")
        return True  # User added successfully
    except DuplicateKeyError:
        logging.info("Error: Duplicate key error.")
        return False
    
def get_all_users():
    collection = user_db['subscribed_users']
    logging.info("------------------------------")
    logging.info("------------RETRIEVED------------")
    logging.info("------------------------------")
    emails = collection.find({}, {'email': 1})
    email_list = [email['email'] for email in emails]
    return email_list