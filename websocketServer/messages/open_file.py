import json
import os

import cv2

from websocketServer.sharedState import SharedState
from websocketServer.messages.message_handler import message_handler
from websocketServer.websocketHandler.websocket_send import send_data_to_client


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

    state.set_video_position(0)

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

    _, ext = os.path.splitext(file_path)
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    is_image = ext.lower() in image_extensions

    if not is_image:
        cap = cv2.VideoCapture(str(file_path))
        if not cap.isOpened():
            print(" Failed to open video.")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        message = json.dumps({
            "type": 'player',
            "isImage": False,
            "videoData": {
                'videoDuration': frame_count / fps if fps else 0
            }
        })
        await send_data_to_client(message)
    else:
        message = json.dumps({
            "type": 'player',
            "isImage": True,
        })
        await send_data_to_client(message)
