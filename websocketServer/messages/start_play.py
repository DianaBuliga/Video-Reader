import asyncio

from object_detection import send_yolo_detections
from websocketServer.messages.message_handler import message_handler
from websocketServer.sharedState import SharedState


@message_handler("startPlay")
async def handle_start_play(websocket, data):
    state = SharedState()
    print('video handler receive', state.get_selected_file_path())
    state.set_video_processing_active(True)

    asyncio.create_task(send_yolo_detections())
