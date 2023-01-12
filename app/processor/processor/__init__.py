import json
import os
import pathlib
import typing

import boto3
import botocore.exceptions
from processor.runner import Score

from processor import runner

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
    sfn.start_execution(
        stateMachineArn=os.environ["STATE_MACHINE_ARN"],
        input=json.dumps({"goto": "nothing"}),
    )


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


def run(submission_bucket_name: str) -> (list[str], list[Score]):
    return runner.run(
        submission_bucket_name=submission_bucket_name,
    )


def record(
    submission_bucket_name: str, video_bucket_name: str
) -> (list[str], list[Score]):
    return runner.record(
        submission_bucket_name=submission_bucket_name,
        video_bucket_name=video_bucket_name,
    )


def post(
    videos: list[str],
    scores: list[dict],
    distribution_id: str,
    static_site_bucket_name: str,
) -> None:
    scores: list[Score] = [Score(**score) for score in scores]
    runner.save_manifest(
        video_names=videos,
        scores=runner.aggregate_scores(scores),
        distribution_id=distribution_id,
        static_site_bucket_name=static_site_bucket_name,
    )


def post_save(video_bucket_name: str, static_site_bucket_name: str, videos: list[str]):
    s3: S3ServiceResource = boto3.resource("s3")
    bucket: Bucket = s3.Bucket(static_site_bucket_name)
    for video in videos:
        key = f"games/{video}"
        # check if object exists
        try:
            bucket.Object(key).load()
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                pass
            else:
                raise
        else:
            raise Exception("trying to overwrite existing file")

        # TODO: validate mp4
        bucket.copy(CopySource={"Bucket": video_bucket_name, "Key": key}, Key=key)
