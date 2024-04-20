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

n = int(sys.argv[1])
addr = sys.argv[2]
buffer = []
for i in range(n):
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp")) as s:
        start = time.time()
        data = bytes(f"{start}", "utf-8")
        id = os.getpid() & 0xFFFF
        header = struct.pack("!BBHHH", 8, 0, 0, id, i)
        header = struct.pack("!BBHHH", 8, 0, checksum(header + data), id, i)
        s.sendto(header + data, (addr, 0))
        s.settimeout(1)
        try:
            data, _ = s.recvfrom(1024)
            end = time.time()
            rtt = (end - start) * 1000
            buffer.append(rtt)
            print(f"Reply from {addr}: bytes={len(data)} time={round(rtt, 2)}ms")
            time.sleep(1)
        except socket.timeout:
            print("Request timed out")

print(f"Packets: Sent = {n}, Received = {len(buffer)}, Lost = {n - len(buffer)} ({round((1 - len(buffer) / n), 2) * 100}% loss)")
print(f"Minimum = {round(min(buffer), 2)}ms, Maximum = {round(max(buffer), 2)}ms, Average = {round(sum(buffer)/len(buffer), 2)}ms")
