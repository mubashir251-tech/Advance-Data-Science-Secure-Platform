"""Download the latest model artifact, SHA-256 + HMAC-sign it, push back."""
import argparse, hashlib, hmac, io, boto3, mlflow
from mlflow.tracking import MlflowClient
from _common import MINIO, HMAC_KEY

ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True); ap.add_argument("--version", default="latest")
a = ap.parse_args()

c = MlflowClient()
vs = c.search_model_versions(f"name='{a.model}'")
v = max(vs, key=lambda x: int(x.version)) if a.version == "latest" else \
    next(x for x in vs if x.version == a.version)
local = mlflow.artifacts.download_artifacts(f"models:/{a.model}/{v.version}")
import pathlib, glob
pkl = next(iter(glob.glob(f"{local}/**/model.pkl", recursive=True)), None) \
      or next(iter(glob.glob(f"{local}/**/*.pkl", recursive=True)))
data = pathlib.Path(pkl).read_bytes()
sha = hashlib.sha256(data).hexdigest()
sig = hmac.new(HMAC_KEY, data, hashlib.sha256).hexdigest()
s3 = boto3.client("s3", **MINIO)
key = f"models/{a.model}/{v.version}"
s3.put_object(Bucket="mlflow", Key=f"{key}/model.pkl", Body=data)
s3.put_object(Bucket="mlflow", Key=f"{key}/model.pkl.sha256", Body=sha.encode())
s3.put_object(Bucket="mlflow", Key=f"{key}/model.pkl.sig", Body=sig.encode())
# also publish a "latest" pointer
bucket = "mlflow"

for suf in ("model.pkl", "model.pkl.sha256", "model.pkl.sig"):
    s3.copy_object(
        Bucket=bucket,
        CopySource={"Bucket": bucket, "Key": f"{key}/{suf}"},
        Key=f"models/{a.model}/latest/{suf}"
    )
print(f"SIGNED ✅  version={v.version}  sha256={sha[:16]}…")
