"""Train a baseline loan-risk model, log + register in MLflow."""
import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    log_loss,
    roc_auc_score,
)
from _common import load

(X_tr, X_te, y_tr, y_te), _ = load()

mlflow.set_experiment("loan-risk")

with mlflow.start_run() as run:
    clf = GradientBoostingClassifier(n_estimators=120, max_depth=3, random_state=0)
    clf.fit(X_tr, y_tr)

    pred = clf.predict(X_te)
    proba = clf.predict_proba(X_te)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_te, pred),
        "f1_score": f1_score(y_te, pred, zero_division=0),
        "precision_score": precision_score(y_te, pred, zero_division=0),
        "recall_score": recall_score(y_te, pred, zero_division=0),
    }

    if len(np.unique(y_te)) == 2:
        metrics["log_loss"] = log_loss(y_te, proba)
        metrics["roc_auc_score"] = roc_auc_score(y_te, proba)

    mlflow.log_metrics(metrics)
    mlflow.sklearn.log_model(
        clf,
        artifact_path="model",
        registered_model_name="loan-risk",
    )

    print(f"run={run.info.run_id} " + " ".join(f"{k}={v:.3f}" for k, v in metrics.items()))
