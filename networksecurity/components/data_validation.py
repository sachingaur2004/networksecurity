from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
)
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline.training_pipeline import SCHEMA_FILE_PATH

from scipy.stats import ks_2samp
import pandas as pd
import os
import sys

from networksecurity.utils.main_utils.utils import (
    read_yaml_file,
    write_yaml_file,
)


class DataValidation:

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Validate dataframe columns against schema.yaml
        """
        try:
            schema_columns = set(self.schema_config["columns"].keys())
            dataframe_columns = set(dataframe.columns)

            logging.info(f"Required number of columns: {len(schema_columns)}")
            logging.info(f"Data frame has columns: {len(dataframe_columns)}")

            missing_columns = schema_columns - dataframe_columns
            extra_columns = dataframe_columns - schema_columns

            if missing_columns:
                logging.error(f"Missing columns: {list(missing_columns)}")
                return False

            if extra_columns:
                logging.warning(f"Extra columns found (ignored): {list(extra_columns)}")

            return True

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(
        self,
        base_df: pd.DataFrame,
        current_df: pd.DataFrame,
        threshold: float = 0.05,
    ) -> bool:
        """
        Detect data drift using KS test
        """
        try:
            drift_status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                ks_test = ks_2samp(d1, d2)
                drift_found = ks_test.pvalue < threshold

                if drift_found:
                    drift_status = False

                report[column] = {
                    "p_value": float(ks_test.pvalue),
                    "drift_status": drift_found,
                }

            drift_report_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_path), exist_ok=True)

            write_yaml_file(
                file_path=drift_report_path,
                content=report,
            )

            return drift_status

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Initiate the data validation")

            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = self.read_data(train_file_path)
            test_df = self.read_data(test_file_path)

            # ✅ Schema validation
            if not self.validate_number_columns(train_df):
                raise Exception("Train dataframe schema validation failed")

            if not self.validate_number_columns(test_df):
                raise Exception("Test dataframe schema validation failed")

            # ✅ Drift detection
            drift_status = self.detect_dataset_drift(
                base_df=train_df,
                current_df=test_df,
            )

            # ✅ Save validated data
            os.makedirs(
                os.path.dirname(self.data_validation_config.valid_train_file_path),
                exist_ok=True,
            )

            train_df.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True,
            )

            test_df.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True,
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=drift_status,
                validation_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info("Data validation completed successfully")
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
