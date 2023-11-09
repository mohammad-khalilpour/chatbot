FROM python:3.11.2-slim

COPY requirements.txt app/requirements.txt

RUN pip install -r app/requirements.txt

COPY . ./app
