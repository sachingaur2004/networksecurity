# 🛡️ Network Security - Phishing Detection ML Pipeline

An end-to-end **Machine Learning-based Network Security system** designed to detect phishing/malicious web activity from network and website-related data.

The project follows a modular ML pipeline covering **data ingestion, data validation, data transformation, model training, model evaluation, model persistence, and API-based prediction**. MongoDB is used for data storage/ingestion, while FastAPI provides training and prediction endpoints.

---

## 📌 Project Overview

Phishing websites and malicious web activities can be identified using characteristics extracted from URLs and web pages. This project builds a machine-learning classification pipeline that processes such features and produces predictions for new input data.

### Main Objectives

- Ingest network/security data from MongoDB.
- Validate input data and check for data quality/drift.
- Transform and preprocess features for machine learning.
- Train and compare classification models.
- Save the trained model and preprocessing object.
- Track experiments/model development with MLflow.
- Expose the trained model through a FastAPI application.
- Accept CSV files for prediction and generate prediction output.

---

## 🚀 Key Features

- End-to-end modular ML pipeline
- MongoDB-based data ingestion
- Data validation and drift detection
- Feature preprocessing and transformation
- Multiple classification algorithms
- Hyperparameter tuning/model comparison
- MLflow experiment tracking
- Serialized model and preprocessor
- FastAPI REST API
- CSV upload for batch prediction
- Prediction output saved as CSV
- Docker-based deployment support
- AWS/cloud-oriented project structure

---

## 🏗️ ML Pipeline Architecture

```text
                    ┌──────────────────────┐
                    │      CSV / Data      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      MongoDB         │
                    │  Data Ingestion      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Data Validation    │
                    │ Schema / Data Drift  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Data Transformation  │
                    │ Preprocessing/Features│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Model Training    │
                    │ Model Comparison &   │
                    │ Hyperparameter Tuning│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Trained Model +      │
                    │ Preprocessor         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │     Prediction       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Prediction Output    │
                    │       CSV            │
                    └──────────────────────┘
