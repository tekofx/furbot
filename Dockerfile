FROM python:3.8-slim-buster

WORKDIR /bot/
COPY requirements.txt /tmp/

RUN apt-get update && apt-get install -y \
        python-dev python-pip python-setuptools \
        libffi-dev libxml2-dev libxslt1-dev \
        libtiff-dev zlib1g-dev libfreetype6-dev \
        liblcms2-dev libwebp-dev

RUN pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt


CMD [ "python3","/bot/src/main.py" ]