import asyncio
import os
from db import add_client_ip,remove_client_ip

DISCONNECT_MESSAGE = "DISCONNECT!!"
CONNECT_MESSAGE = "CONNECT!!"
FORMAT = os.environ.get("FORMAT", "utf-8")

"""
Operations related to the client connection
    To store the client ip address use inmemory database
            here - redis is used
        Adding and removing client IPs when client conneted to the server and disconnet form the server
"""

# Dictionary to store client IPs
connected_clients = {}

# Async function to handle each client connection
async def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected_clients[addr] = 'connected'
    # Save client IP in redis
    await add_client_ip(addr)
    connected = True
    try:
        while connected:
            msg = await asyncio.to_thread(conn.recv, 1024)
            if not msg or msg.decode(FORMAT) == DISCONNECT_MESSAGE:
                connected = False
                print(f"[DISCONNECTED] {addr} disconnected.")
            else:
                print(f"[{addr}] {msg.decode(FORMAT)}")
                # Echo message back to client
                await asyncio.to_thread(conn.send, msg)
    finally:
        await remove_client_ip(addr)
        conn.close()
