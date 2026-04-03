from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)

db = client["soporte_bot"]

forms_col = db["forms"]
responses_col = db["responses"]
tickets_col = db["tickets"]
