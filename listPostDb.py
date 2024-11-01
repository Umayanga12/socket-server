import os
import asyncio
import asyncpg

DATABASE_CONFIG = {
    'user': 'your_user',
    'password': 'your_password',
    'database': 'your_database',
    'host': 'localhost'
}

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
