# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Systemabhängigkeiten installieren (z.B. für OpenCV)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Python-Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projektdateien kopieren
COPY ./app /app

# Optional: .env laden, falls benötigt
ENV PYTHONUNBUFFERED=1

# Production-Server starten
# Standard WSGI-Server für Production in Python
# Multiprozessfähig (-w 4 für 4 Worker – später anpassbar)
# ain:app bedeutet: in deiner main.py befindet sich app = Flask(__name__)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]