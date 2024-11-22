FROM alpine:latest

RUN apk add --no-cache \
    python3 \
    py3-pip \
    libsodium

WORKDIR /root

COPY ./infection /root/infection

# docker build -t stockholm_image .
# docker run -it --rm stockholm_image
# docker run -it --rm -v "$HOME:/root/workspace" stockholm_image
