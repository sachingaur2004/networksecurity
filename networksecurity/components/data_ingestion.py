import os
import sys
import numpy as np
import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

# Load environment variables
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """
        Read data from MongoDB and return as DataFrame
        """
        try:
            logging.info("Connecting to MongoDB")

            client = pymongo.MongoClient(MONGO_DB_URL)
            database = client[self.data_ingestion_config.database_name]
            collection = database[self.data_ingestion_config.collection_name]

            df = pd.DataFrame(list(collection.find()))

            if df.empty:
                raise ValueError("MongoDB collection is empty")

            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            df.replace({"na": np.nan}, inplace=True)

            logging.info(f"Fetched data from MongoDB with shape: {df.shape}")

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Save raw data into feature store
        """
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_path, index=False, header=True)

            logging.info(f"Feature store created at: {feature_store_path}")

            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> None:
        """
        Split data into train and test CSV files
        """
        try:
            if dataframe.shape[0] < 2:
                raise ValueError("Not enough data to perform train-test split")

            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42,
                shuffle=True,
            )

            logging.info("Performed train-test split")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True,
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True,
            )

            logging.info("Train and test datasets exported successfully")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Initiating Data Ingestion")

            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )

            logging.info(f"Data Ingestion completed: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
