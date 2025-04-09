import asyncio
import base64

import websockets
import json
import cv2
from ultralytics import YOLO

connected_clients = set()

model = YOLO("yolo11n.pt")  # Load YOLO model


async def handle_connection(websocket):
    connected_clients.add(websocket)
    print(f"Client connected: {websocket.remote_address}")
    try:
        while True:
            await asyncio.sleep(1)  # Keep connection alive
    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")
    finally:
        connected_clients.remove(websocket)


async def send_data_to_client(message):
    print(f"message: {message}")
    for client in connected_clients.copy():
        try:
            await client.send(message)
        except websockets.exceptions.ConnectionClosed:
            connected_clients.remove(client)

    await asyncio.sleep(0.04)  # ~25 fps


async def send_yolo_detections():
    video_path = "intersection1.mp4"  # Specify the path to your video file
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO detection on the frame
        results = model(frame)[0]

        detections = []
        for box in results.boxes:
            cls = int(box.cls[0])
            class_name = results.names[cls]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            detections.append({
                "class": class_name,
                "box": [x1, y1, x2, y2]
            })

            # Draw bounding boxes on the frame
            color = (0, 255, 0)  # Green for the boxes
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # Encode the frame to JPG format
        _, buffer = cv2.imencode('.jpg', frame)

        # Convert the binary data to base64 string
        frame_data_base64 = base64.b64encode(buffer).decode('utf-8')

        # Prepare the detection data
        data = {
            "count": len(detections),
            "objects": detections,
            "frame": frame_data_base64  # Send the frame as bytes
        }

        message = json.dumps(data)

        # Send the data to connected clients
        await send_data_to_client(message)

    cap.release()

