from aws_cdk import (
    Stack, RemovalPolicy,
    aws_cognito as cognito,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_lambda_python_alpha as lambda_python
)
from constructs import Construct

name = 'SkillsUSA'


class SkillsusaPythonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user_pool = cognito.UserPool(
            self, f'{name}UserPool',
            deletion_protection=True,
            self_sign_up_enabled=False,
            email=cognito.UserPoolEmail.with_cognito(
                reply_to='',
            ),
            user_invitation=cognito.UserInvitationConfig(
                email_subject='',
                email_body='',
            ),
        )

        bucket = s3.Bucket(
            self, f'{name}Bucket',
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            versioned=True,
            removal_policy=RemovalPolicy.RETAIN,
        )

        processor = lambda_python.PythonFunction(
            self, f'{name}Processor',
            runtime=lambda_.Runtime.PYTHON_3_9,
            entry='./app/processor',
            index='main.py',
            handler='main',
        )
