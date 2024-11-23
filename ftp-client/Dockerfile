FROM ubuntu:latest

WORKDIR /

# Update and install the FTP client
RUN apt-get update && apt-get install -y --no-install-recommends \
    ftp \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
