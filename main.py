import websockets
import asyncio

from websocketServer.websocketHandler.websocket_receive import handle_connection


async def main():
    server = await websockets.serve(handle_connection, "localhost", 8081)
    print("WebSocket server running at ws://localhost:8081")

    await asyncio.Future()


asyncio.run(main())
