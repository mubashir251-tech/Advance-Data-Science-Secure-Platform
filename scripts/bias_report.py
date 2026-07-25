"""AIF360 fairness metrics on the loans dataset."""
import argparse, json, pathlib, pandas as pd
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric
from sklearn.ensemble import GradientBoostingClassifier
from _common import load, FEATURES, LABEL

ap = argparse.ArgumentParser()
ap.add_argument("--protected", default="gender"); ap.add_argument("--label", default="approved")
ap.add_argument("--out", default="reports/bias_before.json")
a = ap.parse_args()
(X_tr, X_te, y_tr, y_te), df = load()
clf = GradientBoostingClassifier(n_estimators=120, max_depth=3, random_state=0).fit(X_tr, y_tr)
df_te = pd.DataFrame(X_te, columns=FEATURES); df_te[LABEL] = y_te
df_pred = df_te.copy(); df_pred[LABEL] = clf.predict(X_te)
priv = [{a.protected: 1}]; unpriv = [{a.protected: 0}]
ds_t = BinaryLabelDataset(df=df_te, label_names=[LABEL], protected_attribute_names=[a.protected])
ds_p = BinaryLabelDataset(df=df_pred, label_names=[LABEL], protected_attribute_names=[a.protected])
m = BinaryLabelDatasetMetric(ds_t, unprivileged_groups=unpriv, privileged_groups=priv)
cm = ClassificationMetric(ds_t, ds_p, unprivileged_groups=unpriv, privileged_groups=priv)
report = {
    "disparate_impact": m.disparate_impact(),
    "statistical_parity_diff": m.statistical_parity_difference(),
    "equal_opportunity_diff": cm.equal_opportunity_difference(),
    "avg_odds_diff": cm.average_odds_difference(),
}
pathlib.Path(a.out).parent.mkdir(exist_ok=True)
pathlib.Path(a.out).write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
