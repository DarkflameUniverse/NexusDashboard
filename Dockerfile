# syntax=docker/dockerfile:1

FROM python:3.11-slim-bookworm

RUN apt update
RUN apt -y install zip
RUN apt -y install imagemagick

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY wsgi.py wsgi.py
COPY entrypoint.sh entrypoint.sh
COPY ./app /app
COPY ./migrations /migrations

EXPOSE 8000
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
