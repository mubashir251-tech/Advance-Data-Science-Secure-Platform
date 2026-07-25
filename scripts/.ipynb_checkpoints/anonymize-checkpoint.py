"""k-anonymity (age binning) + HMAC pseudonymisation of an id column."""
import argparse, hmac, hashlib, pandas as pd
from _common import HMAC_KEY
ap = argparse.ArgumentParser()
ap.add_argument("--in", dest="inp", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--k", type=int, default=5)
a = ap.parse_args()
df = pd.read_csv(a.inp).copy()
df.insert(0, "id", range(len(df)))
df["pseudo_id"] = df["id"].astype(str).apply(
    lambda x: hmac.new(HMAC_KEY, x.encode(), hashlib.sha256).hexdigest()[:16])
df["age_bin"] = pd.cut(df["age"], bins=[20, 30, 40, 50, 60, 70], labels=["20s","30s","40s","50s","60s"])
df["income_band"] = (df["income"] // 10000 * 10000).astype(int)
quasi = ["age_bin", "gender", "income_band"]
sizes = df.groupby(quasi, observed=True).size()
df["group_size"] = df.set_index(quasi).index.map(sizes)
suppressed = df[df["group_size"] < a.k]
df_k = df[df["group_size"] >= a.k].drop(columns=["id","age","income","group_size"])
df_k.to_csv(a.out, index=False)
print(f"wrote {a.out}  kept={len(df_k)}  suppressed={len(suppressed)}  k={a.k}")
