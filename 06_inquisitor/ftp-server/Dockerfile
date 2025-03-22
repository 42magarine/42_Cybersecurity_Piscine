FROM ubuntu:latest

RUN apt update && apt install -y --no-install-recommends \
    vsftpd \
    net-tools \
    iputils-ping \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m user1 \
    && echo "user1:user1" | chpasswd \
    && useradd -m user2 \
    && echo "user2:user2" | chpasswd

RUN mkdir -p /var/ftp \
    && mkdir -p /var/run/vsftpd/empty

COPY vsftpd.conf /etc/vsftpd.conf

EXPOSE 21

CMD ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]
