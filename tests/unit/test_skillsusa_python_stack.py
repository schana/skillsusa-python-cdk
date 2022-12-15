import aws_cdk as core
import aws_cdk.assertions as assertions

from sneks.sneks_stack import SneksStack

# example tests. To run these tests, uncomment this file along with the example
# resource in skillsusa_python/skillsusa_python_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SneksStack(app, "sneks")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
