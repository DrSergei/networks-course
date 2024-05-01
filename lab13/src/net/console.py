from scapy.all import ARP, Ether, srp
import socket
import sys

def getname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return None

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
mask = ip + "/" + sys.argv[1]
results, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=mask), timeout=30, verbose=0)

buffer = {}
for _, data in results:
    buffer[data.psrc] = (data.hwsrc, getname(data.psrc))

print("Current host")
print(f"ip={ip}, mac={buffer[ip][0]}, name={buffer[ip][1]}")
buffer.pop(ip)
print("Local network")
for ip, (mac, name) in buffer.items():
    print(f"ip={ip}, mac={mac}, name={name}")
