from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta

default_args = {
    "owner": "mlops-sec",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="secure_enterprise_mlops",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["mlops", "security", "enterprise"],
) as dag:

    from airflow.operators.bash import BashOperator
    
    # ==========================
    # Data Preparation
    # ==========================
    with TaskGroup("data_preparation") as data_preparation:


        init_minio = BashOperator(
            task_id="initialize_minio",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            python scripts/init_minio.py
            '
            """,
        )

        generate_dataset = BashOperator(
            task_id="generate_dataset",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            python scripts/make_dataset.py
            '
            """,
        )

        version_dataset = BashOperator(
            task_id="version_dataset",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            source /opt/lab/.venv/bin/activate &&
            python scripts/version_data.py
            '
            """,
        )

        init_minio >> generate_dataset >> version_dataset

    from airflow.operators.bash import BashOperator

    # ==========================
    # Core MLOps
    # ==========================
    with TaskGroup("core_mlops") as core_mlops:
 

        devsecops_scan = BashOperator(
            task_id="devsecops_scan",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            bash devsecops/scan.sh
            '
            """,
        )

        train_model = BashOperator(
            task_id="train_model",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            python pipelines/01_train_with_mlflow.py
            '
            """,
        )   

        sign_model = BashOperator(
            task_id="sign_model",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            python scripts/sign_artifact.py
            '
            """,
        )

        verify_model = BashOperator(
            task_id="verify_model",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            python scripts/verify_artifact.py
            '
            """,
        )

        bias_audit = BashOperator(
            task_id="bias_audit",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            python governance/02_bias_audit.py
            '
            """,
        )

        bias_mitigation = BashOperator(
            task_id="bias_mitigation",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            python scripts/mitigate_reweighing.py
            '
            """,
        )

        explainability = BashOperator(
            task_id="explainability",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            python governance/03_explainability.py
            '
            """,
        )

        devsecops_scan >> train_model
        train_model >> sign_model
        sign_model >> verify_model
        verify_model >> bias_audit
        bias_audit >> bias_mitigation
        bias_mitigation >> explainability

    # ==========================
    # Privacy
    # ==========================
    with TaskGroup("privacy") as privacy:
        
        differential_privacy = BashOperator(
            task_id="differential_privacy",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            source /opt/lab/.venv-privacy/bin/activate &&
            python privacy/05_differential_privacy.py
            '
            """,
        )

        dp_sgd_training = BashOperator(
            task_id="dp_sgd_training",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            source /opt/lab/.venv-privacy/bin/activate &&
            python privacy/06_dp_sgd_training.py
            '
            """,
        )

        differential_privacy >> dp_sgd_training

    # ==========================
    # Federated Learning
    # ==========================
    with TaskGroup("federated_learning") as federated_learning:
            
        flower_demo = BashOperator(
            task_id="flower_demo",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            source /opt/lab/.venv-flower/bin/activate &&
            bash scripts/flower_demo.sh
            '
            """,
        )

        anonymization = BashOperator(
            task_id="anonymization",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            source /opt/lab/.venv-flower/bin/activate &&
            python privacy/04_anonymize.py
            '
            """,
        )

        flower_demo >> anonymization

    # ==========================
    # Adversarial Security
    # ==========================
    with TaskGroup("adversarial_security") as adversarial_security:
        
        adversarial_testing = BashOperator(
            task_id="adversarial_testing",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            source /opt/lab/.venv-flower/bin/activate &&
            python scripts/adv_fgsm.py
            '
            """,
        )

        poison_detection = BashOperator(
            task_id="poison_detection",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            source /opt/lab/.venv-flower/bin/activate &&
            python scripts/poison_detect.py
            '
            """,
        )

        robustness_gate = BashOperator(
            task_id="robustness_gate",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            source /opt/lab/.venv-flower/bin/activate &&
            python scripts/robustness_gate.py
            '
            """,
        )

        adversarial_testing >> poison_detection >> robustness_gate

    # ==========================
    # Compliance
    # ==========================
    with TaskGroup("compliance") as compliance:
        
        policy_gate = BashOperator(
            task_id="policy_gate",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            python compliance/11_policy_check.py
            '
            """,
        )

        audit_trail = BashOperator(
            task_id="audit_trail",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            python compliance/12_audit_trail.py
            '
            """,
        )

        verify_chain = BashOperator(
            task_id="verify_chain",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            python scripts/verify_chain.py
            '
            """,
        )

        nist_rmf = BashOperator(
            task_id="nist_rmf_mapping",
            bash_command="""
            bash -lc '
            cd /opt/lab &&
            python compliance/13_rmf_mapping.py
            '
            """,
        )

        pipeline_success = BashOperator(
            task_id="pipeline_success",
            bash_command="echo 'Secure Enterprise MLOps Pipeline Completed Successfully'",
        )

        policy_gate >> audit_trail >> verify_chain >> nist_rmf >> pipeline_success

    # Workflow

    data_preparation >> core_mlops

    core_mlops >> [privacy, federated_learning]

    [privacy, federated_learning] >> adversarial_security
    
    adversarial_security >> compliance
