FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR usr/src/fabrique_st

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt