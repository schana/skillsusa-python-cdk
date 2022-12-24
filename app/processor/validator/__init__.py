import os
import typing
from datetime import datetime

import boto3
from sneks.validator import main as sneks_validator

if typing.TYPE_CHECKING:
    from mypy_boto3_s3.service_resource import Bucket, BucketObjectsCollection
    from mypy_boto3_s3 import S3ServiceResource
else:
    S3ServiceResource = object
    Bucket = object
    BucketObjectsCollection = object


def run(bucket_name: str, prefix: str) -> None:
    s3: S3ServiceResource = boto3.resource("s3")
    bucket: Bucket = s3.Bucket(bucket_name)
    objects: BucketObjectsCollection = bucket.objects.filter(Prefix=prefix)
    for obj in objects:
        filename = f"/tmp/{obj.key}"
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        bucket.download_file(obj.key, filename)

    sneks_validator.main(test_path=f"/tmp/{prefix}")


def post(bucket_name: str, prefix: str, success: bool) -> bool:
    new_prefix = (
        f"{prefix.replace('processing', 'invalid', 1)}"
        f"{datetime.utcnow().isoformat(timespec='seconds')}/"
    )
    if success:
        new_prefix = new_prefix.replace("invalid", "submitted", 1)
    s3: S3ServiceResource = boto3.resource("s3")
    bucket: Bucket = s3.Bucket(bucket_name)
    objects: BucketObjectsCollection = bucket.objects.filter(Prefix=prefix)
    for obj in objects:
        key = obj.key
        new_key = key.replace(prefix, new_prefix, 1)
        print(f"moving {key} to {new_key}")
        bucket.Object(new_key).copy(CopySource=dict(Bucket=bucket.name, Key=key))
        obj.delete()

    return success
