#!/usr/bin/env bash
# Demo 5 — DevSecOps scan: SAST + dep CVE + secrets.
set +e
mkdir -p devsecops/reports
echo "▶ Bandit (SAST for Python)"
bandit -r pipelines governance privacy adversarial compliance scripts \
       -f json -o devsecops/reports/bandit.json
echo "▶ Safety (CVE in installed deps)"
safety check --json > devsecops/reports/safety.json
echo "▶ pip-audit (PyPI advisory DB)"
pip-audit -f json -o devsecops/reports/pip-audit.json
echo "▶ gitleaks (secrets) — optional, requires gitleaks installed"
command -v gitleaks >/dev/null && gitleaks detect --no-git \
       --report-path devsecops/reports/gitleaks.json || echo "(gitleaks not installed, skipped)"

python - <<'PY'
import json, os, pathlib
out = ["# DevSecOps summary", ""]
for tool in ("bandit","safety","pip-audit","gitleaks"):
    p = pathlib.Path(f"devsecops/reports/{tool}.json")
    if not p.exists(): continue
    try:
        data = json.loads(p.read_text() or "{}")
    except Exception: data = {}
    n = (len(data.get("results", [])) if tool=="bandit"
         else len(data.get("vulnerabilities", [])) if tool=="safety"
         else len(data.get("dependencies", [])) if tool=="pip-audit"
         else len(data) if isinstance(data, list) else 0)
    out.append(f"- **{tool}**: {n} findings → `{p}`")
pathlib.Path("devsecops/reports/security-summary.md").write_text("\n".join(out))
print("\n".join(out))
PY
