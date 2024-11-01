import multiprocessing
import asyncio
from server import start_server
from listPostDb import listen_to_db
from concurrent.futures import ProcessPoolExecutor

# Main entry function
async def main():
    # Run the server and database listener concurrently
    await asyncio.gather(start_server(), listen_to_db())

# Multiprocessing to start server and database listener in separate processes
if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
