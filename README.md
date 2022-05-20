<h1 align="center">Furbot</h1>

<p align="center">
    <img  width=25% src="./assets/logo.png"  >
</p>


<div align="center"><a href="https://www.codefactor.io/repository/github/tekofx/furbot"><img src="https://www.codefactor.io/repository/github/tekofx/furbot/badge" alt="CodeFactor" /></a></div>

<p align="center">Bot para el servidor de Villafurrense</p>

# Ejecución en docker-compose (recomendado):
- Descargar el archivo docker-compose y cambiar las rutas de los volúmenes
- En la carpeta que corresponde al volumen /bot/env colocar el archivo furbot.env rellenando los tokens 
- `docker-compose up -d`

# Ejecución sin docker
- Clonar el repositorio
- Rellenar el archivo env/furbot.env con los tokens
- `python3 src/main.py`


## Demo
![Demo](assets/demo.gif)
