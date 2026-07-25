"""Train a baseline loan-risk model, log + register in MLflow."""
import mlflow, mlflow.sklearn
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from _common import load

(X_tr, X_te, y_tr, y_te), _ = load()
mlflow.set_experiment("loan-risk")
with mlflow.start_run() as run:
    clf = GradientBoostingClassifier(n_estimators=120, max_depth=3, random_state=0)
    clf.fit(X_tr, y_tr)
    pred = clf.predict(X_te); proba = clf.predict_proba(X_te)[:, 1]
    acc, auc = accuracy_score(y_te, pred), roc_auc_score(y_te, proba)
    mlflow.log_metrics({"accuracy": acc, "auc": auc})
    mlflow.sklearn.log_model(clf, artifact_path="model",
                             registered_model_name="loan-risk")
    print(f"run={run.info.run_id} acc={acc:.3f} auc={auc:.3f}")
