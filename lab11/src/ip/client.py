import socket

sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
sock.connect(('::1', 12345))

sock.sendall("Hello, World!".encode())
print(sock.recv(1024).decode())

sock.close()
