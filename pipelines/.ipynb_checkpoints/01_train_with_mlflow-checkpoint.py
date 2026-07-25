"""Demo 1 — Secure MLOps lifecycle.
Trains a sklearn model, logs to MLflow, signs the artifact, registers it."""
import hashlib, json, os, mlflow, pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import mlflow.sklearn

os.environ.setdefault("MLFLOW_S3_ENDPOINT_URL", "http://localhost:9000")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "minio")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "minio12345")
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("loan-approval")

df = pd.read_csv("data/loans.csv")
X = pd.get_dummies(df.drop(columns=["approved"]), columns=["gender"], drop_first=True)
y = df["approved"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)

with mlflow.start_run() as run:
    model = GradientBoostingClassifier(random_state=0).fit(Xtr, ytr)
    auc = roc_auc_score(yte, model.predict_proba(Xte)[:, 1])
    mlflow.log_metric("roc_auc", auc)
    mlflow.sklearn.log_model(model, artifact_path="model",
        registered_model_name="loan-approval")

    # ── "signing" the artifact: SHA-256 of the serialized model
    import joblib, tempfile
    with tempfile.NamedTemporaryFile() as f:
        joblib.dump(model, f.name)
        digest = hashlib.sha256(open(f.name, "rb").read()).hexdigest()
    mlflow.set_tag("artifact_sha256", digest)
    mlflow.log_dict({"sha256": digest, "run_id": run.info.run_id},
                    "model_signature.json")
    print(f"✓ AUC={auc:.3f}  sha256={digest[:16]}…  run={run.info.run_id}")
