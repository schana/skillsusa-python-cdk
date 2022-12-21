import os
import subprocess
import typing
import pathlib
from datetime import datetime, timezone

import boto3
from aws_lambda_powertools.utilities.data_classes import event_source, SQSEvent
from aws_lambda_powertools.utilities.typing import LambdaContext

if typing.TYPE_CHECKING:
    from mypy_boto3_s3.service_resource import Bucket, BucketObjectsCollection
    from mypy_boto3_s3 import S3ServiceResource
    from mypy_boto3_stepfunctions import SFNClient
else:
    S3Client = object
    S3ServiceResource = object
    Bucket = object
    SFNClient = object


@event_source(data_class=SQSEvent)
def start_processing(event: SQSEvent, context: LambdaContext):
    sfn: SFNClient = boto3.client("stepfunctions")
    sfn.start_execution(stateMachineArn=os.environ["STATE_MACHINE_ARN"])


def process(event, context):
    print(event)
    print(context)


def pre_process(event: dict, context: LambdaContext):
    s3: S3ServiceResource = boto3.resource("s3")
    bucket: Bucket = s3.Bucket(event.get("bucket"))
    objects: BucketObjectsCollection = bucket.objects.filter(Prefix="private/")
    users = set()
    for obj in objects:
        key = obj.key
        new_key = key.replace("private", "processing", 1)
        # Move the new files to a processing area
        print(f"moving {key} to {new_key}")
        bucket.Object(new_key).copy(CopySource=dict(Bucket=bucket.name, Key=key))
        obj.delete()
        users.add(pathlib.PurePosixPath(new_key).parts[1])
    return dict(
        staged=[
            {"prefix": f"processing/{user}/", "bucket": event.get("bucket")}
            for user in users
        ]
    )


def validate(event, context):
    print(event)
    print(os.environ)
    s3: S3ServiceResource = boto3.resource("s3")
    bucket: Bucket = s3.Bucket(event.get("bucket"))
    objects: BucketObjectsCollection = bucket.objects.filter(Prefix=event.get("prefix"))
    for obj in objects:
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key)
    timeout_seconds = 30
    subprocess.run(
        ["pytest"], cwd=event.get("prefix"), timeout=timeout_seconds, env={}, check=True
    )
    return event


def post_validate(event: dict, context: LambdaContext):
    print(event)
    success: bool = event.get("success")
    prefix: str = event.get("prefix")
    new_prefix = (
        f"{prefix.replace('processing', 'invalid', 1)}"
        f"{datetime.now(timezone.utc).isoformat(timespec='seconds')}"
    )
    if success:
        new_prefix = new_prefix.replace("processing", "submitted", 1)
    s3: S3ServiceResource = boto3.resource("s3")
    bucket: Bucket = s3.Bucket(event.get("bucket"))
    objects: BucketObjectsCollection = bucket.objects.filter(Prefix=prefix)
    for obj in objects:
        key = obj.key
        new_key = key.replace(prefix, new_prefix, 1)
        print(f"moving {key} to {new_key}")
        bucket.Object(new_key).copy(CopySource=dict(Bucket=bucket.name, Key=key))
        obj.delete()
