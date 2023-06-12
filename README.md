<h1 align="center">Furbot</h1>

<p align="center">
    <img  width=25% src="./assets/logo.png"  >
</p>

<div align="center"><a href="https://www.codefactor.io/repository/github/tekofx/furbot"><img src="https://www.codefactor.io/repository/github/tekofx/furbot/badge" alt="CodeFactor" /></a></div>

<p align="center">Bot para el servidor de Villafurrense</p>

# Ejecución en docker-compose :

- Descargar el archivo docker-compose
- En la misma carpeta que el docker compose crear un archivo .env y dentro colocar los siguientes datos:

  ```
  DISCORD_TOKEN=
  LOCAL_GUILD=

  REDDIT_CLIENT_ID=
  REDDIT_CLIENT_SECRET=
  REDDIT_USER_AGENT=

  TWITTER_CONSUMER_KEY=
  TWITTER_CONSUMER_SECRET=
  TWITTER_ACCESS_TOKEN=
  TWITTER_ACCESS_TOKEN_SECRET=

  MASTODON_TOKEN=
  MASTODON_APP_INSTANCE=
  ```

- Ejecutar el bot con `docker-compose up -d`

## Demo

![Demo](assets/demo.gif)
