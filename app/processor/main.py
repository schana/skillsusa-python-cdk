import itertools
from typing import Any
import random

import processor
import validator
import notifier


def send_notification(event: dict, context):
    print(event)
    notifier.send(event)


def start_processing(event: dict, context):
    print(event)
    processor.start()


def validate(event: dict, context):
    print(event)
    bucket = event.get("bucket")
    prefix = event.get("prefix")
    validator.run(bucket_name=bucket, prefix=prefix)
    return event


def post_validate(event: dict, context) -> bool:
    print(event)
    bucket = event.get("bucket")
    prefix = event.get("prefix")
    success: bool = "error" not in event
    return validator.post(bucket_name=bucket, prefix=prefix, success=success)


def post_validate_reduce(event: dict, context) -> bool:
    return any(event)


def pre_process(event: dict, context) -> dict[Any, list[dict[str, str]]]:
    print(event)
    bucket = event.get("bucket")
    return processor.pre(bucket_name=bucket)


def process(event, context) -> dict[Any, Any]:
    print(event)
    submission_bucket_name = event.get("submission_bucket")
    videos, scores = processor.run(
        submission_bucket_name=submission_bucket_name,
    )
    result = dict(videos=videos, scores=scores, proceed=True)
    return result


def record(event, context) -> dict[Any, Any]:
    print(event)
    # Seed random to prevent uuid4 collisions due to lambda optimizations?
    random.seed(context.aws_request_id)
    submission_bucket_name = event.get("submission_bucket")
    video_bucket_name = event.get("video_bucket")
    videos, scores = processor.record(
        submission_bucket_name=submission_bucket_name,
        video_bucket_name=video_bucket_name,
    )
    result = dict(videos=videos, scores=scores, proceed=True)
    return result


def post_process(event: dict, context):
    print(event)
    distribution_id = event.get("distribution_id")
    static_site_bucket_name = event.get("static_site_bucket")
    result = event.get("result")
    proceed = all(run.get("proceed") for run in result)
    if not proceed:
        print("nothing to post process")
        return
    processor.post(
        videos=list(itertools.chain.from_iterable(run.get("videos") for run in result)),
        scores=list(itertools.chain.from_iterable(run.get("scores") for run in result)),
        distribution_id=distribution_id,
        static_site_bucket_name=static_site_bucket_name,
    )


def post_process_save(event: dict, context):
    print(event)
    video_bucket_name = event.get("video_bucket")
    static_site_bucket_name = event.get("static_site_bucket")
    result = event.get("result")
    proceed: bool = all(run.get("proceed") for run in result)
    videos: list[str] = list(
        itertools.chain.from_iterable(run.get("videos") for run in result)
    )
    scores: list[dict] = list(
        itertools.chain.from_iterable(run.get("scores") for run in result)
    )
    if proceed:
        processor.post_save(
            video_bucket_name=video_bucket_name,
            static_site_bucket_name=static_site_bucket_name,
            videos=videos,
        )
    return dict(videos=videos, scores=scores, proceed=proceed)
