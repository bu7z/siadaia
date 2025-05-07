FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY person_counter.py .
COPY .env .
COPY yolov8n.pt .

RUN apt-get update && apt-get install -y cron

COPY crontab.txt /etc/cron.d/person-cron
RUN chmod 0644 /etc/cron.d/person-cron && crontab /etc/cron.d/person-cron

CMD ["cron", "-f"]
