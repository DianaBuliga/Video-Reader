import json

from object_detection import send_yolo_detections
from websocketServer.messages.message_handler import message_handler
from websocketServer.sharedState import SharedState


@message_handler("stopPlay")
async def handle_stop_play(websocket, data):
    state = SharedState()
    print('stop play received')
    state.set_video_processing_active(False)
