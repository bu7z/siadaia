import cv2
import time
from ultralytics import YOLO
from dotenv import load_dotenv
import os


# Kamera-Stream mit YOLOv8n
CAMERA_URL_STO = f"http://{os.getenv('STORAGE_CAM_3')}/axis-cgi/mjpg/video.cgi"
CAMERA_URL_AUD = f"http://{os.getenv('AUDIENCE_CAM')}:8081"

model = YOLO('yolov8n.pt')  # kleines YOLO Modell

def generate_camera_stream(cam):
    if cam == 1:
        cap = cv2.VideoCapture(CAMERA_URL_STO)
    elif cam ==2:
        cap = cv2.VideoCapture(CAMERA_URL_AUD)
        

    if not cap.isOpened():
        print("Kamera nicht erreichbar!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fehler beim Kamerabild")
            break

        # YOLO Personenerkennung
        results = model.predict(source=frame, conf=0.4, classes=[0,39], verbose=False)
        annotated = results[0].plot()

        _, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        #time.sleep(5)  # Nur alle 5 Sekunden ein Frame

    cap.release()