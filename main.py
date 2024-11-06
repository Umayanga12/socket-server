import multiprocessing
import redis
import asyncio
from socketserver import start_socketserver
from listPostDb import listen_to_db
from concurrent.futures import ProcessPoolExecutor

# Main entry function
async def main():
    # Run the server and database listener concurrently
    redis_client = redis.Redis()
    response = await redis.from_url('redis://localhost').ping()
    if not response:
        raise RuntimeError("ip storage is not running")
    dbListener = multiprocessing.Process(target=listen_to_db)
    serverProcess = multiprocessing.Process(target=start_socketserver)

    # Start processes directly instead of using gather
    dbListener.start()
    serverProcess.start()

    # Wait for processes to complete
    dbListener.join()
    serverProcess.join()

# Multiprocessing to start server and database listener in separate processes
if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
