from tkinter import *
from tkinter import messagebox
from ftplib import FTP
from pathlib import PurePosixPath

window = Tk()
window.title("FTP Client")
window.geometry("800x600")

frame = Frame(
   window,
   padx = 10,
   pady = 10
)
frame.pack(expand=True)

host_lb = Label(
   frame,
   text="host"
)
host_lb.grid(row=3, column=1)
host_tf = Entry(
    frame
)
host_tf.grid(row=4, column=1)

user_lb = Label(
   frame,
   text="user"
)
user_lb.grid(row=3, column=2)
user_tf = Entry(
    frame
)
user_tf.grid(row=4, column=2)

password_lb = Label(
   frame,
   text="password"
)
password_lb.grid(row=3, column=3)
password_tf = Entry(
    frame
)
password_tf.grid(row=4, column=3)

output = Text(
    frame
)
output.grid(row=7, column=1, columnspan=3)

ftp = None

def connect():
    global ftp
    try:
        ftp = FTP(host_tf.get())
        ftp.login(user_tf.get(), password_tf.get())
        output.insert(END, "Connection started\n")
    except Exception as e:
        output.insert(END, e)

connect_btn = Button(
   frame,
   text="connect",
   command=connect
)
connect_btn.grid(row=5, column=2)

command_lb = Label(
   frame,
   text="command"
)
command_lb.grid(row=6, column=1)
command_tf = Entry(
    frame
)
command_tf.grid(row=6, column=2)

def ls(dir, indent=""):
    output.insert(END, indent + dir.name + "/\n")
    files = ftp.mlsd(dir)
    for name, meta in files:
        if meta["type"] == "dir":
            ls(PurePosixPath(dir, name), indent + " ")
        else:
            output.insert(END, indent + " " + name + "\n")

def upload(local_file_path, remote_file_path):
    try:
        with open(local_file_path, "rb") as file:
            ftp.storbinary("STOR " + remote_file_path, file)
        output.insert(END, "Upload success\n")
    except Exception as e:
        output.insert(END, e)

def download(remote_file_path, local_file_path):
    try:
        with open(local_file_path, "wb") as file:
            ftp.retrbinary("RETR " + remote_file_path, file.write)
        output.insert(END, "Download success\n")
    except Exception as e:
        output.insert(END, e)

def exec():
    cmd = command_tf.get().split()
    if cmd[0] == "exit":
        ftp.quit()
        output.insert(END, "Connection closed\n")
    elif cmd[0] == "ls":
        ls(PurePosixPath(ftp.pwd()))
    elif cmd[0] == "upload":
        upload(cmd[1], cmd[2])
    elif cmd[0] == "download":
        download(cmd[1], cmd[2])
    else:
        print("Invalid command")

command_btn = Button(
   frame,
   text="exec",
   command=exec
)
command_btn.grid(row=6, column=3)

window.mainloop()

