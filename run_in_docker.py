#!/usr/bin/python3

import os
import subprocess


# Get ports available
print("Getting port available")
result = subprocess.Popen(
    "docker ps --format '{{.Ports}}' | cut -d ' ' -f2 | cut -b 4-5 ",
    shell=True,
    stdout=subprocess.PIPE,
)

result = result.stdout.read()
result = result.decode("utf-8")
result = result.split("\n")

ports = []
for x in result[:-1]:
    ports.append(int(x))

count = 80
while True:
    if count not in ports:
        port = count
        break
    count += 1
print("Port available: ", port)


# Get path
path = os.path.dirname(os.path.abspath(__file__))

# Build
print("Building furbot docker image")
os.system("docker build --no-cache -t furbot .")


# Run
print("Running docker container")
docker_run = """ docker run -d \
    --name furbot \
    --mount type=bind,src={path}/files/,dst=/bot/files/  \
    --mount type=bind,src={path}/src/,dst=/bot/src \
    --restart=unless-stopped \
    -p {port}:80 furbot """
docker_run = docker_run.format(path=path, port=port)


os.system(docker_run)
