# Advance-Data-Science-Secure-Platform
=======
# Advanced Data Science Platform Security
**Topic 122 – EduQual L6 (Diploma in AI Operations)**
*MLOps Integration · Model Governance · AI Ethics Enforcement*

This repository is a single, runnable lab that demonstrates every key learning
objective from my exam brief using **only open-source tools**.  this entire project
runable on a laptop (8 GB RAM is enough) with Docker.

---

## 0. Architecture

```
            ┌──────────────────────────────────────────────────────────┐
            │                  DATA SCIENCE PLATFORM                   │
            │                                                          │
  Data ─▶ MinIO (S3) ─▶ DVC ─▶ JupyterHub ─▶ Airflow ─▶ MLflow Registry
            │             │           │           │            │
            ▼             ▼           ▼           ▼            ▼
        Anonymise    Bandit/Safety  AIF360    Adv. Robust.   Model
        (Faker +     (DevSecOps)    +Inter-   Toolbox        Governance
        OpenDP DP)                  pretML    (poisoning)    + Audit Log
                                                                   │
                                                                   ▼
                                                        Compliance Dashboard
                                                        (EU AI Act / NIST AI RMF
                                                         / ISO 42001 checks)
```

Six objective areas → six folders → six demos to run on stage.

| # | Objective                                | Folder           | Tools                                    |
|---|------------------------------------------|------------------|------------------------------------------|
| 1 | Secure MLOps pipeline & lifecycle        | `pipelines/`     | MLflow, DVC, Airflow, MinIO              |
| 2 | Governance & bias detection              | `governance/`    | AI Fairness 360, InterpretML, SHAP       |
| 3 | Privacy & federated learning             | `privacy/`       | OpenDP, TensorFlow Privacy, PySyft, Faker|
| 4 | Adversarial / poisoning protection       | `adversarial/`   | Adversarial Robustness Toolbox (ART)     |
| 5 | DevSecOps for data science               | `devsecops/`     | Bandit, Safety, pip-audit, trivy, gitleaks |
| 6 | Compliance & ethical AI automation       | `compliance/`    | OPA/Rego policies, audit log, RMF mapping|

---

## 1. Prerequisites

```bash
# Linux / macOS / WSL2
docker --version          # >= 24
docker compose version    # v2
python3 --version         # >= 3.10
```

That's it. Everything else runs inside containers or in `venv`.

---

## 2. One-time bootstrap

```bash
cd Advance-DS-Platform-Sec
bash scripts/bootstrap.sh
```

This will:
1. Create a Python `.venv` and install the ML/security libs (pinned).
2. Start the platform stack (`stack/docker-compose.yml`) — MinIO, MLflow,
   JupyterHub, Airflow, Postgres, OPA.
3. Generate a synthetic but realistic dataset (`data/loans.csv`) where the
   protected attribute is `gender` — perfect for the bias demo.

When it finishes you'll have:

| Service     | URL                    | Login              |
|-------------|------------------------|--------------------|
| MinIO       | http://localhost:9001  | `minio` / `minio12345` |
| MLflow      | http://localhost:5000  | —                  |
| JupyterHub  | http://localhost:8000  | `admin` / `admin`  |
| Airflow     | http://localhost:8080  | `admin` / `admin`  |
| OPA         | http://localhost:8181  | —                  |
| fastapi     | http://localhost:8001  | _                  |_ 
---

## 3. The six demos (run in order)

### Demo 1 — Secure MLOps pipeline
```bash
python pipelines/01_train_with_mlflow.py
dvc add data/loans.csv && dvc push       # versioned data → MinIO
airflow dags trigger secure_training_dag # scheduled retraining
```
**Outcomes:** signed artifact in MLflow Registry, DVC hash, Airflow run, MinIO bucket
versioning enabled, KMS-style server-side encryption header on the object.

### Demo 2 — Governance & bias detection
```bash
python governance/02_bias_audit.py        # AIF360 disparate impact, EO diff
python governance/03_explainability.py    # SHAP + InterpretML report → HTML
```
**Outcomes:** `governance/reports/bias_report.html` and `shap_summary.png`. Mention
EU AI Act Art. 10 (data governance) and Art. 13 (transparency).

### Demo 3 — Privacy-preserving ML
```bash
python privacy/04_anonymize.py            # k-anonymity + pseudonymisation
python privacy/05_differential_privacy.py # OpenDP Laplace mechanism on stats
python privacy/06_dp_sgd_training.py      # TensorFlow-Privacy DP-SGD
python privacy/07_federated_demo.py       # Flower simulated FL across 3 clients
```
**Outcomes:** ε/δ budget printed, model accuracy vs. non-private baseline, FL rounds
in the terminal.

### Demo 4 — Adversarial & poisoning protection
```bash
python adversarial/08_evasion_attack.py   # ART FGSM + PGD on the model
python adversarial/09_poisoning_detect.py # Activation-Clustering defence
python adversarial/10_robust_training.py  # Adversarial training hardening
```
**Outcomes:** accuracy drop under attack, then recovery after robust training,
poisoned-sample cluster plot.

### Demo 5 — DevSecOps for data science
```bash
bash devsecops/scan.sh                    # bandit + safety + pip-audit + gitleaks
trivy fs --severity HIGH,CRITICAL .       # SCA on the whole repo
```
**Outcomes:** `devsecops/reports/security-summary.md` aggregated SARIF.

### Demo 6 — Compliance & ethical AI automation
```bash
python compliance/11_policy_check.py      # Hits OPA with model card JSON
python compliance/12_audit_trail.py       # Append-only hash-chained log
python compliance/13_rmf_mapping.py       # Prints NIST AI RMF + ISO 42001 status
```
**Outcomes:** OPA returning `allow: false` when the model card is missing a bias
score; tamper-evident audit log; coverage matrix of EU AI Act articles.

---

