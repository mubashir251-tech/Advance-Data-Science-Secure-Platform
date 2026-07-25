#!/usr/bin/env bash
# One-shot lab bootstrap. Idempotent: safe to re-run.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "▶ 1/4  Python venv + dependencies"
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip wheel
pip install -r scripts/requirements.txt

echo "▶ 2/4  Starting Docker stack (MinIO, MLflow, JupyterHub, Airflow, OPA)"
docker compose -f stack/docker-compose.yml up -d

echo "▶ 3/4  Waiting for MinIO …"
until curl -fs http://localhost:9000/minio/health/ready >/dev/null; do sleep 2; done
python scripts/init_minio.py

echo "▶ 4/4  Generating synthetic loans dataset"
python scripts/make_dataset.py

echo "✅  Lab is ready. See README.md §3 for the demo order."
