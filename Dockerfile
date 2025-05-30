FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY person_counter.py .
COPY .env .
COPY yolov8n.pt .
RUN touch /app/log.txt
ENV YOLO_CONFIG_DIR=/tmp/ultralytics

# Add OpenCV dependency here
RUN apt-get update && apt-get install -y \
    cron \
    libgl1 \
    libglib2.0-0 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*


COPY crontab.txt /etc/cron.d/person-cron
RUN chmod 0644 /etc/cron.d/person-cron && crontab /etc/cron.d/person-cron

ENTRYPOINT ["cron", "-f"]
