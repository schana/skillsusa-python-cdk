import typing

import boto3
import os
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import event_source, SQSEvent

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
    for s3_object in objects:
        print(s3_object.key)


def validate(event, context):
    pass
