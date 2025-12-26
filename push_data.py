import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()

import certifi
import pandas as pd
import pymongo

from networksecurity.exception.exception import NetworkSecurityException

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=ca
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            records = df.to_dict(orient="records")
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            db = self.mongo_client[database]
            col = db[collection]

            # 🔥 VERY IMPORTANT: clear old dummy data
            col.delete_many({})

            col.insert_many(records)
            return len(records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = r"C:\Users\Astral Divine\Downloads\networksecurity (1)\Network_Data\phisingData.csv"
    DATABASE = "Sachindb"
    COLLECTION = "NetworkData"

    networkobj = NetworkDataExtract()

    records = networkobj.csv_to_json_converter(FILE_PATH)
    print(f"Total records prepared: {len(records)}")

    count = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)
    print(f"Inserted records into MongoDB: {count}")
