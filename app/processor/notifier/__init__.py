import json
import os
import typing

import boto3

if typing.TYPE_CHECKING:
    from mypy_boto3_sns import SNSClient
else:
    SNSClient = object


def send(event: dict) -> None:
    topic_arn: str = os.environ["sns_topic_arn"]
    sns: SNSClient = boto3.client("sns")
    sns.publish(
        Message=json.dumps(event, indent=4),
        Subject=f"Sneks workflow status changed: {event.get('detail', {}).get('status', 'unknown')}",
        TopicArn=topic_arn,
    )
