FROM python:3.8

RUN apt update && \
  apt install -y python-dev default-libmysqlclient-dev opus-tools ffmpeg

COPY ./requirements.txt /root/requirements.txt

WORKDIR /root

RUN pip install -r requirements.txt

RUN mkdir /root/bukibot

WORKDIR /root/bukibot
