# Project Implementation Evidence Screenshots - MLOps Security Platform

Here is the organized visual evidence

| Req # | Requirement Description | Screenshot Filename (in screenshot folder) |
| :--- | :--- | :--- |
| #1 | End-to-End MLOps Pipeline (Airflow) & Model Tracking | `airflow_dag_graph.png` & `mlflow_experiment_runs.png` |
| #2 | Bias Detection & Mitigation (Metrics & Outcomes) | `bias_before_after_json.png` & `Bias_detection_and_mitigation.png` |
| #3 | Explainability (SHAP on actual model) | `shap_summary_plot.png` |
| #4 | Adversarial Testing (Clean/FGSM/PGD accuracies) | `adversarial.json.png` |
| #5 | Data Poisoning Detection | `poison_detection_cli.png` |
| #6 | Differential Privacy (Epsilon=0.92, clipping, noise) | `dp_training_cli.png` |
| #7 | Federated Learning (Flower server logs) | `flower_server_logs.png` |
| #8 | Anonymization / Pseudonymization (K=5) | `anonymization_k_5_cli.png` |
| #9 | Central Secrets Management - Vulnerability Detected | `bandit_hardcoded_creds_found.png` |
| #10 | Model Registry & Artifact Integrity (Sig & SHA256) | `minio_artifact_bucket.png` & `integrity_failure_cli.png` |
| #11 | Vulnerability Scanning (Bandit, Trivy, pip-audit) | `trivy_fs_results.png` & `bandit_html.png` |
| #12 | Compliance Mapping (ISO, NIST, EU AI Act) | `compliance_report_ui.png` |
| #13 | NIST AI RMF Alignment (Govern, Map, Measure, Manage) | `nist_ai_rmf_checklist.png` |
| #14 | Failure & Recovery (Tamper-evident audit logs) | `audit_chain_broken_cli.png` |
| #15 | API Gateway & Inference | `fastapi_swagger_ui.png` |
