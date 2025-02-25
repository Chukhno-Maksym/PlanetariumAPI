FROM python:3.12.9-alpine
LABEL maintainer="maksym.chukhno@gmail.com"

ENV PYTHONUNBUFFERED = 1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
