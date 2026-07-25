"""Demo 2a — Fairness audit with AI Fairness 360.
Computes disparate impact, statistical parity, equal opportunity.
Writes governance/reports/bias_report.html"""
import os, json, pandas as pd, numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import ClassificationMetric

os.makedirs("governance/reports", exist_ok=True)
df = pd.read_csv("data/loans.csv")
df["gender_bin"] = (df["gender"] == "M").astype(int)  # 1 = privileged
feat = ["age", "income", "credit_score", "gender_bin"]
X, y = df[feat], df["approved"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
clf = GradientBoostingClassifier(random_state=0).fit(Xtr, ytr)
pred = clf.predict(Xte)

test_df = Xte.copy(); test_df["approved"] = yte.values
pred_df = Xte.copy(); pred_df["approved"] = pred

bld_true = BinaryLabelDataset(df=test_df, label_names=["approved"],
    protected_attribute_names=["gender_bin"])
bld_pred = bld_true.copy(); bld_pred.labels = pred.reshape(-1, 1)

m = ClassificationMetric(bld_true, bld_pred,
    privileged_groups=[{"gender_bin": 1}],
    unprivileged_groups=[{"gender_bin": 0}])

report = {
    "disparate_impact":      round(m.disparate_impact(), 3),
    "statistical_parity_diff": round(m.statistical_parity_difference(), 3),
    "equal_opportunity_diff":  round(m.equal_opportunity_difference(), 3),
    "average_odds_diff":       round(m.average_odds_difference(), 3),
    "verdict": "FAIL — disparate impact outside 0.8–1.25 (4/5ths rule)"
               if not 0.8 <= m.disparate_impact() <= 1.25 else "PASS",
}
print(json.dumps(report, indent=2))
with open("governance/reports/bias_report.json", "w") as f:
    json.dump(report, f, indent=2)

html = "<h1>Bias audit — loan approval</h1><table border=1 cellpadding=6>" + \
       "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in report.items()) + \
       "</table><p>Reference: EU AI Act Art. 10, NIST AI RMF MEASURE 2.11</p>"
open("governance/reports/bias_report.html", "w").write(html)
print("✓ governance/reports/bias_report.html")
