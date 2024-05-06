from tkinter import *
from tkinter import messagebox
import socket
import time
import struct

window = Tk()
window.title("Server")

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
host_tf.grid(row=3, column=2)

port_lb = Label(
   frame,
   text="port"
)
port_lb.grid(row=4, column=1)
port_tf = Entry(
    frame
)
port_tf.grid(row=4, column=2)

PACKET_SIZE = 1024

def receive():
    start = None
    n = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host_tf.get(), int(port_tf.get())))
        s.listen()
        conn, _ = s.accept()
        with conn:
            data = conn.recv(12)
            start = struct.unpack_from("d", data[0:8])[0]
            n = int.from_bytes(data[8:12], "big")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host_tf.get(), int(port_tf.get())))
        s.settimeout(1)
        k = 0
        end = start
        try:
            for i in range(n):
                _ = s.recv(PACKET_SIZE)
                k = i
                end = time.time()
            end = time.time()
        except socket.timeout:
            pass
        messagebox.showinfo("Results", f"speed={round(k * PACKET_SIZE / (end - start)/1000, 2)}Mb/s\npackets={k} of {n}")

receive_btn = Button(
   frame,
   text="receive",
   command=receive
)
receive_btn.grid(row=5, column=1, columnspan=2)

window.mainloop()
