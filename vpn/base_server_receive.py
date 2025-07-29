#!/usr/bin/env python3

from scapy.all import *

IP_A = "0.0.0.0"
PORT = 9090

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_A, PORT))

while True:
   data, (ip, port) = sock.recvfrom(2048)
   print("Received packet on my socket: {}:{} --> {}:{}".format(ip, port, IP_A, PORT))
   pkt = IP(data)
   print("The data is a packet: {} --> {}".format(pkt.src, pkt.dst))
   print(IP(data).show())
   print("")
