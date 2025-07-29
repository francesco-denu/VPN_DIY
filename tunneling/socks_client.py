#!/usr/bin/env python3

import socks

with socks.socksocket() as s:
    s.set_proxy(socks.SOCKS5, "localhost", 9000)
    s.connect(("10.9.0.5", 8080))
    
    s.sendall(b"Hello World, \n")
    s.sendall(b"GRAZIE A TUTTI")
    
    data = s.recv(4096)
    print(data)
