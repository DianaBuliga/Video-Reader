import json

from object_detection import send_yolo_detections
from websocketServer.messages.message_handler import message_handler
from websocketServer.sharedState import SharedState


@message_handler("playVideo")
async def handle_play_video(websocket, data):
    state = SharedState()
    print('video handler receive', state.get_selected_file_path())
    await send_yolo_detections(state.get_selected_file_path())
