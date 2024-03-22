from ftplib import FTP
from pathlib import PurePosixPath

ftp = FTP("127.0.0.1")
ftp.login("TestUser", "000")

def ls(dir, indent=""):
    print(indent, dir.name + "/", sep="")
    files = ftp.mlsd(dir)
    for name, meta in files:
        if meta["type"] == "dir":
            ls(PurePosixPath(dir, name), indent + " ")
        else:
            print(indent, name)

def upload(local_file_path, remote_file_path):
    with open(local_file_path, "rb") as file:
        ftp.storbinary("STOR " + remote_file_path, file)

def download(remote_file_path, local_file_path):
    with open(local_file_path, "wb") as file:
        ftp.retrbinary("RETR " + remote_file_path, file.write)

while True:
    cmd = input().split(" ")
    if cmd[0] == "exit":
        break
    elif cmd[0] == "ls":
        ls(PurePosixPath(ftp.pwd()))
    elif cmd[0] == "upload":
        upload(cmd[1], cmd[2])
    elif cmd[0] == "download":
        download(cmd[1], cmd[2])
    else:
        print("Invalid command")

ftp.quit()
