import asyncio
import socket
import sys

from aioconsole import get_standard_streams

async def handle_output(sock, writer):
    loop = asyncio.get_event_loop()
    while True:
        buf = await loop.sock_recv(sock, 256)
        if not buf:
            break
        writer.write(buf.decode("utf-8"))
        await writer.drain()

async def handle_input(sock, reader):
    loop = asyncio.get_event_loop()
    while True:
        buf = await reader.readline()
        if not buf:
            return
        await loop.sock_sendall(sock, buf)

async def run_client(host, command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    
    loop = asyncio.get_event_loop()
    await loop.sock_connect(sock, (host, 12345))
    await loop.sock_sendall(sock, bytes(command, "utf-8"))
    reader, writer = await get_standard_streams()
    tasks = [loop.create_task(handle_input(sock, reader)), loop.create_task(handle_output(sock, writer))]
    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in tasks:
        task.cancel()

asyncio.run(run_client(sys.argv[1], sys.argv[2]))
