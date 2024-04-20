from tkinter import *
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 12345))
    s.listen()
    while True:
        conn, addr = s.accept()
        root = Tk()
        root.geometry("500x500")
        root.title("server")
        canvas = Canvas(bg="white", width=450, height=450)
        canvas.pack(anchor=CENTER, expand=1)
        root.update()
        while True:
            data = conn.recv(7)
            if not data:
                root.destroy()
                break
            x, y = list(map(int, data.decode("utf-8").split(" ")))
            canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black", outline="black")
            root.update()
