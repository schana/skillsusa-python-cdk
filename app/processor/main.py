import itertools
from typing import Any

import processor
import validator


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


def pre_process(event: dict, context) -> dict[Any, list[dict[str, str]]]:
    print(event)
    bucket = event.get("bucket")
    return processor.pre(bucket_name=bucket)


def process(event, context) -> dict[Any, Any]:
    print(event)
    # TODO: turn this into a Sfn Choice
    if not any(event):
        print("no new submissions")
        return dict(videos=[], scores=[], proceed=False)
    else:
        videos, scores = processor.run()
        return dict(videos=videos, scores=scores, proceed=True)


def post_process(event: dict, context):
    print(event)
    proceed = all(run.get("proceed") for run in event)
    if not proceed:
        print("nothing to post process")
        return
    processor.post(
        videos=list(itertools.chain(run.get("videos") for run in event)),
        scores=list(itertools.chain(run.get("scores") for run in event)),
    )
