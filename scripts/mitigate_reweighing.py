"""Reweighing (pre-processing) — re-train, re-measure, write bias_after.json."""
import json, pathlib, pandas as pd
from aif360.datasets import BinaryLabelDataset
from aif360.algorithms.preprocessing import Reweighing
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric
from sklearn.ensemble import GradientBoostingClassifier
from _common import load, FEATURES, LABEL

(X_tr, X_te, y_tr, y_te), _ = load()
df_tr = pd.DataFrame(X_tr, columns=FEATURES); df_tr[LABEL] = y_tr
ds_tr = BinaryLabelDataset(df=df_tr, label_names=[LABEL], protected_attribute_names=["gender"])
rw = Reweighing(unprivileged_groups=[{"gender": 0}], privileged_groups=[{"gender": 1}])
ds_tr_rw = rw.fit_transform(ds_tr)
clf = GradientBoostingClassifier(n_estimators=120, max_depth=3, random_state=0)
clf.fit(X_tr, y_tr, sample_weight=ds_tr_rw.instance_weights)
df_te = pd.DataFrame(X_te, columns=FEATURES); df_te[LABEL] = y_te
df_pred = df_te.copy(); df_pred[LABEL] = clf.predict(X_te)
ds_t = BinaryLabelDataset(df=df_te, label_names=[LABEL], protected_attribute_names=["gender"])
ds_p = BinaryLabelDataset(df=df_pred, label_names=[LABEL], protected_attribute_names=["gender"])
m = BinaryLabelDatasetMetric(ds_t, [{"gender": 0}], [{"gender": 1}])
cm = ClassificationMetric(ds_t, ds_p, [{"gender": 0}], [{"gender": 1}])
after = {
    "disparate_impact": m.disparate_impact(),
    "statistical_parity_diff": m.statistical_parity_difference(),
    "equal_opportunity_diff": cm.equal_opportunity_difference(),
    "avg_odds_diff": cm.average_odds_difference(),
}
pathlib.Path("reports/bias_after.json").write_text(json.dumps(after, indent=2))
before = json.loads(pathlib.Path("reports/bias_before.json").read_text())
print(f"{'metric':30s} {'before':>10s} {'after':>10s}")
for k in before:
    print(f"{k:30s} {before[k]:>10.3f} {after[k]:>10.3f}")
