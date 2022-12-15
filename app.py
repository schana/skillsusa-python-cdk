#!/usr/bin/env python3

import aws_cdk as cdk

from sneks.sneks_stack import SneksStack

app = cdk.App()
SneksStack(
    app,
    "SneksStack",
)

app.synth()
