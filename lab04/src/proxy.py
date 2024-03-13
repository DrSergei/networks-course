import socket
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

LOCALHOST = "127.0.0.1"

blasklist = set()

def send_error(conn, http_version, code, message):
    answer = f"{http_version} {code} {message}\r\nContent-Length: 0\r\n\r\n"
    print(f"Send error: {code}")
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
        url = url[:pos]
    pos = url.find(":")
    if (pos == -1):
        host = url
    else:
        host = url[:pos]
        port = int(url[pos+1:])
    return host, port

def redirect(first, second):
    while True:
        bytes = first.recv(4096)
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
        if host in blasklist:
            send_error(input, http_version, 400, "Bad Request")
            return
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as output:
            try:
                output.connect((host, port))
            except socket.error as e:
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

def init_blacklist(filename):
    with open(filename) as f:
        for host in f.readlines():
            blasklist.add(host)

if __name__ == "__main__":
    port = int(sys.argv[1])
    max_threads = int(sys.argv[2])
    init_blacklist(sys.argv[3])
    pool = ThreadPoolExecutor(max_threads)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((LOCALHOST, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            pool.submit(handle, conn)
