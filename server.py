import socket
import os
import asyncio
import asyncpg
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process

# Server configuration
SERVER = socket.gethostbyname(socket.gethostname())
PORT = int(os.environ.get("SERVERPORT", 5000))
ADDRESS = (SERVER, PORT)
FORMAT = os.environ.get("FORMAT", "utf-8")
DISCONNECT_MESSAGE = "DISCONNECT!!"
CONNECT_MESSAGE = "CONNECT!!"
DATABASE_CONFIG = {
    'user': 'your_user',
    'password': 'your_password',
    'database': 'your_database',
    'host': 'localhost'
}

# Dictionary to store client IPs
connected_clients = {}

# Initialize server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

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

# Async function to accept incoming connections
async def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    loop = asyncio.get_running_loop()
    while True:
        conn, addr = await loop.run_in_executor(None, server.accept)
        asyncio.create_task(handle_client(conn, addr))

# Async function to listen for PostgreSQL notifications
async def listen_to_db():
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        await conn.add_listener('vehicle_number_palates_changes', notify_clients)
        print("Listening for database changes on vehicle_number_palates_changes channel...")
        await asyncio.Future()  # Keeps the coroutine running indefinitely
    except Exception as e:
        print(f"Database connection error: {e}")

# Notification callback function
async def notify_clients(connection, pid, channel, payload):
    print(f"[NOTIFICATION] Received {payload} on {channel}")
    # Here you can notify connected clients if needed

# Main entry function
async def main():
    # Run the server and database listener concurrently
    await asyncio.gather(start_server(), listen_to_db())

# Multiprocessing to start server and database listener in separate processes
if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
