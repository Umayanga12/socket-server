import socket
import os
import asyncio
from multiprocessing import Process
from db import add_client_ip, remove_client_ip, get_all_client_ips
from client import handle_client

# Server configuration
SERVER = socket.gethostbyname(socket.gethostname())
PORT = int(os.environ.get("SERVERPORT", 5000))
ADDRESS = (SERVER, PORT)

# Initialize server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


# Async function to accept incoming connections
async def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    loop = asyncio.get_running_loop()
    while True:
        conn, addr = await loop.run_in_executor(None, server.accept)
        asyncio.create_task(handle_client(conn, addr))
