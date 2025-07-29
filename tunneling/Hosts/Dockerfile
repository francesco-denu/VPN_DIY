FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive

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
        openssh-server \
        iptables \
        netcat \
        curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install scapy PySocks

# Set the password for the account
RUN echo 'root:12345' | chpasswd

COPY sshd_config /etc/ssh/sshd_config
