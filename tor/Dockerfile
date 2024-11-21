FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get install -y tor --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/lib/tor/hidden_service && \
    chmod 700 /var/lib/tor/hidden_service

CMD ["tor"]
