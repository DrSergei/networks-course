import socket
import sys
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

LOCALHOST = "127.0.0.1" 

def send_error(conn, http_version, code, message):
    answer = f"{http_version} {code} {message}\r\nContent-Length: 0\r\n\r\n"
    print(answer)
    conn.sendall(answer.encode())

def get_host_port(url):
    pos = url.find("://")
    host = None
    port = 80
    if (pos == -1):
        url = url
    else:
        url = url[(pos+3):]
    
    pos = url.find("/")
    if (pos != -1):
        host = url[:pos]
    
    pos = url.find(":")
    if (pos == -1):
        host = url if host is None else host
    else:
        host = url[:pos] if host is None else host
        port = int(url[pos:])

    return host, port

def redirect(first, second):
    while True:
        bytes = first.recv(4096)
        # print(bytes.decode())
        if not bytes:
            return
        second.sendall(bytes)

def handle(input):
    with input:
        bytes = input.recv(4096)
        if not bytes:
            return
        heading = bytes.decode().split("\r\n")[0]
        type, url, http_version = heading.split()
        if type not in ["GET", "POST"]:
            send_error(input, http_version, 400, "Bad Request")
            return
        host, port = get_host_port(url)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as output:
            output.settimeout(0.1)
            # try:
            #     output.connect((host, port))
            # except socket.error as e:
            #     print("aaa")
            send_error(input, http_version, 522, "Connection Timed Out")
            return
            print(f"Connection started for {host}:{port}")
            output.sendall(bytes)
            input_to_output = Thread(target=redirect, args=(input, output,))
            input_to_output.start()
            output_to_input = Thread(target=redirect, args=(output, input,))
            output_to_input.start()
            input_to_output.join()
            output_to_input.join()
            print(f"Connection closed for {host}:{port}")

if __name__ == "__main__":
    port = int(sys.argv[1])
    max_threads = int(sys.argv[2])
    pool = ThreadPoolExecutor(max_threads)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((LOCALHOST, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            pool.submit(handle, conn)
