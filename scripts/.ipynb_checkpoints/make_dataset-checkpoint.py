"""Synthetic loan-approval dataset with an intentional gender bias so the
fairness demo has something to find."""
import numpy as np
import pandas as pd
import os

rng = np.random.default_rng(42)
N = 5000

gender = rng.choice(["M", "F"], size=N, p=[0.55, 0.45])
age = rng.integers(21, 65, size=N)
income = rng.normal(55000, 18000, size=N).clip(15000, 200000)
credit = rng.normal(680, 70, size=N).clip(350, 850)

base = 0.000015 * income + 0.01 * credit - 10.0
logits = base + np.where(gender == "F", -0.7, 0.0)

approved = (1 / (1 + np.exp(-logits)) > rng.random(N)).astype(int)

df = pd.DataFrame({
    "gender": gender,
    "age": age,
    "income": income.round(2),
    "credit_score": credit.round(),
    "approved": approved,
})

os.makedirs("data", exist_ok=True)
df.to_csv("data/loans.csv", index=False)

print(df.groupby("gender")["approved"].mean())
print(df["approved"].value_counts())
print("✓ data/loans.csv written")
