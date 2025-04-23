import json
import os

from websocketServer.sharedState import SharedState
from websocketServer.messages.message_handler import message_handler


@message_handler("openFile")
async def handle_open_file(websocket, data):
    state = SharedState()
    file_path = data.get("payload")

    if not file_path:
        await websocket.send(json.dumps({
            "type": "openFile_response",
            "status": "error",
            "message": "Missing 'path' in request"
        }))
        return

    if os.path.exists(file_path) and os.path.isfile(file_path):
        state.set_selected_file_path(file_path)

        await websocket.send(json.dumps({
            "type": "openFile_response",
            "status": "success",
            "message": "File path received and valid",
            "path": file_path
        }))
    else:
        await websocket.send(json.dumps({
            "type": "openFile_response",
            "status": "error",
            "message": f"File does not exist at path: {file_path}"
        }))
