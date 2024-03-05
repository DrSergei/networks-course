import socket
import sys
from concurrent.futures import ThreadPoolExecutor

LOCALHOST = "127.0.0.1" 

if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    path = sys.argv[3]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(f"GET /{path} HTTP/1.1".encode())
        while True:
            bytes = s.recv(1024)
            if not bytes:
                break
            print(bytes.decode())
