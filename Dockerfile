FROM python:3.8-slim-buster



RUN apt-get update
RUN apt-get install nano

RUN mkdir wd
WORKDIR wd
COPY app/requirements.txt .
RUN pip3 install -r requirements.txt

COPY app/ ./
EXPOSE 10000
CMD echo "Gunicorn running on port: $PORT" && gunicorn --workers=3 --threads=1 -b 0.0.0.0 --timeout 600 --log-level debug app:server