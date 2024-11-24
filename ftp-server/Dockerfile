FROM ubuntu:latest

WORKDIR /ftp-server/files

RUN apt-get update && apt-get install -y --no-install-recommends \
    vsftpd \
    iputils-ping \
    net-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY vsftpd.conf /etc/vsftpd.conf

RUN mkdir -p /var/run/vsftpd/empty \
    && chmod 755 /var/run/vsftpd/empty

RUN adduser --disabled-password --gecos "" ftpuser \
    && echo "ftpuser:ftp123" | chpasswd \
    && usermod -d /ftp-server/files ftpuser

RUN mkdir -p /ftp-server/files \
    && chown -R ftpuser:ftpuser /ftp-server/files \
    && chmod -R 755 /ftp-server/files

EXPOSE 21

CMD ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]
