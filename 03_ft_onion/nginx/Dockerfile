FROM nginx:alpine

RUN apk add --no-cache openssh

# Generates SSH host keys for secure SSH communication.
RUN ssh-keygen -A

# Sets the password for the root user to password. This enables password-based authentication.
RUN echo 'root:password' | chpasswd

# Starts both the SSH daemon (sshd) and Nginx when the container runs.
CMD /usr/sbin/sshd && nginx -g 'daemon off;'

# Exposes port 4242 in the container for SSH access.
EXPOSE 4242
