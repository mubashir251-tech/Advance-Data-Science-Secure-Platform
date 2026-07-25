"""Differentially-private release of a mean income with OpenDP."""
import argparse
import pandas as pd
import numpy as np
import opendp.prelude as dp

dp.enable_features("contrib")

ap = argparse.ArgumentParser()
ap.add_argument("--query", default="avg_income_by_region")
ap.add_argument("--epsilon", type=float, default=1.0)
a = ap.parse_args()

df = pd.read_csv("data/loans.csv")
df["income"] = pd.to_numeric(df["income"], errors="coerce")
df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["income"]).copy()

data = [float(x) for x in df["income"].tolist()]
if not data:
    raise ValueError("No valid income values after cleaning")
if a.epsilon <= 0:
    raise ValueError("epsilon must be > 0")

bounds = (15000.0, 200000.0)
lower, upper = bounds
n = len(data)

true_mean = float(np.mean(data))
clamped = [min(max(x, lower), upper) for x in data]
sensitivity = (upper - lower) / n
noise = np.random.laplace(0.0, sensitivity / a.epsilon)
dp_mean = float(np.mean(clamped) + noise)

print(f"query={a.query}  bounds=({lower:.0f}, {upper:.0f})  true={true_mean:.2f}  dp(ε={a.epsilon})={dp_mean:.2f}")
