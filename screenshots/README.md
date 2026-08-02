# Exam Evidence Screenshots - MLOps Security Platform

Here is the organized visual evidence

| Requirement Description | Screenshot Filename (in screenshot folder) |
| :--- | :--- | :--- |
| End-to-End MLOps Pipeline (Airflow) & Model Tracking | `airflow_dag_graph.png` & `mlflow_experiment_runs.png` |
| Bias Detection & Mitigation (Metrics & Outcomes) | `bias_before_after_json.png` & `Bias_detection_and_mitigation.png` |
| Explainability (SHAP on actual model) | `shap_summary_plot.png` |
| Adversarial Testing (Clean/FGSM/PGD accuracies) | `adversarial.json.png` |
| Data Poisoning Detection | `poison_detection_cli.png` |
| Differential Privacy (Epsilon=0.92, clipping, noise) | `dp_training_cli.png` |
| Federated Learning (Flower server logs) | `flower_server_logs.png` |
| Anonymization / Pseudonymization (K=5) | `anonymization_k_5_cli.png` |
| Central Secrets Management - Vulnerability Detected | `bandit_hardcoded_creds_found.png` |
| Model Registry & Artifact Integrity (Sig & SHA256) | `minio_artifact_bucket.png` & `integrity_failure_cli.png` |
| Vulnerability Scanning (Bandit, Trivy, pip-audit) | `trivy_fs_results.png` & `bandit_html.png` |
| Compliance Mapping (ISO, NIST, EU AI Act) | `compliance_report_ui.png` |
| NIST AI RMF Alignment (Govern, Map, Measure, Manage) | `nist_ai_rmf_checklist.png` |
| Failure & Recovery (Tamper-evident audit logs) | `audit_chain_broken_cli.png` |
| API Gateway & Inference | `fastapi_swagger_ui.png` |