# ================= PIPELINE =================
PIPELINE_NAME = "network_security_pipeline"
ARTIFACT_DIR = "Artifacts"

# ================= S3 / MODEL STORAGE =================
TRAINING_BUCKET_NAME = "networksecurity-training"
SAVED_MODEL_DIR = "final_model"

# ================= DATA INGESTION =================
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"

# This is just the feature-store filename (NOT source CSV)


TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

DATA_INGESTION_TRAIN_TEST_SPLIT_RATION = 0.2

# ✅ MUST MATCH push_data.py + MongoDB
DATA_INGESTION_DATABASE_NAME = "Sachindb"
DATA_INGESTION_COLLECTION_NAME = "NetworkData"

# ================= DATA VALIDATION =================
DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_VALID_DIR = "validated"
DATA_VALIDATION_INVALID_DIR = "invalid"

DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "report.yaml"

# ================= DATA TRANSFORMATION =================
DATA_TRANSFORMATION_DIR_NAME = "data_transformation"

DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "transformed_object"

TRANSFORMED_TRAIN_FILE_NAME = "train.npy"
TRANSFORMED_TEST_FILE_NAME = "test.npy"

PREPROCESSING_OBJECT_FILE_NAME = "preprocessor.pkl"

DATA_TRANSFORMATION_IMPUTER_PARAMS = {
    "missing_values": None,
    "n_neighbors": 3,
    "weights": "uniform",
}

# ================= MODEL TRAINER =================
MODEL_TRAINER_DIR_NAME = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR = "trained_model"
MODEL_FILE_NAME = "model.pkl"

# ================= TARGET =================
TARGET_COLUMN = "Result"

# ================= SCHEMA =================
import os

SCHEMA_FILE_PATH = os.path.join("networksecurity", "schema", "schema.yaml")
