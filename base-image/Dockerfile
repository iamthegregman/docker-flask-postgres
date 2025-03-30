FROM python:3.9-alpine

WORKDIR /home/app/

COPY requirements.txt .

RUN apk add --no-cache postgresql-dev gcc musl-dev && \
    pip install --upgrade pip setuptools && \
    pip install -r requirements.txt