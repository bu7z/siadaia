import cv2
import time
from threading import Lock
from ultralytics import YOLO
from dotenv import load_dotenv
import os

load_dotenv()

# Globale Variablen (mit Getter/Setter)
_model = YOLO('yolov8n.pt')
_person_count = 0
_lock = Lock()
_cap_sto = None
_cap_aud = None

# ---- Öffentliche API ----
def get_person_count() -> int:
    """Thread-sichere Abfrage der Personenzahl"""
    with _lock:
        return _person_count

def init_camera(cam_type: int):
    """Initialisiert die Kamera (wird von Flask-Endpoint aufgerufen)"""
    global _cap_sto, _cap_aud
    try:
        if cam_type == 1 and _cap_sto is None:
            _cap_sto = _create_capture(cam_type)
        elif cam_type == 2 and _cap_aud is None:
            _cap_aud = _create_capture(cam_type)
    except Exception as e:
        print(f"Kamerafehler: {str(e)}")

def get_latest_frame(cam_type: int):
    """Holt das aktuellste Frame (mit Puffer-Leerung)"""
    cap = _cap_sto if cam_type == 1 else _cap_aud
    if cap is None:
        return None
    
    for _ in range(3):  # Puffer leeren
        cap.grab()
    ret, frame = cap.retrieve()
    return frame if ret else None

def generate_camera_stream(cam_type: int):
    """Generator für Video-Stream (mit automatischer Initialisierung)"""
    global _person_count, _cap_sto, _cap_aud
    
    if cam_type not in (1, 2):
        raise ValueError("Ungültiger Kameratyp")

    cap = _cap_sto if cam_type == 1 else _cap_aud
    if cap is None:
        init_camera(cam_type)
        cap = _cap_sto if cam_type == 1 else _cap_aud
        if cap is None:
            raise RuntimeError(f"Kamera {cam_type} konnte nicht initialisiert werden")

    while True:
        try:
            frame = get_latest_frame(cam_type)
            if frame is None:
                time.sleep(0.1)
                continue

            results = _model.predict(source=frame, conf=0.4, classes=[0], verbose=False)
            with _lock:
                _person_count = sum(1 for c in results[0].boxes.cls if int(c) == 0)

            _, buffer = cv2.imencode('.jpg', results[0].plot())
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
        except Exception as e:
            print(f"Stream-Fehler: {str(e)}")
            time.sleep(1)  # Kurze Pause bei Fehlern

# ---- Private Hilfsfunktionen ----
def _create_capture(cam_type: int):
    """Erstellt VideoCapture-Instanz mit optimierten Einstellungen"""
    urls = {
        1: f"http://{os.getenv('STORAGE_CAM_3')}/axis-cgi/mjpg/video.cgi",
        2: f"http://{os.getenv('AUDIENCE_CAM')}:8081"
    }
    cap = cv2.VideoCapture(urls[cam_type])
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    if not cap.isOpened():
        raise ConnectionError(f"Kamera {cam_type} nicht erreichbar")
    return cap

def cleanup():
    """Sollte beim Beenden aufgerufen werden"""
    if _cap_sto: _cap_sto.release()
    if _cap_aud: _cap_aud.release()