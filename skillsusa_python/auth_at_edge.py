from aws_cdk import (
    CustomResource,
    aws_cognito as cognito,
    aws_sam as sam,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as cloudfront_origins,
    aws_lambda as lambda_,
)
from constructs import Construct


class AuthAtEdge(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        user_pool: cognito.UserPool,
        user_pool_client: cognito.UserPoolClient,
        user_pool_domain: cognito.UserPoolDomain,
        distribution: cloudfront.Distribution,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        redirect_path_sign_in = "/parseauth"
        redirect_path_auth_refresh = "/refreshauth"
        sign_out_url = "/signout"
        redirect_path_sign_out = "/"

        o_auth_scopes = [
            "email",
            "aws.cognito.signin.user.admin",
        ]

        auth_at_edge = sam.CfnApplication(
            self,
            "AuthAtEdge",
            location=sam.CfnApplication.ApplicationLocationProperty(
                application_id="arn:aws:serverlessrepo:us-east-1:520945424137:applications/cloudfront-authorization-at-edge",
                semantic_version="2.1.5",
            ),
            parameters=dict(
                CreateCloudFrontDistribution="false",
                UserPoolArn=user_pool.user_pool_arn,
                UserPoolClientId=user_pool_client.user_pool_client_id,
                EnableSPAMode="false",
                OAuthScopes=",".join(o_auth_scopes),
                RedirectPathAuthRefresh=redirect_path_auth_refresh,
                RedirectPathSignIn=redirect_path_sign_in,
                SignOutUrl=sign_out_url,
                Version="2.1.5",
            ),
        )

        auth_at_edge.node.add_dependency(user_pool_domain)

        check_auth_handler = lambda_.Version.from_version_arn(
            self,
            "CheckAuthHandler",
            auth_at_edge.get_att("Outputs.CheckAuthHandler").to_string(),
        )

        parse_auth_handler = lambda_.Version.from_version_arn(
            self,
            "ParseAuthHandler",
            auth_at_edge.get_att("Outputs.ParseAuthHandler").to_string(),
        )

        sign_out_handler = lambda_.Version.from_version_arn(
            self,
            "SignOutHandler",
            auth_at_edge.get_att("Outputs.SignOutHandler").to_string(),
        )

        refresh_auth_handler = lambda_.Version.from_version_arn(
            self,
            "RefreshAuthHandler",
            auth_at_edge.get_att("Outputs.RefreshAuthHandler").to_string(),
        )

        trailing_slash_handler = lambda_.Version.from_version_arn(
            self,
            "TrailingSlashHandler",
            auth_at_edge.get_att("Outputs.TrailingSlashHandler").to_string(),
        )

        CustomResource(
            self,
            "RedirectUriUpdates",
            service_token=auth_at_edge.get_att(
                "Outputs.UserPoolClientUpdateHandler"
            ).to_string(),
            properties=dict(
                UserPoolArn=user_pool.user_pool_arn,
                UserPoolClientId=user_pool_client.user_pool_client_id,
                CloudFrontDistributionDomainName=distribution.domain_name,
                RedirectPathSignIn=redirect_path_sign_in,
                RedirectPathSignOut=redirect_path_sign_out,
                AlternateDomainNames="",
                OAuthScopes=",".join(o_auth_scopes),
            ),
        )

        cloudfront.LambdaFunctionAssociation(
            event_type=cloudfront.LambdaEdgeEventType.VIEWER_REQUEST,
            lambda_function=check_auth_handler,
        )

        cloudfront.LambdaFunctionAssociation(
            event_type=cloudfront.LambdaEdgeEventType.ORIGIN_REQUEST,
            lambda_function=trailing_slash_handler,
        )

        dummy_origin = cloudfront_origins.HttpOrigin("example.com")

        distribution.add_behavior(
            path_pattern=redirect_path_auth_refresh,
            origin=dummy_origin,
            edge_lambdas=[
                cloudfront.EdgeLambda(
                    event_type=cloudfront.LambdaEdgeEventType.VIEWER_REQUEST,
                    function_version=refresh_auth_handler,
                )
            ],
            viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        )

        distribution.add_behavior(
            path_pattern=redirect_path_sign_in,
            origin=dummy_origin,
            edge_lambdas=[
                cloudfront.EdgeLambda(
                    event_type=cloudfront.LambdaEdgeEventType.VIEWER_REQUEST,
                    function_version=parse_auth_handler,
                )
            ],
            viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        )

        distribution.add_behavior(
            path_pattern=sign_out_url,
            origin=dummy_origin,
            edge_lambdas=[
                cloudfront.EdgeLambda(
                    event_type=cloudfront.LambdaEdgeEventType.VIEWER_REQUEST,
                    function_version=sign_out_handler,
                )
            ],
            viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        )
