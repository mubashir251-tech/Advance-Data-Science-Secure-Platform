"""Version the generated dataset with DVC and push to the MinIO remote."""
import json
import os
import pathlib
import subprocess
import sys

REPORT = pathlib.Path("reports/data_versioning.json")


def run(cmd):
    print("$", " ".join(cmd))
    return subprocess.run(cmd, text=True, capture_output=True)


def checked(cmd, allow_codes=(0,)):
    result = run(cmd)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    if result.returncode not in allow_codes:
        raise SystemExit(result.returncode)
    return result


pathlib.Path("reports").mkdir(exist_ok=True)
if not pathlib.Path("data/loans.csv").exists():
    raise SystemExit("data/loans.csv missing — run scripts/gen_data.py first")

if not pathlib.Path(".dvc").exists():
    in_git = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True).returncode == 0
    checked(["dvc", "init", "--subdir", "-q"] if in_git else ["dvc", "init", "--no-scm", "-q"])

checked(["dvc", "remote", "add", "-d", "minio", "s3://mlops/dvc", "-f"])
endpoint = os.environ.get("MINIO_ENDPOINT_URL", "http://localhost:9000")
access_key = os.environ.get("AWS_ACCESS_KEY_ID", "minio")
secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "minio12345")
checked(["dvc", "remote", "modify", "minio", "endpointurl", endpoint])
checked(["dvc", "remote", "modify", "minio", "access_key_id", access_key])
checked(["dvc", "remote", "modify", "minio", "secret_access_key", secret_key])
checked(["dvc", "add", "data/loans.csv"])
checked(["dvc", "push"])

out = {"dataset": "data/loans.csv", "dvc_file": "data/loans.csv.dvc", "remote": "s3://mlops/dvc", "endpoint": endpoint, "status": "pushed"}
REPORT.write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
