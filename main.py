import logging
import websockets
import asyncio

from websocketServer.websocketHandler.websocket_receive import handle_connection


logging.basicConfig(
    filename='videoReader.log', level=logging.INFO
)

async def main():
    logging.info('Starting app...')
    server = await websockets.serve(handle_connection, "localhost", 8081)
    print("WebSocket server running at ws://localhost:8081")
    logging.info('WebSocket server running at ws://localhost:8081')

    await asyncio.Future()


asyncio.run(main())
