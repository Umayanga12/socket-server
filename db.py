import redis.asyncio as redis
import asyncio
import redis.asyncio as aioredis
from redis.exceptions import RedisError, DataError
"""
Operations to interact with Redis database
    add, delete and rectrive client IP addresses
"""


# Initialize Redis connection
REDIS_DATABASE = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Redis key to store connected client IPs
CLIENTS_KEY = "connected_clients"

# Add IP into Redis when client connects to the server
async def add_client_ip(ip: str):
    """Adds the client IP address to a Redis set to ensure uniqueness."""
    try:
        if not ip:
            raise ValueError("IP address is required")

        # Add IP to Redis set (sadd ensures unique entries)
        async with REDIS_DATABASE.pipeline() as pipe:
            await pipe.sadd(CLIENTS_KEY, ip)
            await pipe.execute()
        return True

    except DataError as e:
        raise RuntimeError(f"Redis data error: {str(e)}")
    except RedisError as e:
        raise RuntimeError(f"Redis error occurred: {str(e)}")

# Remove IP from Redis when client disconnects from the server
async def remove_client_ip(ip: str):
    try:
        if not ip:
            raise ValueError("IP address is required")

        # Remove IP from Redis set
        async with REDIS_DATABASE.pipeline() as pipe:
            await pipe.srem(CLIENTS_KEY, ip)
            await pipe.execute()
        return True

    except redis.RedisError as e:
        raise RuntimeError(f"Redis error occurred: {str(e)}")

# Retrieve all client IPs from Redis
async def get_all_client_ips():
    try:
        # Retrieve all IPs in the set
        async with REDIS_DATABASE.pipeline() as pipe:
            result = await pipe.smembers(CLIENTS_KEY).execute()
            return result[0] if result else []

    except redis.RedisError as e:
        raise RuntimeError(f"Redis error occurred: {str(e)}")

# async def main():
#     # await add_client_ip('192.168.1.1')
#     # ips = await get_all_client_ips()
#     # print("Connected IPs:", ips)
#     await get_all_client_ips()
#     ips = await get_all_client_ips()
#     print("Connected IPs:", ips)
#     await REDIS_DATABASE.aclose()

# async def main():
#     test_ips = [
#         '192.168.1.1',
#         '192.168.1.2',
#         '192.168.1.3',
#         '192.168.1.4',
#         '192.168.1.5',
#         '192.168.1.6',
#         '192.168.1.7',
#         '192.168.1.8',
#         '192.168.1.9',
#         '192.168.1.10'
#     ]

#     # Add test IPs
#     for ip in test_ips:
#         await add_client_ip(ip)

#     # Get and print all IPs
#     ips = await get_all_client_ips()
#     print("Connected IPs:", ips)
#     await REDIS_DATABASE.aclose()


# asyncio.run(main())
