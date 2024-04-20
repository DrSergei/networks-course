import os
import sys
import socket
import struct
import time

def checksum(data):
    if len(data) % 2:
        data += b'\x00'
    sum = 0
    for i in range(0, len(data), 2):
        sum += (data[i] << 8) + data[i+1]
    while (sum >> 16):
        sum = (sum & 0xFFFF) + (sum >> 16)
    sum = ~sum & 0xFFFF
    return sum

def trygethostbyaddr(addr):
    try:
        return socket.gethostbyaddr(addr[0])[0]
    except:
        return None

n = 1
reached = False
for ttl in range(1, int(sys.argv[2]) + 1):
    if reached:
        break
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp')) as s:
        s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        for i in range(1, int(sys.argv[3]) + 1):
            data = b""
            id = os.getpid() & 0xFFFF
            header = struct.pack("!BBHHH", 8, 0, 0, id, n)
            header = struct.pack("!BBHHH", 8, 0, checksum(header + data), id, n)
            n += 1
            s.sendto(header + data, (sys.argv[1], 0))
            start = time.time()
            s.settimeout(1)
            try:
                data, addr = s.recvfrom(1024)
                end = time.time()
                if data[20] == 11:
                    host = trygethostbyaddr(addr)
                    rtt = round((end - start) * 1000, 2)
                    result = f'{ttl}.{i}: ({addr[0]}) {rtt} ms'
                    if host is not None:
                        result += f' [{host}]'
                    print(result)
                elif data[20] == 0:
                    host = trygethostbyaddr(addr)
                    result = f'{ttl}.{i}: ({addr[0]}) {rtt} ms'
                    if host is not None:
                        result += f' [{host}]'
                    print(result)
                    reached = True
            except socket.timeout:
                print(f"{ttl}.{i}: Request timed out")
