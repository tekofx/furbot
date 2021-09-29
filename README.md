<h1 align="center">Furbot</h1>

<div align="center"><a href="https://www.codefactor.io/repository/github/tekofx/furbot"><img src="https://www.codefactor.io/repository/github/tekofx/furbot/badge" alt="CodeFactor" /></a></div>

<p align="center">Bot para el servidor de Villafurrense</p>

![Demo](assets/demo.gif)


- [Ejecución en docker:](#ejecución-en-docker)
  - [Construir](#construir)
  - [Ejecutar](#ejecutar)
  - [Ejecucion automatica al reinicar el sistema](#ejecucion-automatica-al-reinicar-el-sistema)
  - [Iniciar reiniciar y detener](#iniciar-reiniciar-y-detener)
- [Ejecucion sin docker](#ejecucion-sin-docker)
# Ejecución en docker:



Si es la primera vez que se ejecuta:

## Construir

```sh
docker build --no-cache -t furbot .
```
## Ejecutar
```sh
docker run -d \           
  --env-file <env_file> \
  --name furbot \
  --mount type=bind,src=<furbot_folder>/files/,dst=/bot/files/  \
  --mount type=bind,src=<furbot_folder>/src/,dst=/bot/src \
  --restart=unless-stopped \
  -p 80:80 furbot
```

## Ejecucion automatica al reinicar el sistema
```sh
docker update --restart=unless-stopped furbot
```


## Iniciar reiniciar y detener

Para iniciar, reiniciar o detener:

```sh
docker start furbot # Iniciar docker
docker restart furbot # Reiniciar docker
docker stop furbot # Detener docker
```

# Ejecucion sin docker
- Añadir a la carpeta del bot el archivo .env
```sh
python3 src/main.py
```