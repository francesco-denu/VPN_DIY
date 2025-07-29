#!/usr/bin python3

import fcntl
import struct
import os
import time
from scapy.all import *

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001 #layer 3 interface
IFF_TAP   = 0x0002 #layer 2 interface
IFF_NO_PI = 0x1000

# Creazione dell'interfaccia in lettura/scrittura
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'tun%d', IFF_TAP | IFF_NO_PI) # creazione della struttura: stringa a 16 byte, nome, flags (il secondo dice di non aggiungere header o dati al pacchetto)
ifname_bytes  = fcntl.ioctl(tun, TUNSETIFF, ifr) # si aggiunge l'interfaccia al kernel, e ci viene ritornato il vero nome dell'interfaccia (%d sostituito)

#Eliminiamo dal nome dell'interfaccia eventuale padding
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name: {}".format(ifname))

#Configuriamo l'interfaccia
os.system("ip addr add 10.0.53.99/24 dev {}".format(ifname)) 
os.system("ip link set dev {} up".format(ifname)) 
"""
while True:
   packet = os.read(tun, 2048) #si legge cio che arriva dall'interfaccia
   if packet:
      pkt = IP(packet) #si convertono i dati in un pacchetto IP di scapy
      print(pkt.show()) #si stampa il pacchetto
      responseIP = IP(src='10.0.53.88', dst = pkt.src) #PER SIMULARE UNA RISPOSTA
      responsePkt = responseIP/pkt.payload
      os.write(tun,bytes(responsePkt))

"""
# SE TAP, vediamo layer 2, ARP

while True:
   packet = os.read(tun, 2048) #si legge cio che arriva dall'interfaccia
   if packet:
      ether = Ether(packet) #si convertono i dati in un pacchetto IP di scapy
      print(ether.show()) #si stampa il pacchetto
      
      #responseEther = Ether(src='aa:bb:cc:dd:ee:ff', dst= ether.src)
      #responsePkt = responseEther / ether.payload
      #os.write(tun,bytes(responsePkt))
      
 
