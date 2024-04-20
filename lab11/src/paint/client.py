from tkinter import *
import socket

class Paint(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.color = "black"
        self.pack(fill=BOTH, expand=1)
        self.canv = Canvas(self, bg="white", width=450, height=450)
        self.canv.pack(anchor=CENTER, expand=1)
        self.canv.bind("<B1-Motion>", self.draw)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("127.0.0.1", 12345))
 
    def draw(self, event):
        x = str(event.x)
        x = str.rjust(x, 3, '0')
        y = str(event.y)
        y = str.rjust(y, 3, '0')
        self.socket.sendall(bytes(f"{x} {y}", "utf-8"))
        self.canv.create_oval(event.x - 2, event.y - 2, event.x + 2, event.y + 2, fill=self.color, outline=self.color)
 
root = Tk()
root.title("client")
root.geometry("500x500")
app = Paint(root)
root.mainloop()
