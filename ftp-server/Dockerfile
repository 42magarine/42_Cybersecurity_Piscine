FROM ubuntu:latest

WORKDIR /

# Update and install vsftpd
RUN apt-get update && apt-get install -y --no-install-recommends \
    vsftpd \
    && mkdir -p /var/ftp \
    && chmod -R 755 /var/ftp \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the vsftpd configuration file into the container
COPY vsftpd.conf /etc/vsftpd.conf

# Expose the FTP port (default is 21)
EXPOSE 21
