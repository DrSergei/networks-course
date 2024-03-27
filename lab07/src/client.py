import socket
import time
import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.settimeout(1)

buffer = []
n = 0
for i in range(1, 11):
    try:
        start = datetime.datetime.now()
        sock.sendto(bytes(f"Ping {i} {start.time()}", "utf-8"), ("127.0.0.1", 12000))
        data = sock.recv(1024)
        print(data.decode("utf-8"))
        end = datetime.datetime.now()
        delta = (end - start).total_seconds()
        buffer.append(delta)
        print(f"RTT: {delta}s")
    except Exception as e:
        n += 1
        print("Request timed out")
    time.sleep(0.1)

print(f"min: {min(buffer)}s, max: {max(buffer)}s, avg: {sum(buffer)/len(buffer)}s, loss: {n/10.0}%")
