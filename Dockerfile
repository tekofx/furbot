FROM python:3.8-slim-buster

WORKDIR /bot/
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    make \
    gcc \
    && pip install -r requirements.txt \
    && apt-get remove -y --purge make gcc build-essential \
    && apt-get autoremove -y 


CMD [ "python3","/bot/src/main.py" ]
