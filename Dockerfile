# Start with a base image that has git installed or install git manually
FROM ubuntu:22.04

# Install curl, git, and Python 3 with pip
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Clone the git repository inside /app
RUN git clone https://github.com/tushar5353/service.git .

RUN cd service && pip3 install .

RUN cd service && python api_gateway/run_server.py  service=service
