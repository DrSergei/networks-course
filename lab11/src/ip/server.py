import socket

sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
sock.bind(('::1', 12345))
sock.listen()

while True:
    conn, addr = sock.accept()
    print(addr)
    data = conn.recv(1024)
    if not data:
        break
    conn.sendall(data.upper())
    conn.close()

sock.close()
