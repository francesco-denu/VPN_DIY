#!/bin/bash

#NAT PER LA RETE 192.168.60.0/24, QUANDO VA SU INTERNET (ESCLUDENDO QUINDI 10.9.0.0/24) AVRÀ SORGENTE 10.9.0.11 
iptables -t nat -A POSTROUTING ! -d 10.9.0.0/24 -j MASQUERADE -o eth0

#------->IGRESS
#ACCETTA SOLO TRAFFICO IN INGRESSO DERIVANTE DA CONNESSIONE SSH 
iptables -A FORWARD -i eth0 -p tcp -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT #stateful
iptables -A FORWARD -i eth0 -p tcp --dport 22 -j ACCEPT  
iptables -A FORWARD -i eth0 -p tcp -j DROP  

#------->EGRESS
#RIFIUTA TRAFFICO IN INGRESSO SU ETH1 (in uscita dalla rete) PROVENIENTE DA www.example.com
iptables -A FORWARD -i eth1 -d 93.184.216.0/24 -j DROP


