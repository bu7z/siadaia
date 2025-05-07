FROM python:3.11-slim

WORKDIR /app

# Install system packages (cron + OpenCV dependencies)
RUN apt-get update && apt-get install -y \
    cron \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY person_counter.py .
COPY .env .
COPY yolov8n.pt .

# Set up cron
COPY crontab.txt /etc/cron.d/person-cron
RUN chmod 0644 /etc/cron.d/person-cron && crontab /etc/cron.d/person-cron

CMD ["cron", "-f"]
