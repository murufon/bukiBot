FROM python:3.7

RUN apt-get update && \
  apt-get install -y python-dev libmysqlclient.dev opus-tools ffmpeg

COPY ./requirements.txt /root/requirements.txt

WORKDIR /root

RUN pip install -r requirements.txt

RUN mkdir /root/bukibot

WORKDIR /root/bukibot
