import json

from websocketServer.messages.message_handler import message_handlers
from websocketServer.messages.open_file import handle_open_file
from websocketServer.messages.start_play import handle_start_play
from websocketServer.messages.stop_play import handle_stop_play
from websocketServer.sharedState import SharedState


async def handle_connection(websocket):
    state = SharedState()
    state.add_client(websocket)
    print(f" Client connected: {websocket.remote_address}")

    try:
        async for message in websocket:
            print(f" Received: {message}")
            try:
                data = json.loads(message)
                msg_type = data.get("type")
                print(msg_type)

                handler = message_handlers.get(msg_type)

                if handler:
                    await handler(websocket, data)
                else:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"Unknown message type: {msg_type}"
                    }))
            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON"
                }))
    except:
        pass
    finally:
        state.remove_client(websocket)

        print(" Client disconnected")
