import socket
import struct
import uuid
import sys

try:
    mac = uuid.getnode().to_bytes(6, 'big')
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    s.bind(("eth0", 0))
    input = 0
    output = 0
    while True:
        data = s.recv(2048)
        dst_mac, src_mac, _ = struct.unpack("!6s6sH", data[:14])
        print(f"{src_mac.hex(':')} -> {dst_mac.hex(':')} length={len(data)}")
        if src_mac == mac:
            output += len(data)
        else:
            input += len(data)
except KeyboardInterrupt:
    print()
    print(f"in={input} bytes, out={output} bytes")
    sys.exit(0)
