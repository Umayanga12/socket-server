import asyncio
import asyncpg
import json
import os
from dotenv import load_dotenv
import multiprocessing
clients = set()

load_dotenv(dotenv_path='./.env')

DATABASE_CONFIG =  {
    'database': 'API-DB',
    'user': 'user',
    'password': '123456',
    'host': 'localhost',
    'port': '5432'
}


"""
Operations to interact with PostgreSQL database and notify clients of changes
"""
async def listen_to_db():
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        await conn.add_listener('vehicle_number_palates_changes', notify_clients)
        print("Listening for database changes on vehicle_number_palates_changes channel...")
        await asyncio.Future()  # Keeps the coroutine running indefinitely
    except Exception as e:
        print(f"Database connection error: {e}")

async def notify_clients(conn, pid, channel, payload):
    if clients:  # Notify clients only if they are connected
        message = json.loads(payload)
        print(f"Received notification: {message}")
        await asyncio.gather(*[client.send(payload) for client in clients])
