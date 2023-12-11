FROM python:3.9.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/transferring_things/ad_things

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/
RUN pip install -r /usr/src/requirements.txt

COPY ./ad_things /usr/src/transferring_things/ad_things

