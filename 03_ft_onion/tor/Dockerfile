FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get install -y tor --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Creates the directory for Tor’s hidden service and restricts its permissions for security.
RUN mkdir -p /var/lib/tor/hidden_service && \
    chmod 700 /var/lib/tor/hidden_service

# Sets the default command to run the Tor daemon.
CMD ["tor"]
