import base64
from pathlib import Path
from ultralytics import YOLO
import cv2
import json

from websocketServer.sharedState import SharedState
from websocketServer.websocketHandler.websocket_send import send_data_to_client

model = YOLO("yolo11n.pt")  # Load YOLO model
state = SharedState()


async def send_yolo_detections():
    file_path = Path(state.get_selected_file_path())

    # Determine if it's a photo or a video based on extension
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    is_image = file_path.suffix.lower() in image_extensions

    if is_image:
        # Handle image detection
        image = cv2.imread(str(file_path))
        if image is None:
            print(" Failed to read the image.")
            return
        await process_frame_and_send(image)
    else:
        cap = cv2.VideoCapture(str(file_path))
        if not cap.isOpened():
            print(" Failed to open video.")
            return

        start_time = state.get_video_position()
        cap.set(cv2.CAP_PROP_POS_MSEC, start_time)

        while cap.isOpened() and state.get_video_processing_active():
            ret, frame = cap.read()
            if not ret:
                break
            current_pos = cap.get(cv2.CAP_PROP_POS_MSEC)
            state.set_video_position(current_pos)
            await process_frame_and_send(frame, current_pos/1000.0)

        cap.release()


async def process_frame_and_send(frame, current_pos):
    # Run YOLO detection on the frame
    results = model(frame)[0]

    height, width = frame.shape[:2]

    _, buffer = cv2.imencode('.jpg', frame)
    frame_data_base64 = base64.b64encode(buffer).decode('utf-8')

    message_info, detections = create_message(results)

    data = [
        {
            "type": 'image',
            "frameData": {
                "imageType": 'jpg',
                "count": len(detections),
                "objects": detections,
                "frame": frame_data_base64,
                "width": width,
                "height": height
            }
        },
        {
            "type": 'data',
            "objects": message_info
        },
        {
            "type": 'player',
            "timeFrame": current_pos
        }
    ]

    message = json.dumps(data)
    await send_data_to_client(message)


def create_message(results):
    data = {}
    detections = []

    for box in results.boxes:
        cls = int(box.cls[0])
        class_name = results.names[cls]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        detections.append({
            "class": class_name,
            "box": [x1, y1, x2, y2]
        })

        if class_name not in data:
            data[class_name] = {
                "number": 1,
                "otherInfo": {'type': 'string'}
            }
        else:
            data[class_name]["number"] += 1

    return data, detections
