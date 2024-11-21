FROM nginx:alpine

RUN apk add --no-cache openssh
RUN ssh-keygen -A
RUN echo 'root:password' | chpasswd

CMD /usr/sbin/sshd && nginx -g 'daemon off;'

EXPOSE 4242
