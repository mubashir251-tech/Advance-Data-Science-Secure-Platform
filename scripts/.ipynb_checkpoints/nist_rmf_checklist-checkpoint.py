"""Regenerate a NIST AI RMF (Govern/Map/Measure/Manage) checklist from real evidence."""
import json, pathlib
R = pathlib.Path("reports")
def has(p): return (R / p).exists()
rows = [
  ("GOVERN-1.1", "Model card present + OPA-approved", pathlib.Path("model_card.json").exists()),
  ("MAP-2.3",    "Bias measured before mitigation",   has("bias_before.json")),
  ("MEASURE-2.11","Bias mitigated + remeasured",       has("bias_after.json")),
  ("MEASURE-2.7","Adversarial robustness evaluated",   has("adversarial.json")),
  ("MEASURE-2.8","Explainability artefacts produced",  has("ebm_global.html") or has("shap_summary.png")),
  ("MANAGE-2.3", "Tamper-evident audit log in place",  pathlib.Path("audit/chain.jsonl").exists()),
]
md = ["# NIST AI RMF — auto checklist\n", "| ID | Control | Evidence |", "|---|---|---|"]
for k, desc, ok in rows: md.append(f"| {k} | {desc} | {'✅' if ok else '❌'} |")
out = R / "nist_ai_rmf.md"; out.write_text("\n".join(md))
print(out.read_text())
