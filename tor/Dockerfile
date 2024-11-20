FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    tor \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 4242

CMD ["tor", "-f", "/etc/tor/torrc"]
