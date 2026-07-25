"""Demo 2b — Explainability with SHAP + InterpretML (glassbox EBM).
Saves: governance/reports/shap_summary.png + ebm_global.html"""
import os, pandas as pd, shap, matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from interpret.glassbox import ExplainableBoostingClassifier
from interpret import show, preserve

os.makedirs("governance/reports", exist_ok=True)
df = pd.read_csv("data/loans.csv")
X = pd.get_dummies(df.drop(columns=["approved"]), columns=["gender"], drop_first=True)
y = df["approved"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)

# SHAP on the GBM
clf = GradientBoostingClassifier(random_state=0).fit(Xtr, ytr)
expl = shap.TreeExplainer(clf)
sv = expl.shap_values(Xte.iloc[:500])
shap.summary_plot(sv, Xte.iloc[:500], show=False)
plt.tight_layout()
plt.savefig("governance/reports/shap_summary.png", dpi=120)
plt.close()

# Glassbox model (intrinsically interpretable)
ebm = ExplainableBoostingClassifier(random_state=0).fit(Xtr, ytr)
preserve(ebm.explain_global(), file_name="governance/reports/ebm_global.html")
print("✓ shap_summary.png + ebm_global.html written")
