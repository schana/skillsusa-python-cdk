FROM public.ecr.aws/lambda/python:3.9

ARG PYPY_VERSION=pypy3.9-v7.3.11-linux64

ADD https://downloads.python.org/pypy/$PYPY_VERSION.tar.bz2 .

RUN yum install -y bzip2
RUN bunzip2 $PYPY_VERSION.tar.bz2
RUN yum history undo last -y

RUN yum install -y tar
RUN tar xf $PYPY_VERSION.tar
RUN yum history undo last -y

RUN rm $PYPY_VERSION.tar
RUN mkdir -p /opt
RUN mv $PYPY_VERSION/* /opt
RUN rm -rf $PYPY_VERSION
RUN pypy -m ensurepip
RUN pypy -m pip install --upgrade pip

COPY requirements-scoring.txt .
RUN pypy -m pip install -r requirements-scoring.txt
RUN pypy -m pip install awslambdaric

COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
ADD . "${LAMBDA_TASK_ROOT}"
