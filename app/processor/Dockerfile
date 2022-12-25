FROM public.ecr.aws/lambda/python:3.9

ARG CACHE=1
COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
ADD . "${LAMBDA_TASK_ROOT}"
