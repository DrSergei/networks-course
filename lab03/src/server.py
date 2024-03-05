import socket
import sys
import os
from concurrent.futures import ThreadPoolExecutor

LOCALHOST = "127.0.0.1" 

def send_error(conn, http_version, code, message):
    answer = f"{http_version} {code} {message}\r\nContent-Length: 0\r\n\r\n"
    conn.sendall(answer.encode())

def handle_conn(conn):
    with conn:
        bytes = conn.recv(4096)
        if not bytes:
            return
        heading = bytes.decode().split("\r\n")[0]
        query, arg, http_version = heading.split()
        if query == "GET":
            path = os.path.join(os.getcwd(), arg[1:])
            if os.path.exists(path):
                with open(path, "rb") as f:
                    data = f.read()
                    answer = f"{http_version} 200 OK\r\nConnection: Closed\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(data)}\r\n\r\n"
                    response = answer.encode() + data
                    conn.sendall(response)
            else:
                send_error(conn, http_version, 404, "Not Found")
        else:
            send_error(conn, http_version, 400, "Bad Request")

if __name__ == "__main__":
    port = int(sys.argv[1])
    max_threads = int(sys.argv[2])
    pool = ThreadPoolExecutor(max_threads)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((LOCALHOST, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            pool.submit(handle_conn, conn)
