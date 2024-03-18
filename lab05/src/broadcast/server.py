import socket
import time
import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    sock.sendto(bytes(f"{datetime.datetime.now()}", "utf-8"), ("<broadcast>", 12345))
    time.sleep(1)
