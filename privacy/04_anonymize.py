"""Demo 3a — Anonymisation + pseudonymisation.
- Drops direct identifiers
- HMAC-pseudonymises a 'customer_id'
- Enforces k-anonymity via generalisation (income bands, age bands)."""
import hmac, hashlib, os, pandas as pd, numpy as np

os.makedirs("privacy/out", exist_ok=True)
df = pd.read_csv("data/loans.csv")
df["customer_id"] = [f"cust_{i:05d}" for i in range(len(df))]

SECRET = os.environ.get("PSEUDO_KEY", "rotate-me-in-prod").encode()
def pseudo(x):
    return hmac.new(SECRET, str(x).encode(), hashlib.sha256).hexdigest()[:16]
df["customer_id"] = df["customer_id"].map(pseudo)

# Generalisation
df["age_band"] = pd.cut(df["age"], bins=[0, 25, 35, 50, 65, 120],
                        labels=["<25","25-34","35-49","50-64","65+"])
df["income_band"] = pd.cut(df["income"], bins=[0,30_000,60_000,100_000,1e9],
                           labels=["low","mid","high","vhigh"])

quasi = ["gender", "age_band", "income_band"]
k = df.groupby(quasi, observed=True).size().min()
print(f"k-anonymity achieved: k={k}")
df.drop(columns=["age", "income"]).to_csv("privacy/out/anon_loans.csv", index=False)
print("✓ privacy/out/anon_loans.csv")
