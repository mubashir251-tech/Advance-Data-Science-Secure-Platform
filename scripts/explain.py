"""SHAP (post-hoc) + InterpretML EBM (glass-box) explanations."""
import pathlib, shap, numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from interpret.glassbox import ExplainableBoostingClassifier
from interpret import preserve
from _common import load, FEATURES
pathlib.Path("reports").mkdir(exist_ok=True)
(X_tr, X_te, y_tr, y_te), _ = load()

# SHAP on a GBM
gbm = GradientBoostingClassifier(n_estimators=120, max_depth=3, random_state=0).fit(X_tr, y_tr)
expl = shap.TreeExplainer(gbm)
sv = expl.shap_values(X_te[:500])
shap.summary_plot(sv, X_te[:500], feature_names=FEATURES, show=False)
import matplotlib.pyplot as plt
plt.savefig("reports/shap_summary.png", bbox_inches="tight"); plt.close()

# Glass-box EBM
ebm = ExplainableBoostingClassifier(random_state=0).fit(X_tr, y_tr)
preserve(ebm.explain_global(), file_name="reports/ebm_global.html")
print("wrote reports/shap_summary.png and reports/ebm_global.html")
