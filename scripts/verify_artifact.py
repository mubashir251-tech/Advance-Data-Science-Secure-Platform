"""Fail-closed verifier: re-hash + re-HMAC, compare to stored values."""
import argparse, hashlib, hmac, sys, boto3
from _common import MINIO, HMAC_KEY
ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True); ap.add_argument("--version", default="latest")
a = ap.parse_args()
s3 = boto3.client("s3", **MINIO)
def get(k): return s3.get_object(Bucket="mlflow", Key=k)["Body"].read()
base = f"models/{a.model}/{a.version}"
try:
    data = get(f"{base}/model.pkl")
    sha_expected = get(f"{base}/model.pkl.sha256").decode().strip()
    sig_expected = get(f"{base}/model.pkl.sig").decode().strip()
except Exception as e:
    print(f"INTEGRITY FAILURE ❌  missing artifact: {e}"); sys.exit(2)
sha = hashlib.sha256(data).hexdigest()
sig = hmac.new(HMAC_KEY, data, hashlib.sha256).hexdigest()
ok = hmac.compare_digest(sha, sha_expected) and hmac.compare_digest(sig, sig_expected)
print("VERIFIED ✅" if ok else "INTEGRITY FAILURE ❌  hash/signature mismatch")
sys.exit(0 if ok else 1)
