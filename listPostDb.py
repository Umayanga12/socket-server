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

# Main entry function
def main():
    # Check if Redis is running
    redis_client = redis.from_url('redis://localhost')
    try:
        if not redis_client.ping():
            raise RuntimeError("IP storage (Redis) is not running")
    except redis.ConnectionError:
        raise RuntimeError("Failed to connect to Redis")

    # Start server and database listener processes with wrapper functions
    db_listener = multiprocessing.Process(target=start_db_listener)
    server_process = multiprocessing.Process(target=start_socket_server)

    # Start both processes
    db_listener.start()
    server_process.start()

    # Wait for processes to complete
    db_listener.join()
    server_process.join()

# Entry point
if __name__ == "__main__":
    main()
