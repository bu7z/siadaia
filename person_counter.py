import os
import requests
from datetime import datetime
import psycopg2
from ultralytics import YOLO
from dotenv import load_dotenv

# === .env laden ===
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_ADDR"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

CAM_ADDR = os.getenv("ADDR_CAM", "localhost")
SNAPSHOT_URL = f"http://{CAM_ADDR}:8081"
SNAPSHOT_FILE = "snapshot.jpg"
MODEL_PATH = "yolov8n.pt"

# === Bild holen ===
try:
    response = requests.get(SNAPSHOT_URL, timeout=5)
    response.raise_for_status()
    with open(SNAPSHOT_FILE, "wb") as f:
        f.write(response.content)
    print(f"[{datetime.now()}] Snapshot gespeichert.")
except Exception as e:
    print(f"[{datetime.now()}] Fehler beim Laden des Snapshots: {e}")
    exit(1)

# === YOLO laden und Personen zählen ===
try:
    model = YOLO(MODEL_PATH)
    results = model(SNAPSHOT_FILE)
    person_count = sum(1 for cls_id in results[0].boxes.cls if int(cls_id) == 0)
    print(f"[{datetime.now()}] Personen erkannt: {person_count}")
except Exception as e:
    print(f"[{datetime.now()}] Fehler bei YOLO-Auswertung: {e}")
    exit(1)

# === In Datenbank eintragen ===
try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO person_count (timestamp, count) VALUES (%s, %s)",
        (datetime.now(), person_count)
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"[{datetime.now()}] Personenzahl in DB gespeichert.")
except Exception as e:
    print(f"[{datetime.now()}] Fehler beim Eintragen in die Datenbank: {e}")
    exit(1)

# === Aufräumen ===
try:
    os.remove(SNAPSHOT_FILE)
except FileNotFoundError:
    pass
