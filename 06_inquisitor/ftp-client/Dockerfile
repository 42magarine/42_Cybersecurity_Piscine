FROM ubuntu:latest

RUN apt update && apt install -y --no-install-recommends \
    ftp \
    net-tools \
    iputils-ping \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# Keep container alive
CMD ["tail", "-f", "/dev/null"]
