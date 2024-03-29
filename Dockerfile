FROM python:3.10-slim-buster
WORKDIR /bot/


COPY requirements.txt /tmp/
COPY src /bot/src
COPY data/resources /bot/data/resources

ENV TZ="Europe/Madrid"
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential libffi-dev  \
        libtiff-dev libfreetype6-dev \
        libwebp-dev sqlite\
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* \
        && pip3 install -r /tmp/requirements.txt --no-cache-dir && pip3 install python-dotenv --no-cache-dir\
        && rm /tmp/requirements.txt 

CMD [ "python3","/bot/src/main.py" ]
