import json


def main(event, context):
    print(json.dumps(event))
    print(json.dumps(context))
