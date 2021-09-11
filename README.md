<h1 align="center">Furbot</h1>

<div align="center"><a href="https://www.codefactor.io/repository/github/tekofx/furbot"><img src="https://www.codefactor.io/repository/github/tekofx/furbot/badge" alt="CodeFactor" /></a></div>

<p align="center">Bot para el servidor de Villafurrense</p>

![Demo](assets/demo.gif)

## Ejecución:

El bot se ejecuta en un contenedor docker.

Si es la primera vez que se ejecuta:

```sh
docker build --no-cache -t furbot .

docker run -d\
 --name furbot \
 --mount type=bind,src=<furbot_folder>/files/,dst=/bot/files/ \
 --mount type=bind,src=<furbot_folder>/src/,dst=/bot/src \
 -p 80:80 \
 furbot


```

Para iniciar, reiniciar o detener:

```
docker start furbot # Iniciar docker
docker restart furbot # Reiniciar docker
docker stop furbot # Detener docker
```
