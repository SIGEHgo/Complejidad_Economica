FROM python:3.8-slim-buster



RUN apt-get update
RUN apt-get install nano

RUN mkdir wd
WORKDIR wd
COPY app/requirements.txt .
RUN pip3 install -r requirements.txt

COPY app/ ./
CMD [ "gunicorn", "--workers=1", "--threads=2", "-b", "0.0.0.0:80", "--timeout", "600", "--preload", "app:server"]
