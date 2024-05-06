from tkinter import *
import socket
import random
import time
import struct

window = Tk()
window.title("Client")

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

number_lb = Label(
   frame,
   text="number"
)
number_lb.grid(row=5, column=1)
number_tf = Entry(
    frame
)
number_tf.grid(row=5, column=2)

PACKET_SIZE = 1024

def get_random_data():
    return random.randbytes(PACKET_SIZE)

def get_data():
    start = struct.pack("d", time.time())
    n = int(number_tf.get()).to_bytes(4, "big")
    return start + n

def send():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host_tf.get(), int(port_tf.get())))
        s.sendall(get_data())
        for _ in range(int(number_tf.get())):
            s.sendall(get_random_data())

send_btn = Button(
   frame,
   text="send",
   command=send
)
send_btn.grid(row=6, column=1, columnspan=2)

window.mainloop()
