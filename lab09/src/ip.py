import subprocess

lines = subprocess.check_output(["ipconfig"]).decode("utf-8").split("\n")
ip = None
mask = None
for line in lines:
    line = line.strip()
    if line.startswith("IPv4 Address"):
        ip = line.split()[-1]
    if line.startswith("Subnet Mask"):
        mask = line.split()[-1]

print(ip, mask)
