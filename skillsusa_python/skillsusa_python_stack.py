from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_lambda_python_alpha as lambda_python,
)
from constructs import Construct

from skillsusa_python.static_site import StaticSite

name = "SkillsUSA"


class SkillsusaPythonStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        static_site = StaticSite(self, "StaticSite")

        submission_bucket = s3.Bucket(
            self,
            f"{name}SubmissionBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        results_bucket = s3.Bucket(
            self,
            f"{name}ResultsBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        processor = lambda_python.PythonFunction(
            self,
            f"{name}Processor",
            runtime=lambda_.Runtime.PYTHON_3_9,
            entry="./app/processor",
            index="main.py",
            handler="main",
        )

        submission_bucket.grant_read(processor)
        results_bucket.grant_read_write(processor)
