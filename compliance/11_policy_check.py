"""Demo 6a — Send a model card to OPA and enforce the governance policy."""
import json, requests, sys

model_card = {
    "model_name": "loan-approval",
    "version": "1.0.3",
    "owner": "ml-platform@example.com",
    "performance": {"roc_auc": 0.82},
    "bias":      {"disparate_impact": 0.85},   # ← intentionally failing
    "privacy":   {"epsilon": 1.0},
    "explainability": {"method": "SHAP+EBM"},
    "dataset":   {"consent_obtained": True},
}
r = requests.post("http://opa:8181/v1/data/modelgovernance",
                  json={"input": model_card}, timeout=5)
result = r.json()["result"]
print(json.dumps(result, indent=2))
sys.exit(0 if result.get("allow") else 1)
