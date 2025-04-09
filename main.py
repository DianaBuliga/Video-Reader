import websockets
import asyncio
from object_detection import show_results
from websocket_server import handle_connection, send_yolo_detections


async def main():
    server = await websockets.serve(handle_connection, "localhost", 8081)
    print("WebSocket server running at ws://localhost:8081")

    await asyncio.gather(server.wait_closed(), send_yolo_detections())


asyncio.run(main())
