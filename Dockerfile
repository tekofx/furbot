FROM python:3.8-slim-buster

WORKDIR /bot/
COPY requirements.txt .

RUN pip3 install -r requirements.txt


CMD [ "python3","/bot/src/main.py" ]
