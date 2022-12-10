import aws_cdk as core
import aws_cdk.assertions as assertions

from skillsusa_python.skillsusa_python_stack import SkillsusaPythonStack

# example tests. To run these tests, uncomment this file along with the example
# resource in skillsusa_python/skillsusa_python_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SkillsusaPythonStack(app, "skillsusa-python")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
