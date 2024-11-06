import asyncio
import asyncpg
import json
import os

from dotenv import load_dotenv
import multiprocessing
from db import get_all_client_ips


clients = set()

load_dotenv(dotenv_path='./.env')

DATABASE_CONFIG =  {
    'database': 'API-DB',
    'user': 'user',
    'password': '123456',
    'host': '127.0.0.1',
    'port': '5432'
}


"""
Operations to interact with PostgreSQL database and notify clients of changes
"""
async def listen_to_db():
    """Listens for changes in the specified database channel."""
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        await conn.add_listener('vehicle_number_palates_changes', notify_clients)
        print("Listening for database changes on vehicle_number_palates_changes channel...")

        await asyncio.Future()
    except Exception as e:
        print(f"Database connection error: {e}")


async def notify_clients(conn, pid, channel, payload):
    """Notify all connected clients with the payload if they are in the allowed client IPs."""
    try:
        if not clients:
            print("No connected clients to notify.")
            return json.dumps([])

        try:
            message = json.loads(payload)
            print(f"Received notification: {message}")
        except json.JSONDecodeError:
            print("Failed to decode payload as JSON")
            return json.dumps({"error": "Invalid payload format"})

        client_ips = await get_all_client_ips()
        issend = await asyncio.gather(
            *[client.send(payload) for client in clients if client.remote_address[0] in client_ips],
            return_exceptions=True  # Optional: Catch exceptions per client
        )
        results = [res if not isinstance(res, Exception) else str(res) for res in issend]
        return json.dumps(results)

    except Exception as e:
        print(f"Error in notify_clients: {e}")
        return json.dumps({"error": str(e)})
