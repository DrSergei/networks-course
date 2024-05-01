import socket
import struct
import uuid
import sys

try:
    mac = uuid.getnode().to_bytes(6, 'big')
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    s.bind(("eth0", 0))
    buffer = {}
    while True:
        data = s.recv(2048)
        direction = None
        dst_mac, src_mac, type = struct.unpack("!6s6sH", data[:14])
        if src_mac == mac:
            direction = "out"
        else:
            direction = "in"
        type = socket.htons(type)
        if type == 8:
            src_ip, dst_ip = struct.unpack("4s4s", data[26:34])
            proto = data[23]
            length = (data[14] & 0b00001111) * 4
            src_ip = f"{src_ip[0]}.{src_ip[1]}.{src_ip[2]}.{src_ip[3]}"
            dst_ip = f"{dst_ip[0]}.{dst_ip[1]}.{dst_ip[2]}.{dst_ip[3]}"
            if proto in [6, 17]:
                port = None
                if direction == "in":
                    port = struct.unpack("!H", data[14 + length + 2:14 + length + 4])[0]
                else:
                    port = struct.unpack("!H", data[14 + length:14 + length + 2])[0]
                if port not in buffer:
                    buffer[port] = {"in": 0, "out": 0}
                buffer[port][direction] += len(data) - 14 - length
                print(f"{src_ip} -> {dst_ip} length={len(data)}, protocol={'TCP' if proto == 6 else 'UDP'}, local port={port}")
            else:
                print(f"Unsupported protocol: {proto}")
        else:
            print(f"Unsupported type: {type}")
except KeyboardInterrupt:
    print()
    for port, data in buffer.items():
        print(f"port={port} in={data['in']} bytes out={data['out']} bytes")
    sys.exit(0)
