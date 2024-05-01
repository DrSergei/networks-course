from scapy.all import ARP, Ether, srp
import socket
from tkinter import *
from tkinter import ttk
 
window = Tk()
frame = Frame(
   window,
   padx = 10,
   pady = 10
)
frame.pack(expand=True)
lb = Label(
   frame,
   text="prefix length"
)
lb.grid(row=1, column=1)
tf = Entry(
    frame
)
tf.grid(row=1, column=2)
def work():
    def getname(ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return None
    
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    mask = ip + "/" + tf.get()
    results, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=mask), timeout=30, verbose=0)

    buffer = {}
    for _, data in results:
        buffer[data.psrc] = (data.hwsrc, getname(data.psrc))
    
    tree.delete(*tree.get_children())
    tree.insert("", END, values=("Current host","",""))
    tree.insert("", END, values=(ip, buffer[ip][0], buffer[ip][1]))
    buffer.pop(ip)
    tree.insert("", END, values=("Local network","",""))
    for ip, (mac, name) in buffer.items():
        tree.insert("", END, values=(ip, mac, name))
btn = Button(
   frame,
   text="start",
   command=work
)
btn.grid(row=1, column=3)
columns = ("ip", "mac", "name")
tree = ttk.Treeview(frame, columns=columns, show="headings")
tree.grid(row=2, column=1, columnspan=3)
tree.heading("ip", text="ip")
tree.heading("mac", text="mac")
tree.heading("name", text="name")
window.mainloop()
