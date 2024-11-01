import asyncio
import os

DISCONNECT_MESSAGE = "DISCONNECT!!"
CONNECT_MESSAGE = "CONNECT!!"
FORMAT = os.environ.get("FORMAT", "utf-8")

# Dictionary to store client IPs
connected_clients = {}

# Async function to handle each client connection
async def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected_clients[addr] = 'connected'  # Store IP address
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
        # Remove client from the dictionary on disconnect
        connected_clients.pop(addr, None)
        conn.close()
