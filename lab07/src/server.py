import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", 12000))

while True:
    data, addr = sock.recvfrom(1024)
    if random.randint(0, 9) < 2:
        continue
    sock.sendto(data.upper(), addr)
