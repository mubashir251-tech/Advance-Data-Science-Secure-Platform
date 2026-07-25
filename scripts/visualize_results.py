"""Create chart artefacts from all JSON outputs produced by the full POC."""
import json
import math
import pathlib

import matplotlib.pyplot as plt

REPORTS = pathlib.Path("reports")
CHARTS = REPORTS / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)


def load_json(name, default=None):
    path = REPORTS / name
    if not path.exists():
        return default
    return json.loads(path.read_text())


def save(fig, name):
    path = CHARTS / name
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path


created = []

bias_before = load_json("bias_before.json")
bias_after = load_json("bias_after.json")
if bias_before and bias_after:
    metrics = list(bias_before.keys())
    x = range(len(metrics))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar([i - 0.18 for i in x], [bias_before[m] for m in metrics], width=0.36, label="Before mitigation")
    ax.bar([i + 0.18 for i in x], [bias_after[m] for m in metrics], width=0.36, label="After reweighing")
    ax.axhline(0, color="#333333", linewidth=1)
    ax.axhline(0.8, color="#d62728", linestyle="--", linewidth=1, label="DI 0.8 threshold")
    ax.set_title("Fairness metrics before/after mitigation")
    ax.set_xticks(list(x), [m.replace("_", "\n") for m in metrics])
    ax.legend(loc="best")
    ax.set_ylabel("Metric value")
    created.append(save(fig, "bias_before_after.png"))

privacy = load_json("privacy_dp.json")
release = load_json("opendp_release.json")
if privacy or release:
    labels, eps, values = [], [], []
    if privacy:
        labels.append("DP-SGD\ntraining")
        eps.append(privacy["epsilon"])
        values.append(privacy["test_accuracy"])
    if release:
        labels.append("OpenDP\nrelease")
        eps.append(release["epsilon"])
        values.append(release["absolute_error"])
    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(labels, eps, marker="o", linewidth=2, label="ε privacy budget")
    ax1.set_ylabel("Epsilon (lower is more private)")
    ax1.set_title("Privacy budget evidence")
    ax1.grid(axis="y", alpha=0.25)
    ax2 = ax1.twinx()
    ax2.bar(labels, values, alpha=0.25, label="Accuracy / error evidence")
    ax2.set_ylabel("Accuracy or absolute release error")
    created.append(save(fig, "privacy_epsilon.png"))

adv = load_json("adversarial.json")
if adv:
    labels = ["Clean", "FGSM", "PGD"]
    vals = [adv["clean_acc"], adv["fgsm_acc"], adv["pgd_acc"]]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, vals)
    ax.axhline(0.55, color="#d62728", linestyle="--", linewidth=1, label="DAG gate threshold")
    ax.set_ylim(0, max(1.0, math.ceil(max(vals) * 10) / 10))
    ax.set_ylabel("Accuracy")
    ax.set_title("Adversarial robustness gate")
    ax.legend(loc="lower right")
    created.append(save(fig, "adversarial_robustness.png"))

poison = load_json("poison_detection.json")
if poison:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(["Precision", "Recall"], [poison["precision"], poison["recall"]])
    ax.set_ylim(0, 1)
    ax.set_title("Poisoning detection quality")
    ax.set_ylabel("Score")
    created.append(save(fig, "poison_detection.png"))

anon = load_json("anonymization.json")
fl = load_json("federated_learning.json")
checks = {
    "Data versioned": bool(load_json("data_versioning.json")),
    "Bias mitigated": bool(bias_after),
    "DP evidence": bool(privacy),
    "FL evidence": bool(fl),
    "k-anonymity": bool(anon),
    "Robustness": bool(adv),
    "Poison detection": bool(poison),
    "Audit chain": pathlib.Path("audit/chain.jsonl").exists(),
    "Compliance": (REPORTS / "nist_ai_rmf.md").exists(),
}
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(list(checks.keys()), [1 if v else 0 for v in checks.values()])
ax.set_xlim(0, 1)
ax.set_xticks([0, 1], ["Missing", "Evidence ready"])
ax.set_title("Objective evidence coverage")
created.append(save(fig, "objective_coverage.png"))

html = ["# MLOps Security Lab — Chart Index\n"]
for path in created:
    html.append(f"## {path.stem.replace('_', ' ').title()}\n")
    html.append(f"![{path.stem}]({path.relative_to(REPORTS)})\n")
(REPORTS / "charts.md").write_text("\n".join(html))

print("wrote charts:")
for path in created:
    print(f" - {path}")
print("wrote reports/charts.md")
