FROM python:3.7-alpine
MAINTAINER matfij

ENV PYTHONUNBUFFORED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
  gcc libc-dev linux-headers postgresql-dev
RUN pip3 install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /pp
WORKDIR /app
COPY ./app /app

RUN adduser -D runuser
USER runuser
