from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_DB_URL"))

# ✅ MATCH PIPELINE CONSTANTS
db = client["network_security_db"]
collection = db["network_logs"]

data = [
    {"feature1": 10, "feature2": 0.5, "feature3": 1, "label": 0},
    {"feature1": 12, "feature2": 0.7, "feature3": 0, "label": 1},
    {"feature1": 8,  "feature2": 0.3, "feature3": 1, "label": 0},
]

collection.insert_many(data)
print("Data inserted successfully into network_security_db.network_logs")
