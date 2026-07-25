"""Create the buckets MLflow + DVC need, with versioning + SSE enabled."""
import boto3
from botocore.client import Config

s3 = boto3.client("s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minio",
    aws_secret_access_key="minio12345",
    config=Config(signature_version="s3v4"))

for bucket in ("mlflow", "dvc"):
    try:
        s3.create_bucket(Bucket=bucket)
    except s3.exceptions.BucketAlreadyOwnedByYou:
        pass
    s3.put_bucket_versioning(Bucket=bucket,
        VersioningConfiguration={"Status": "Enabled"})
    print(f"✓ bucket {bucket} ready (versioning on)")
