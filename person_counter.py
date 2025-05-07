import os
import cv2
import psycopg2
import requests
from datetime import datetime
from ultralytics import YOLO
from dotenv import load_dotenv

print(f"[{datetime.now()}] --- person_counter.py gestartet ---")

# === .env laden ===
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_ADDR"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

CAM_ADDR = os.getenv("ADDR_CAM", "10.0.0.2:8081")
SNAPSHOT_URL = f"http://{CAM_ADDR}"
SNAPSHOT_FILE = "snapshot.jpg"
MODEL_PATH = "yolov8n.pt"

# === Einzelbild vom MJPEG-Stream abgreifen ===
print(f"[{datetime.now()}] Hole einen Frame aus dem MJPEG-Stream ({SNAPSHOT_URL})...")

try:
    cap = cv2.VideoCapture(SNAPSHOT_URL)
    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        print(f"[{datetime.now()}] ❌ Kein gültiger Frame vom Kamera-Stream erhalten!")
        exit(1)

    cv2.imwrite(SNAPSHOT_FILE, frame)
    print(f"[{datetime.now()}] ✅ Frame gespeichert als {SNAPSHOT_FILE}")
except Exception as e:
    print(f"[{datetime.now()}] ❌ Fehler beim Zugriff auf den Stream: {e}")
    exit(1)

# === YOLO laden und Personen zählen ===
print(f"[{datetime.now()}] Lade YOLO-Modell...")

try:
    model = YOLO(MODEL_PATH)
    print(f"[{datetime.now()}] Modell geladen. Erkenne Personen...")
    results = model(SNAPSHOT_FILE)
    person_count = sum(1 for cls_id in results[0].boxes.cls if int(cls_id) == 0)
    print(f"[{datetime.now()}] 👥 Personen erkannt: {person_count}")
except Exception as e:
    print(f"[{datetime.now()}] ❌ Fehler bei YOLO-Auswertung: {e}")
    exit(1)

# === In Datenbank eintragen ===
print(f"[{datetime.now()}] Versuche Verbindung zur Datenbank...")

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    print(f"[{datetime.now()}] Verbindung erfolgreich. Eintrag wird geschrieben...")
    cur.execute(
        "INSERT INTO person_count (timestamp, count) VALUES (%s, %s)",
        (datetime.now(), person_count)
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"[{datetime.now()}] ✅ Personenzahl in DB gespeichert.")
except Exception as e:
    print(f"[{datetime.now()}] ❌ Fehler beim Eintragen in die Datenbank: {e}")
    exit(1)

# === Aufräumen ===
try:
    os.remove(SNAPSHOT_FILE)
    print(f"[{datetime.now()}] 🧹 Snapshot gelöscht.")
except FileNotFoundError:
    pass
