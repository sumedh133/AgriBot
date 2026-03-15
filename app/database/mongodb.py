from pymongo import MongoClient
from app.config import MONGODB_URI,DB_NAME

_client = None

def get_database():
    global _client

    if _client is None:
        _client = MongoClient(MONGODB_URI)

    return _client[DB_NAME]