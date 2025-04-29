import cv2
import time
from ultralytics import YOLO
from dotenv import load_dotenv
import os


# Kamera-Stream mit YOLOv8n
CAMERA_URL = f"http://{os.getenv('STORAGE_CAM_3')}/axis-cgi/mjpg/video.cgi"

model = YOLO('yolov8n.pt')  # kleines YOLO Modell

def generate_camera_stream():
    cap = cv2.VideoCapture(CAMERA_URL)

    if not cap.isOpened():
        print("Kamera nicht erreichbar!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fehler beim Kamerabild")
            break

        # YOLO Personenerkennung
        results = model.predict(source=frame, conf=0.4, classes=[0], verbose=False)
        annotated = results[0].plot()

        _, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        #time.sleep(5)  # Nur alle 5 Sekunden ein Frame

    cap.release()