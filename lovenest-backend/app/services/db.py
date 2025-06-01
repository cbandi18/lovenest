from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGODB_URL"))
db = client["lovenest"]

users_collection = db["users"]
articles_collection = db["articles"]
