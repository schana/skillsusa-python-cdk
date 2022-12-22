import os
import pathlib
import typing
from datetime import datetime

import boto3
import pytest
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
    if not any(event):
        print("no new submissions")
        return
    print(event)


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
    s3: S3ServiceResource = boto3.resource("s3")
    bucket: Bucket = s3.Bucket(event.get("bucket"))
    objects: BucketObjectsCollection = bucket.objects.filter(Prefix=event.get("prefix"))
    for obj in objects:
        filename = f"/tmp/{obj.key}"
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        bucket.download_file(obj.key, filename)

    if pytest.main([f"/tmp/{event.get('prefix')}"]) != pytest.ExitCode.OK:
        raise ValueError("validation failed")

    return event


def post_validate(event: dict, context: LambdaContext):
    print(event)
    success: bool = "error" not in event
    prefix: str = event.get("prefix")
    new_prefix = (
        f"{prefix.replace('processing', 'invalid', 1)}"
        f"{datetime.utcnow().isoformat(timespec='seconds')}/"
    )
    if success:
        new_prefix = new_prefix.replace("invalid", "submitted", 1)
    s3: S3ServiceResource = boto3.resource("s3")
    bucket: Bucket = s3.Bucket(event.get("bucket"))
    objects: BucketObjectsCollection = bucket.objects.filter(Prefix=prefix)
    for obj in objects:
        key = obj.key
        new_key = key.replace(prefix, new_prefix, 1)
        print(f"moving {key} to {new_key}")
        bucket.Object(new_key).copy(CopySource=dict(Bucket=bucket.name, Key=key))
        obj.delete()

    return success
