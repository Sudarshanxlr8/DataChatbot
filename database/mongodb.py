import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "datachat_demo")

_client = None

def get_mongo_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return _client

def get_database() -> Database:
    client = get_mongo_client()
    return client[MONGO_DATABASE]

def close_db_connection():
    global _client
    if _client is not None:
        _client.close()
        _client = None
