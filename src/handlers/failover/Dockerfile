FROM 137112412989.dkr.ecr.us-west-2.amazonaws.com/amazonlinux:latest

RUN mkdir /app && \
    yum install -y \
      python27 \
      python27-pip \
      python27-devel \
      python27-libs \
      libffi-devel \
      openssl-devel \
      gcc && \
    pip install -U pip

WORKDIR /app
COPY ["requirements.txt", "requirements.txt"]
ENTRYPOINT pip install --no-cache-dir -r requirements.txt -t vendored
