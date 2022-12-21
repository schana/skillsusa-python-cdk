import os
import typing
import pathlib

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
    for s3_object in objects:
        key = s3_object.key
        new_key = key.replace("private", "processing", 1)
        # Move the new files to a processing area
        print(f"moving {key} to {new_key}")
        bucket.Object(new_key).copy(CopySource=dict(Bucket=bucket.name, Key=key))
        s3_object.delete()
        users.add(pathlib.PurePosixPath(new_key).parts[1])
    return dict(staged=[{"user": user} for user in users])


def validate(event, context):
    print(event)
    pass


def post_validate(event: dict, context: LambdaContext):
    print(event)
    success: bool = event.get("success")
