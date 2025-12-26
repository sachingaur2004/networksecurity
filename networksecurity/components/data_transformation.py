import sys
import os
import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline.training_pipeline import (
    TARGET_COLUMN,
    DATA_TRANSFORMATION_IMPUTER_PARAMS,
)

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object


class DataTransformation:

    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformer_object(self) -> Pipeline:
        """
        Create preprocessing pipeline
        """
        try:
            logging.info("Creating data transformation pipeline")

            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)

            processor = Pipeline(steps=[("imputer", imputer)])

            return processor

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Started data transformation")

            # ---------------- LOAD DATA ----------------
            train_df = self.read_data(
                self.data_validation_artifact.validation_train_file_path
            )
            test_df = self.read_data(self.data_validation_artifact.valid_test_file_path)

            logging.info(f"Train DF columns: {train_df.columns.tolist()}")
            logging.info(f"Test DF columns: {test_df.columns.tolist()}")

            # ---------------- TARGET COLUMN CHECK ----------------
            if TARGET_COLUMN not in train_df.columns:
                raise Exception(
                    f"TARGET_COLUMN '{TARGET_COLUMN}' not found in train dataframe. "
                    f"Available columns: {train_df.columns.tolist()}"
                )

            if TARGET_COLUMN not in test_df.columns:
                raise Exception(
                    f"TARGET_COLUMN '{TARGET_COLUMN}' not found in test dataframe. "
                    f"Available columns: {test_df.columns.tolist()}"
                )

            # ---------------- SPLIT FEATURES & TARGET ----------------
            X_train = train_df.drop(columns=[TARGET_COLUMN])
            y_train = train_df[TARGET_COLUMN].replace(-1, 0)

            X_test = test_df.drop(columns=[TARGET_COLUMN])
            y_test = test_df[TARGET_COLUMN].replace(-1, 0)

            # ---------------- PREPROCESSING ----------------
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(X_train)

            X_train_transformed = preprocessor_object.transform(X_train)
            X_test_transformed = preprocessor_object.transform(X_test)

            # ---------------- FINAL ARRAYS ----------------
            train_arr = np.c_[X_train_transformed, np.array(y_train)]
            test_arr = np.c_[X_test_transformed, np.array(y_test)]

            # ---------------- SAVE OUTPUTS ----------------
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path, train_arr
            )

            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path, test_arr
            )

            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor_object,
            )

            save_object("final_model/preprocessor.pkl", preprocessor_object)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            logging.info("Data transformation completed successfully")

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
