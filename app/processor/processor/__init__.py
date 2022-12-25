import os
import pathlib
import typing

import boto3

from processor import runner
from processor.runner import Score

if typing.TYPE_CHECKING:
    from mypy_boto3_s3.service_resource import Bucket, BucketObjectsCollection
    from mypy_boto3_s3 import S3ServiceResource
    from mypy_boto3_stepfunctions import SFNClient
else:
    S3Client = object
    S3ServiceResource = object
    Bucket = object
    BucketObjectsCollection = object
    SFNClient = object


def start() -> None:
    sfn: SFNClient = boto3.client("stepfunctions")
    sfn.start_execution(stateMachineArn=os.environ["STATE_MACHINE_ARN"])


def pre(bucket_name: str) -> dict[str, list[dict[str, str]]]:
    s3: S3ServiceResource = boto3.resource("s3")
    bucket: Bucket = s3.Bucket(bucket_name)
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
            {"prefix": f"processing/{user}/", "bucket": bucket_name} for user in users
        ]
    )


def run(
    submission_bucket_name: str, static_site_bucket_name: str
) -> (list[str], list[Score]):
    return runner.run(
        submission_bucket_name=submission_bucket_name,
        static_site_bucket_name=static_site_bucket_name,
    )


def post(
    videos: list[str],
    scores: list[Score],
    submission_bucket_name: str,
    static_site_bucket_name: str,
) -> None:
    runner.save_manifest(
        video_names=videos,
        scores=runner.aggregate_scores(scores),
        submission_bucket_name=submission_bucket_name,
        static_site_bucket_name=static_site_bucket_name,
    )
