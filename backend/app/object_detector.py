import cv2
import time
from ultralytics import YOLO
from dotenv import load_dotenv
import os

load_dotenv()

CAMERA_URL_STO = f"http://{os.getenv('STORAGE_CAM_3')}/axis-cgi/mjpg/video.cgi"
CAMERA_URL_AUD = f"http://{os.getenv('AUDIENCE_CAM')}:8081"

model = YOLO('yolov8n.pt')  # kleines YOLO Modell


person_count = 0

def generate_camera_stream(cam):
    global person_count

    if cam == 1:
        cap = cv2.VideoCapture(CAMERA_URL_STO)
    elif cam == 2:
        cap = cv2.VideoCapture(CAMERA_URL_AUD)

    if not cap.isOpened():
        print("Kamera nicht erreichbar!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fehler beim Kamerabild")
            break

        results = model.predict(source=frame, conf=0.4, classes=[0, 39], verbose=False)
        annotated = results[0].plot()

        # Personenzahl zählen (Klasse 0 = person)
        person_count = sum(1 for c in results[0].boxes.cls if int(c) == 0)

        _, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
