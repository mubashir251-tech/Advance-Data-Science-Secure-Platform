"""CI gate — reads reports/adversarial.json, exits non-zero if below threshold."""
import argparse, json, sys, pathlib
ap = argparse.ArgumentParser(); ap.add_argument("--min-robust-acc", type=float, default=0.65)
a = ap.parse_args()
r = json.loads(pathlib.Path("reports/adversarial.json").read_text())
worst = min(r["fgsm_acc"], r["pgd_acc"])
print(f"worst_robust_acc={worst:.3f}  threshold={a.min_robust_acc}")
sys.exit(0 if worst >= a.min_robust_acc else 1)
