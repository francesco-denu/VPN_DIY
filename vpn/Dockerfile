FROM ubuntu:latest

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        net-tools \
        iputils-ping \
        telnet \
        tcpdump \
        python3 \
        python3-pip \
        iproute2 \
        inetutils-inetd \
        netcat \
        build-essential \
        libffi-dev \
        libssl-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install scapy pycryptodome

CMD ["/bin/bash"]
