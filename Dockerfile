FROM python:3.7-alpine
MAINTAINER matfij

ENV PYTHONUNBUFFORED 1

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

RUN mkdir /pp
WORKDIR /app
COPY ./app /app

RUN adduser -D runuser
USER runuser
