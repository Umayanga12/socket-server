import redis
import asyncio

# Initialize Redis connection
REDIS_DATABASE = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Redis key to store connected client IPs
CLIENTS_KEY = "connected_clients"

#add ip into redis when client connected to the server
async def add_client_ip(ip: str):
    try:
        if not ip:
            raise ValueError("IP address is required")

        # Add IP to Redis set (unique entries)
        with await REDIS_DATABASE.pipeline() as pipe:
            await pipe.sadd(CLIENTS_KEY, ip)
            await pipe.execute()
        return True

    except redis.RedisError as e:
        raise RuntimeError(f"Redis error occurred: {str(e)}")

#remove ip from redis when client disconnected from the server
async def remove_client_ip(ip: str):
    try:
        if not ip:
            raise ValueError("IP address is required")

        # Remove IP from Redis set
        with await REDIS_DATABASE.pipeline() as pipe:
            await pipe.srem(CLIENTS_KEY, ip)
            await pipe.execute()
        return True

    except redis.RedisError as e:
        raise RuntimeError(f"Redis error occurred: {str(e)}")
#rectrive all the client ips from redis
async def get_all_client_ips():
    try:
        # Retrieve all IPs in the set
        with await REDIS_DATABASE.pipeline() as pipe:
            result = await pipe.smembers(CLIENTS_KEY).execute()
            return result[0] if result else []

    except redis.RedisError as e:
        raise RuntimeError(f"Redis error occurred: {str(e)}")
