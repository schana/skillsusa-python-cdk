#!/usr/bin/env python3

import aws_cdk as cdk

from sneksinfra.sneks_stack import SneksStack

app = cdk.App()
SneksStack(
    app,
    "SneksStack",
)

app.synth()
