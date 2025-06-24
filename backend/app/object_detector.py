import cv2
import time
from threading import Lock
from ultralytics import YOLO
from dotenv import load_dotenv
import os

load_dotenv()

# Globale Variablen
model = YOLO('yolov8n.pt')
person_count = 0
person_count_lock = Lock()
cap_sto = None
cap_aud = None

def get_person_count() -> int:
    """Thread-sichere Abfrage der Personenzahl"""
    with person_count_lock:
        return person_count

def init_camera(cam_type: int):
    """Initialisiert die Kamera"""
    global cap_sto, cap_aud
    try:
        if cam_type == 1 and cap_sto is None:
            cap_sto = cv2.VideoCapture(f"http://{os.getenv('STORAGE_CAM_3')}/axis-cgi/mjpg/video.cgi")
            cap_sto.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        elif cam_type == 2 and cap_aud is None:
            cap_aud = cv2.VideoCapture(f"http://{os.getenv('AUDIENCE_CAM')}:8081")
            cap_aud.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    except Exception as e:
        print(f"Kamerafehler: {str(e)}")

def get_latest_frame(cam_type: int):
    """Holt das aktuellste Frame"""
    cap = cap_sto if cam_type == 1 else cap_aud
    if cap is None or not cap.isOpened():
        return None
    
    for _ in range(3):  # Puffer leeren
        cap.grab()
    ret, frame = cap.retrieve()
    return frame if ret else None

def generate_camera_stream(cam_type: int):
    """Generiert den Video-Stream"""
    global person_count
    
    init_camera(cam_type)
    cap = cap_sto if cam_type == 1 else cap_aud

    if cap is None or not cap.isOpened():
        print("Kamera nicht verfügbar")
        return

    while True:
        try:
            # Puffer leeren
            for _ in range(3):
                cap.grab()
            
            ret, frame = cap.read()
            if not ret:
                print("Frame konnte nicht gelesen werden")
                time.sleep(0.1)
                continue

            # Objekterkennung
            results = model.predict(source=frame, conf=0.4, classes=[0], verbose=False)
            
            with person_count_lock:
                person_count = sum(1 for c in results[0].boxes.cls if int(c) == 0)

            # Frame encodieren
            _, buffer = cv2.imencode('.jpg', results[0].plot())
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        except Exception as e:
            print(f"Fehler im Stream: {str(e)}")
            time.sleep(1)

def cleanup():
    """Gibt Ressourcen frei"""
    global cap_sto, cap_aud
    if cap_sto is not None:
        cap_sto.release()
        cap_sto = None
    if cap_aud is not None:
        cap_aud.release()
        cap_aud = None
