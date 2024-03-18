import asyncio
import socket

async def handle_stdout(conn, stdout):
    loop = asyncio.get_event_loop()
    while True:
        buf = await stdout.read(256)
        if not buf:
            break
        await loop.sock_sendall(conn, buf)

async def handle_stderr(conn, stderr):
    loop = asyncio.get_event_loop()
    while True:
        buf = await stderr.read(256)
        if not buf:
            break
        await loop.sock_sendall(conn, buf)

async def handle_stdin(conn, stdin):
    loop = asyncio.get_event_loop()
    while True:
        buf = await loop.sock_recv(conn, 256)
        if not buf:
            break
        stdin.write(buf)
        await stdin.drain()

async def handle_conn(conn):
    print("Connection started")
    loop = asyncio.get_event_loop()
    command = await loop.sock_recv(conn, 256)
    if not command:
        return
    command = command.decode("utf-8")
    print(f"Command: {command}")
    proc = await asyncio.create_subprocess_shell(
        command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    tasks = [loop.create_task(handle_stderr(conn, proc.stderr)),
        loop.create_task(handle_stdout(conn, proc.stdout)),
        loop.create_task(handle_stdin(conn, proc.stdin))]
    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in tasks:
        task.cancel()

    conn.close()
    print("Connection finished")

async def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.bind(("", 12345))
    sock.listen()

    loop = asyncio.get_event_loop()
    while True:
        conn, _ = await loop.sock_accept(sock)
        loop.create_task(handle_conn(conn))

asyncio.run(run_server())
