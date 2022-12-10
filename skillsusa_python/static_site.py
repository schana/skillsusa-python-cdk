from aws_cdk import (
    RemovalPolicy,
    CfnOutput,
    aws_cognito as cognito,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as cloudfront_origins,
    aws_iam as iam,
)
from constructs import Construct

from skillsusa_python.auth_at_edge import AuthAtEdge


class StaticSite(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        static_site_bucket = s3.Bucket(
            self,
            "StaticSiteBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            versioned=True,
            removal_policy=RemovalPolicy.RETAIN,
        )

        origin_access_identity = cloudfront.OriginAccessIdentity(
            self,
            "OriginAccessIdentity",
        )

        distribution = cloudfront.Distribution(
            self,
            "Distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=cloudfront_origins.S3Origin(
                    bucket=static_site_bucket,
                    origin_access_identity=origin_access_identity,
                ),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object="index.html",
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_page_path="/notfound.html",
                ),
            ],
            price_class=cloudfront.PriceClass.PRICE_CLASS_100,
        )

        static_site_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:ListBucket"],
                principals=[origin_access_identity.grant_principal],
                resources=[static_site_bucket.bucket_arn],
            )
        )

        static_site_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                principals=[origin_access_identity.grant_principal],
                resources=[static_site_bucket.arn_for_objects("*")],
            )
        )

        user_pool = cognito.UserPool(
            self,
            "UserPool",
            deletion_protection=True,
            self_sign_up_enabled=False,
            email=cognito.UserPoolEmail.with_cognito(
                reply_to="",
            ),
            user_invitation=cognito.UserInvitationConfig(
                email_subject="",
                email_body="",
            ),
        )

        user_pool_client = user_pool.add_client(
            "LambdaAtEdge",
            generate_secret=True,
            o_auth=cognito.OAuthSettings(
                callback_urls=[f"https://{distribution.distribution_domain_name}"],
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True,
                ),
            ),
        )

        user_pool_domain = user_pool.add_domain(
            "HostedUI",
            cognito_domain=cognito.CognitoDomainOptions(domain_prefix="auth-static"),
        )

        CfnOutput(
            self,
            "CloudFrontURL",
            value=f"https://{distribution.distribution_domain_name}",
            description="Path of static site",
            export_name="CloudFrontURL",
        )

        AuthAtEdge(
            self,
            "AuthAtEdge",
            user_pool=user_pool,
            user_pool_client=user_pool_client,
            user_pool_domain=user_pool_domain,
            distribution=distribution,
        )
