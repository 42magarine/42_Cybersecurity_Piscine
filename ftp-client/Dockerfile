FROM ubuntu:latest

WORKDIR /ftp-client/files

RUN apt-get update && apt-get install -y --no-install-recommends \
    ftp \
    iputils-ping \
    net-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Keep container alive
CMD ["tail", "-f", "/dev/null"]
