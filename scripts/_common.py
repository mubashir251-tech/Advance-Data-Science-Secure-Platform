"""Shared helpers: MLflow + MinIO config, dataset loader."""
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# MLflow + MinIO environment configuration
os.environ.setdefault("MLFLOW_TRACKING_URI", "http://localhost:5000")
os.environ.setdefault("MLFLOW_S3_ENDPOINT_URL", "http://localhost:9000")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "minio")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "minio12345")

MINIO = dict(
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minio",
    aws_secret_access_key="minio12345",
)

# Demo-only; in real life use a proper secrets manager
HMAC_KEY = b"demo-hmac-key-rotate-in-prod"

# Features and label for data/loans.csv
FEATURES = ["age", "income", "credit_score", "gender"]
LABEL = "approved"


def load(test_size: float = 0.25, seed: int = 42):
    """
    Load the loans dataset, encode categorical features/labels,
    and return a train/test split plus the full DataFrame.
    """
    df = pd.read_csv("data/loans.csv").copy()

    # Encode gender (F/M/etc) as numeric
    df["gender"] = LabelEncoder().fit_transform(df["gender"].astype(str))

    # Make sure approved is numeric 0/1
    # If it's already 0/1 ints, this keeps it; if it's strings, this encodes them.
    df[LABEL] = LabelEncoder().fit_transform(df[LABEL].astype(str))

    X = df[FEATURES].values
    y = df[LABEL].values

    # Stratified split so both classes appear in train and test
    return train_test_split(
        X, y, test_size=test_size, random_state=seed, stratify=y
    ), df
