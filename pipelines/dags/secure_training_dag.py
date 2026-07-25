"""Airflow DAG that retrains the model nightly and pushes new versions to the
MLflow Registry. Real production setups add Great Expectations + tests."""
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "mlops-sec",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "secure_training_dag",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["mlops", "security"],
) as dag:

    scan = BashOperator(
        task_id="devsecops_scan",
        bash_command="bash -lc 'cd /opt/lab && bash devsecops/scan.sh'",
    )

    train = BashOperator(
        task_id="train",
        bash_command="bash -lc 'cd /opt/lab && python pipelines/01_train_with_mlflow.py'",
    )

    bias = BashOperator(
        task_id="bias_audit",
        bash_command="bash -lc 'cd /opt/lab && python governance/02_bias_audit.py'",
    )

    policy = BashOperator(
        task_id="policy_gate",
        bash_command="bash -lc 'cd /opt/lab && python compliance/11_policy_check.py'",
    )

    scan >> train >> bias >> policy
