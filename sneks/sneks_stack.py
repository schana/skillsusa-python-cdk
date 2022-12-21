from aws_cdk import (
    CfnOutput,
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_lambda_event_sources as lambda_event_sources,
    aws_lambda_python_alpha as lambda_python,
    aws_events as events,
    aws_events_targets as targets,
    aws_sqs as sqs,
    aws_stepfunctions as step_functions,
    aws_stepfunctions_tasks as tasks,
    Duration,
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
            auto_delete_objects=True,
            cors=[
                s3.CorsRule(
                    allowed_headers=["*"],
                    allowed_methods=[s3.HttpMethods.PUT, s3.HttpMethods.GET],
                    allowed_origins=["*"],
                )
            ],
            event_bridge_enabled=True,
        )

        results_bucket = s3.Bucket(
            self,
            "ResultsBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        start_processor = self.build_python_lambda("StartProcessor", "start_processing")
        pre_processor = self.build_python_lambda(
            name="PreProcessor", handler="pre_process", timeout=Duration.minutes(5)
        )
        validator = self.build_python_lambda(name="Validator", handler="validate")
        post_validator = self.build_python_lambda(
            name="PostValidator", handler="post_validate"
        )
        processor = self.build_python_lambda(name="Processor", handler="process")

        submission_bucket.grant_read_write(pre_processor)
        submission_bucket.grant_read(validator)
        submission_bucket.grant_read_write(post_validator)
        submission_bucket.grant_read(processor)
        results_bucket.grant_read_write(processor)

        dead_letter_queue = sqs.Queue(
            self,
            "DeadLetterQueue",
            fifo=True,
            retention_period=Duration.days(14),
        )

        submission_queue = sqs.Queue(
            self,
            "SubmissionQueue",
            fifo=True,
            content_based_deduplication=True,
            dead_letter_queue=sqs.DeadLetterQueue(
                max_receive_count=3, queue=dead_letter_queue
            ),
        )

        rule = events.Rule(
            self,
            "SubmissionRule",
            enabled=True,
            event_pattern=events.EventPattern(
                source=["aws.s3"],
                detail_type=["Object Created"],
                resources=[submission_bucket.bucket_arn],
            ),
        )

        # Use SQS to provide deduplication so our downstream workflow only runs at most once every 5 minutes
        rule.add_target(
            target=targets.SqsQueue(
                queue=submission_queue,
                message=events.RuleTargetInput.from_event_path("$.detail.bucket.name"),
                message_group_id="submission",
            )
        )

        # Wait for the SQS dedupe time to get uploaded items in a "batch"
        task_wait = step_functions.Wait(
            self,
            "WaitForUploadComplete",
            time=step_functions.WaitTime.duration(
                Duration.minutes(1)  # TODO: replace minutes with 5
            ),
        )

        # Move new files into "staging" folder before validation
        task_pre_process = tasks.LambdaInvoke(
            self,
            "PreProcessTask",
            lambda_function=pre_processor,
            payload=step_functions.TaskInput.from_object(
                dict(bucket=submission_bucket.bucket_name)
            ),
        )

        post_pre_process_choice = (
            step_functions.Choice(self, "PostPreProcessChoice")
            .when(
                step_functions.Condition.is_not_present("$.Payload.staged[0]"),
                step_functions.Succeed(self, "No new submissions"),
            )
            .afterwards(include_otherwise=True)
        )

        # Validate each staged submission using a map
        task_validate_map = step_functions.Map(
            self, "ValidateMap", items_path="$.Payload.staged"
        )
        task_validate = tasks.LambdaInvoke(
            self, "ValidateTask", lambda_function=validator
        )
        # After validation, move submission to "submitted <timestamp>"
        task_post_validation_success = tasks.LambdaInvoke(
            self,
            "PostValidateSuccess",
            lambda_function=post_validator,
            payload=step_functions.TaskInput.from_object(
                dict(
                    success=True,
                    prefix="$.Payload.prefix",
                    bucket="$.Payload.bucket",
                )
            ),
        )
        # On failure, move submission to "invalid <timestamp>"
        task_post_validation_failure = tasks.LambdaInvoke(
            self,
            "PostValidateFailure",
            lambda_function=post_validator,
            payload=step_functions.TaskInput.from_object(
                dict(
                    success=False,
                    prefix="$.Payload.prefix",
                    bucket="$.Payload.bucket",
                )
            ),
        )
        task_validate_map.iterator(
            task_validate.add_catch(task_post_validation_failure).next(
                task_post_validation_success
            )
        )

        task_process = tasks.LambdaInvoke(
            self,
            "ProcessTask",
            lambda_function=processor,
        )

        definition = (
            task_wait.next(task_pre_process)
            .next(post_pre_process_choice)
            .next(task_validate_map)
            .next(task_process)
        )

        workflow = step_functions.StateMachine(
            self, "Workflow", definition=definition, timeout=Duration.minutes(5)
        )
        start_processor.add_environment("STATE_MACHINE_ARN", workflow.state_machine_arn)
        workflow.grant_start_execution(start_processor)

        # Trigger the workflow from SQS by using a lambda
        submission_event = lambda_event_sources.SqsEventSource(
            queue=submission_queue,
            batch_size=1,
        )
        start_processor.add_event_source(submission_event)

        static_site = StaticSite(
            self, "StaticSite", submission_bucket=submission_bucket
        )

        CfnOutput(
            self,
            "SneksSubmissionBucket",
            value=submission_bucket.bucket_name,
            export_name="SneksSubmissionBucket",
        )

    def build_python_lambda(
        self, name: str, handler: str, timeout: Duration = Duration.seconds(3)
    ):
        return lambda_python.PythonFunction(
            self,
            name,
            runtime=lambda_.Runtime.PYTHON_3_9,
            entry="./app/processor",
            index="main.py",
            handler=handler,
            timeout=timeout,
        )
