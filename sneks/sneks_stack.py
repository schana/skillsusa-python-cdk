from aws_cdk import (
    CfnOutput,
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_lambda_event_sources as lambda_event_sources,
    aws_lambda_python_alpha as lambda_python,
)
from constructs import Construct

from sneks.static_site import StaticSite


class SneksStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        submission_bucket = s3.Bucket(
            self,
            "SubmissionBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.DESTROY,
            cors=[
                s3.CorsRule(
                    allowed_headers=["*"],
                    allowed_methods=[s3.HttpMethods.PUT],
                    allowed_origins=["*"],
                )
            ],
        )

        results_bucket = s3.Bucket(
            self,
            "ResultsBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        processor = lambda_python.PythonFunction(
            self,
            "Processor",
            runtime=lambda_.Runtime.PYTHON_3_9,
            entry="./app/processor",
            index="main.py",
            handler="main",
        )

        submission_bucket.grant_read(processor)
        results_bucket.grant_read_write(processor)

        submission_event = lambda_event_sources.S3EventSource(
            bucket=submission_bucket,
            events=[s3.EventType(s3.EventType.OBJECT_CREATED_PUT)],
        )

        processor.add_event_source(submission_event)

        static_site = StaticSite(
            self, "StaticSite", submission_bucket=submission_bucket
        )

        CfnOutput(
            self,
            "SneksSubmissionBucket",
            value=submission_bucket.bucket_name,
            export_name="SneksSubmissionBucket",
        )
