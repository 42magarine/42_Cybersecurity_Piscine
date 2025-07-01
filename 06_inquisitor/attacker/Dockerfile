FROM ubuntu:latest

WORKDIR /

# Update and install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    tcpdump \
    libpcap0.8 \
    libpcap-dev \
    iproute2 \
    iputils-ping \
    net-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and activate a Python virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python dependencies inside the virtual environment
RUN pip install --no-cache-dir \
    scapy

# Copy the ARP poisoning script
COPY inquisitor.py /inquisitor.py

# Keep container alive for testing
CMD ["tail", "-f", "/dev/null"]
