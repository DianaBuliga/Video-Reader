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

        while cap.isOpened() and state.get_video_processing_active():
            ret, frame = cap.read()
            if not ret:
                break
            await process_frame_and_send(frame)

        cap.release()


async def process_frame_and_send(frame):
    # Run YOLO detection on the frame
    results = model(frame)[0]

    _, buffer = cv2.imencode('.jpg', frame)
    frame_data_base64 = base64.b64encode(buffer).decode('utf-8')

    message_info, detections = create_message(results)

    data = [
        {
            "type": 'image',
            "imageType": 'jpg',
            "count": len(detections),
            "objects": detections,
            "frame": frame_data_base64
        },
        {
            "type": 'data',
            "objects": message_info
        }]

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
                "otherInfo": {'type': 'string'}  # You can customize this
            }
        else:
            data[class_name]["number"] += 1
            # data[class_name]["otherInfo"].append({'type': 'string'})

    return data, detections
