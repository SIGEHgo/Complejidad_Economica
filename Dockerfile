FROM python:3.11-slim-buster



RUN apt-get update
RUN apt-get install nano

COPY app/requirements.txt .
RUN pip3 install -r requirements.txt

COPY app/ ./
EXPOSE 80
CMD [ "gunicorn", "--workers=1", "--threads=2", "-b", "0.0.0.0:80", "--timeout", "600", "--preload", "app:server"]
