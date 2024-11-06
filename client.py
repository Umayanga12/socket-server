import asyncio
import websockets
import logging

logging.basicConfig(level=logging.INFO)

# This is the WebSocket handler
async def handle_client(websocket, path):
    client_ip = websocket.remote_address[0]
    logging.info(f"New connection from IP: {client_ip}")

    try:
        async for message in websocket:
            logging.info(f"Received message from {client_ip}: {message}")
    except websockets.ConnectionClosed as e:
        logging.info(f"Connection closed for {client_ip}: {e}")


async def main():
    server = await websockets.serve(handle_client, "0.0.0.0", 12333)
    print("WebSocket server started...")
    await server.wait_closed()

# Run the server
asyncio.run(main())
