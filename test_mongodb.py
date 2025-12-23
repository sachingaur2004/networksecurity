from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

# Username and password
username = quote_plus("sachinsingh9194_db_user")
password = quote_plus("Admin@123")  # special characters escaped

# Construct the URI with escaped credentials
uri = f"mongodb+srv://{username}:{password}@cluster0.vvdh9cd.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Error connecting to MongoDB:", e)
