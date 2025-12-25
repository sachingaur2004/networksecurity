# ================= PIPELINE =================
PIPELINE_NAME = "network_security_pipeline"
ARTIFACT_DIR = "Artifacts"

# ================= DATA INGESTION =================
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"

FILE_NAME = "data.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

DATA_INGESTION_TRAIN_TEST_SPLIT_RATION = 0.2
DATA_INGESTION_COLLECTION_NAME = "network_logs"
DATA_INGESTION_DATABASE_NAME = "network_security_db"

# ================= DATA VALIDATION =================
DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_VALID_DIR = "validated"
DATA_VALIDATION_INVALID_DIR = "invalid"

DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "report.yaml"

# ================= DATA TRANSFORMATION =================
DATA_TRANSFORMATION_DIR_NAME = "data_transformation"

TRANSFORMED_TRAIN_DIR_NAME = "transformed_train"
TRANSFORMED_TEST_DIR_NAME = "transformed_test"

TRANSFORMED_TRAIN_FILE_NAME = "train.npy"
TRANSFORMED_TEST_FILE_NAME = "test.npy"

PREPROCESSING_OBJECT_FILE_NAME = "preprocessor.pkl"

DATA_TRANSFORMATION_IMPUTER_PARAMS = {
    "n_neighbors": 3,
    "weights": "uniform"
}

# ================= MODEL TRAINER =================
MODEL_TRAINER_DIR_NAME = "model_trainer"
MODEL_FILE_NAME = "model.pkl"

# ================= TARGET =================
TARGET_COLUMN = "Result"

# ================= SCHEMA =================
import os

SCHEMA_FILE_PATH = os.path.join(
    "networksecurity",
    "schema",
    "schema.yaml"
)
