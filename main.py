import multiprocessing
import redis
import asyncio
from listPostDb import start_db_listener,start_socket_server
from concurrent.futures import ProcessPoolExecutor

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
