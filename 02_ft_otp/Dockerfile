FROM ubuntu:latest

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies: python, pip, venv, and exiftool
RUN apt update && apt install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    exiftool \
    oathtool \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Create a virtual environment and install python libraries
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir \
    requests \
    beautifulsoup4 \
    Pillow \
    humanize \
    cryptography

# Add the virtual environment to PATH so it is used by default
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /workspace

# docker build -t cybersecurity_image .
# docker run -it --rm -v "$HOME:/workspace" cybersecurity_image

# docker ps -a
# docker images
# docker rm
# docker rmi
