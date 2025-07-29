#!/usr/bin/python3

#import select
import fcntl
import struct
import os
from scapy.all import *

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

"""
def encrypt_aes(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return base64.b64encode(ciphertext)

def decrypt_aes(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(base64.b64decode(ciphertext))
    return unpad(decrypted_data, AES.block_size)
"""

def encrypt_aes(data, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return base64.b64encode(cipher.nonce + ciphertext + tag)

def decrypt_aes(ciphertext, key):
    ciphertext = base64.b64decode(ciphertext)
    nonce = ciphertext[:16]
    tag = ciphertext[-16:]
    ciphertext = ciphertext[16:-16]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data
    
    
key = b"0123456789abcdef"  # 128-bit key in bytes


IP_A = "0.0.0.0"
PORT = 9090

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000

# Create a tun interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'tun%d', IFF_TUN | IFF_NO_PI)
ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)
ifname  = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name: {}".format(ifname))

# Set up the tun interface and routing
os.system("ip addr add 10.0.53.1/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_A, PORT))

# We need to initialize ip and port (their values do not matter)
ip   = '0.0.0.0'
port = 10000

fds = [sock, tun]
while True:
  # this will block until at least one socket is ready
  ready, _, _ = select.select(fds, [], []) 

  for fd in ready:
    if fd is sock:
       data, (ip, port) = sock.recvfrom(2048) 
       decrypted_data = decrypt_aes(data, key)
       pkt = IP(decrypted_data)
       print("From socket <==: {} --> {}".format(pkt.src, pkt.dst))
       os.write(tun, decrypted_data)

    if fd is tun: #i pacchetti diretti al client 10.0.53.99 (client:tun) sono automaticamente diretti verso la tun del server perche hanno stessa rete
       packet = os.read(tun, 2048)
       pkt = IP(packet)
       print("From tun    ==>: {} --> {}".format(pkt.src, pkt.dst))
       encrypted_data = encrypt_aes(packet, key)
       sock.sendto(encrypted_data, (ip, port)) #invia alla destinazione che è stata l'ultimo mittente a inviare qualcosa
       
