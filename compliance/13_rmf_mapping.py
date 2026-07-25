"""Demo 6c — Map controls implemented in this lab to recognised AI standards."""
import json
MAP = {
    "EU AI Act": {
        "Art.9 Risk Mgmt":        ["compliance/11_policy_check.py", "governance/02_bias_audit.py"],
        "Art.10 Data Governance": ["privacy/04_anonymize.py", "scripts/make_dataset.py"],
        "Art.12 Record-keeping":  ["compliance/12_audit_trail.py"],
        "Art.13 Transparency":    ["governance/03_explainability.py"],
        "Art.15 Robustness":      ["adversarial/10_robust_training.py"],
    },
    "NIST AI RMF": {
        "GOVERN-1": ["compliance/policies/governance.rego"],
        "MAP-2.3":  ["governance/02_bias_audit.py"],
        "MEASURE-2.7": ["adversarial/08_evasion_attack.py"],
        "MEASURE-2.10":["privacy/05_differential_privacy.py"],
        "MANAGE-2.4":  ["compliance/12_audit_trail.py"],
    },
    "ISO/IEC 42001": {
        "A.6 AI policy":          ["compliance/policies/governance.rego"],
        "A.8 Data for AI systems":["privacy/04_anonymize.py"],
        "A.9 Information for interested parties": ["governance/03_explainability.py"],
        "A.10 Use of AI systems": ["compliance/11_policy_check.py"],
    },
}
print(json.dumps(MAP, indent=2))
