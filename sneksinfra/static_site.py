from aws_cdk import (
    CfnOutput,
    Duration,
    RemovalPolicy,
    aws_certificatemanager as certificate_manager,
    aws_cognito as cognito,
    aws_cognito_identitypool_alpha as cognito_identity,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_ssm as ssm,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as cloudfront_origins,
)
from constructs import Construct


class StaticSite(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        submission_bucket: s3.Bucket,
        static_site_bucket: s3.Bucket,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        distribution = cloudfront.Distribution(
            self,
            "Distribution",
            domain_names=["sneks.dev", "www.sneks.dev"],
            certificate=certificate_manager.Certificate.from_certificate_arn(
                self,
                "Certificate",
                ssm.StringParameter.value_for_string_parameter(self, "certificate-arn"),
            ),
            default_behavior=cloudfront.BehaviorOptions(
                origin=cloudfront_origins.S3Origin(
                    bucket=static_site_bucket,
                ),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object="index.html",
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.millis(0),
                ),
            ],
            price_class=cloudfront.PriceClass.PRICE_CLASS_100,
        )

        s3_deployment.BucketDeployment(
            self,
            "StaticSiteDeployment",
            destination_bucket=static_site_bucket,
            sources=[s3_deployment.Source.asset("app/sneks/build")],
            retain_on_delete=False,
            distribution=distribution,
        )

        user_pool = cognito.UserPool(
            self,
            "UserPool",
            # TODO: change this before going live
            # deletion_protection=True,
            deletion_protection=False,
            removal_policy=RemovalPolicy.DESTROY,
            self_sign_up_enabled=False,
            sign_in_aliases=cognito.SignInAliases(email=True),
            email=cognito.UserPoolEmail.with_cognito(
                reply_to="admin@sneks.dev",
            ),
            user_invitation=cognito.UserInvitationConfig(
                email_subject="SkillsUSA programming challenge invite",
                email_body=(
                    "Dear {username},\n\n"
                    "Welcome to the SkillsUSA programming challenge! Visit the website at https://www.sneks.dev "
                    "to begin. You can get started by logging in with your email and this temporary password:\n"
                    "\n{####}\n\n"
                    "Have fun and happy coding!"
                ),
            ),
        )

        user_pool_client = user_pool.add_client(
            "Amplify",
            prevent_user_existence_errors=True,
        )

        identity_pool = cognito_identity.IdentityPool(
            self,
            "IdentityPool",
            authentication_providers=cognito_identity.IdentityPoolAuthenticationProviders(
                user_pools=[
                    cognito_identity.UserPoolAuthenticationProvider(
                        user_pool=user_pool,
                        user_pool_client=user_pool_client,
                        disable_server_side_token_check=False,
                    )
                ],
            ),
        )

        submission_bucket.grant_put(
            identity_pool.authenticated_role,
            objects_key_pattern="private/${cognito-identity.amazonaws.com:sub}/*.py",
        )
        submission_bucket.grant_read(
            identity_pool.authenticated_role,
            objects_key_pattern="private/${cognito-identity.amazonaws.com:sub}/*",
        )
        submission_bucket.grant_read(
            identity_pool.authenticated_role,
            objects_key_pattern="submitted/${cognito-identity.amazonaws.com:sub}/*",
        )
        submission_bucket.grant_read(
            identity_pool.authenticated_role,
            objects_key_pattern="invalid/${cognito-identity.amazonaws.com:sub}/*",
        )
        submission_bucket.grant_read(
            identity_pool.authenticated_role,
            objects_key_pattern="processing/${cognito-identity.amazonaws.com:sub}/*",
        )

        CfnOutput(
            self,
            "SneksCloudFrontDomain",
            value=distribution.distribution_domain_name,
            export_name="SneksCloudFrontDomain",
        )

        CfnOutput(
            self,
            "SneksCognitoUserPoolId",
            value=user_pool.user_pool_id,
            export_name="SneksCognitoUserPoolId",
        )

        CfnOutput(
            self,
            "SneksCognitoUserPoolClientId",
            value=user_pool_client.user_pool_client_id,
            export_name="SneksCognitoUserPoolClientId",
        )

        CfnOutput(
            self,
            "SneksCognitoIdentityPoolId",
            value=identity_pool.identity_pool_id,
            export_name="SneksCognitoIdentityPoolId",
        )
