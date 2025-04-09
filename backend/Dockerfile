# backend/Dockerfile
#FROM python:3.11-slim

#WORKDIR /app
#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

#COPY ./app /app

#CMD ["python", "app/main.py"]

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

CMD ["flask", "run", "--host=0.0.0.0"]

