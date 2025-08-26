FROM ubuntu:latest

# Declare build args to receive values from docker-compose
ARG ENVIRONMENT
ARG RUN_TYPE

ENV ENVIRONMENT=${ENVIRONMENT}
ENV RUN_TYPE=${RUN_TYPE}

# Install curl, git, and Python 3 with pip
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3.12-venv \
    python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

ENV PYTHONPATH=/app

RUN echo "ENVIRONMENT is $ENVIRONMENT"
RUN echo "RUN_TYPE is $RUN_TYPE"

WORKDIR /app/service

COPY . /app/service

RUN ls

RUN python3 -m venv venv

RUN ./venv/bin/pip install .

CMD ["./venv/bin/python", "api_gateway/run_server.py", "--service=service"]
