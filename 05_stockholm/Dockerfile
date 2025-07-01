FROM ubuntu:latest

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies: python, pip and venv
RUN apt update && apt install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    libsodium-dev \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Create a virtual environment and install python libraries
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir \
    pynacl

# Add the virtual environment to PATH so it is used by default
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /root

# COPY ./infection /root/infection

# docker build -t stockholm_image .
# docker run -it --rm stockholm_image
# docker run -it --rm -v "$(pwd):/root" stockholm_image
