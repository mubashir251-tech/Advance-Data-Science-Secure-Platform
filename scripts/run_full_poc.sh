#!/usr/bin/env bash
# One command for the exam POC. It uses the orchestrated DAG and the right venv
# for every dependency family, so you do not run scripts manually one by one.
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ ! -x .venv/bin/python || ! -x .venv-privacy/bin/python || ! -x .venv-flower/bin/python ]]; then
  echo "Missing one or more venvs. Run: bash scripts/bootstrap.sh"
  exit 2
fi

.venv/bin/python dags/secure_loan_pipeline.py
echo
echo "✅ Full POC complete. Open these chart outputs:"
printf ' - reports/charts/%s\n' \
  bias_before_after.png privacy_epsilon.png adversarial_robustness.png \
  poison_detection.png objective_coverage.png
echo " - reports/charts.md"
