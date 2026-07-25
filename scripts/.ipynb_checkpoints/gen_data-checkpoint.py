"""Generate a synthetic, intentionally biased loans dataset."""
import numpy as np, pandas as pd, pathlib
rng = np.random.default_rng(42)
N = 5000
gender = rng.choice([0, 1], size=N, p=[0.5, 0.5])           # 0=female, 1=male
age = rng.integers(21, 65, N)
income = rng.normal(45000 + 8000 * gender, 12000, N).clip(15000, 200000)
credit = rng.normal(640 + 30 * gender, 70, N).clip(300, 850)
debt = rng.normal(15000, 6000, N).clip(0, 80000)
# biased label: males get a +0.15 approval boost independent of merit
logit = 0.00005 * income + 0.01 * (credit - 600) - 0.00008 * debt + 0.15 * gender - 2.0
p = 1 / (1 + np.exp(-logit))
approved = (rng.random(N) < p).astype(int)
df = pd.DataFrame({"gender": gender, "age": age, "income": income.round(2),
                   "credit_score": credit.round(0), "debt": debt.round(2),
                   "approved": approved})
out = pathlib.Path("data/loans.csv"); out.parent.mkdir(exist_ok=True)
df.to_csv(out, index=False)
print(f"wrote {out}  rows={len(df)}  approval_rate_by_gender=\n{df.groupby('gender')['approved'].mean()}")
