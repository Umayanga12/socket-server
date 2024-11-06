import multiprocessing
import redis
import asyncio
from socketserver import start_socketserver
from server import listen_to_db

# Wrapper for starting the async database listener
def start_db_listener():
    asyncio.run(listen_to_db())

# Wrapper for starting the async socket server
def start_socket_server():
    asyncio.run(start_socketserver())
