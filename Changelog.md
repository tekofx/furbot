# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v4.3.11] - 2022-6-22
### Arreglado 
- Error en la versión de la libreria que hacia que no funcionase el bot

## [v4.3.10] - 2022-6-22
### Arreglado
- Error que hacia que solo se mandaran memes de 2 subreddits

### Añadido
- Ahora los memes se muestran con info sobre el subreddit, su enlace y el titulo de su post en Reddit


## v4.3.9 - 2022-5-27
### Cambios
- Modificado github action para usar tag de release

## v4.3.8 - 2022-5-27
### Cambios
- Cambios en github actions


## v4.3.7 - 2022-5-27

### Cambiado
- No se enviarán memes de video porque se envían sin audio
### Arreglado
- Error que no establecia el estado al iniciar el bot


## v4.3.6 - 2022-5-10
### Arreglado
- Hora de activacion de task meme

### Modificado
- Comprobacion de nueva version al iniciar bot


## v4.3.5 - 2022-5-10
### Añadido
- Subreddits LMDShow, MemesESP y orslokx en memes
- Los memes pueden ser ahora videos

### Eliminado
- Comando count_memes
- Cog ReactionRoles
- Subreddit furry_irl en memes

## v4.3.4 - 2022-3-28
### Añadido 
- Nuevo canal numbers: Para jugar a contar numeros
- Extensión numbers: Permite jugar a contar numeros

## v4.3.3 - 2022-3-14
### Añadido 
- Comando pais: Obtiene info de un país

### Modificado
- Comando bandera: Modificada tolerancia del nombre del pais


## v4.3.2 - 2022-3-11

### Añadido
- Comando bandera: Adivina a que país pertenece la bandera
- Comando trivial: Compite con otra persona a ver quien acierta mas preguntas de trivia

### Mejorado
- Trivial: Textos de preguntas y respuestas


## v4.3.1 - 2022-03-04 
### Mejorado
- Wordle: Ajustada la imagen para que se vea mejor

### Corregido
- Wordle: Error que sumaba puntos si una persona repetia letras parecidas


## v4.3.0 - 2022-03-04 
### Añadido
- Wordle: Sistema de puntos y ranking
- Wordle: Imagen con la palabra introducida

### Mejorado
- Memes: Cambios del código para que los memes se envíen más rápido

## v4.2.3 - 2022-03-04 
### Añadido
- Wordle: Ahora la información se muestra en un embed
- Wordle: Campo "letras acertadas"

## v4.2.2 - 2022-03-02 
### Añadido
- Comando pregunta: envia un trivial

## v4.2.1 - 2022-03-01 
### Cambiado
- Wordle: Los mensajes con intentos fallidos de palabras se eliminarán

### Añadido
- Wordle: Ahora se muestra la palabra parcial segun se vayan acertando las letras

## v4.2.0 - 2022-03-01 
### Eliminado
- Comando addcumple
- Recordatorios de cumpleaños

### Añadido 
- Recordatorio de aniversario de union al servidor
- Wordle: Cada vez que se use `fur guess` mostrará las letras que ya han sido descartadas


## [v4.1.1] - 2022-02-29
### Cambiado
- Ahora en wordle se generará una nueva palabra tras un tiempo aleatorio cada vez que se adivine una palabra


## [v4.1.0] - 2022-02-28
### Cambiado
- Ahora en wordle cada usuario tendrá 1 intento de adivinar la palabra cada hora en punto


## [v4.0.1] - 2022-02-26
### Añadido
- Task que dice la palabra solucion a las 12
  
### Arreglado
- Error con wordle que no creaba la palabra a adivinar

### Modificado
- Eliminadas palabras poco conocidas de la lista de palabras de wordle

## [v4.0] - 2022-02-25
### Añadido 
- Mensajes cuando un usuario se va del servidor
- Task que publica juegos nuevos
- Opcion para solo configurar 1 canal con el comando setup
- Cog wordle: para jugar al wordle entre todos los miembros del server. Cada miembro tiene 1 oportunidad para proponer una palabra
  
### Añadido
- Comando wordle

### Eliminado
- Comando cojones
- Comando tecute

### Cambiado
- Modificada task remove_records_from_previous_day para que no borre records de github

## [v3.9.1] - 2022-2-18
### Arreglado 
- Error en comando bird

## [v3.9] - 2022-2-15
### Añadido 
- Nuevo canal noticias bot
- Opcion para que se envien varias fotos a la vez de los comandos de `animal`
- Task que notifica nuevas versiones del bot

### Arreglado
- Ahora se configura la base de datos antes de cargar las cogs

## [v3.8] - 2022-2-14
### Añadido
- Task discord status
- Eliminacion de mensajes a partir de un mensaje. Responde a un mensaje para eliminar los mensajes anteriores a ese
- Comando cat

### Solucionado
- Error en task meme que hacia que a veces no publicase un meme

### Eliminado
- Comando carnet


## [3.7] - 2022-1-24
### Añadido
- Comando reactionroles
- Cog ReactionRoles
- Comando setup
### Cambiado
- Añadida opcion para mencionar en comando undertale
- Cambiado praw por asyncpraw
- Ahora no se pasan los ids de los canales en el .env, se utiliza el comando setup para configurarlos

### Mejorado 
- Mensajes de error

## [3.5] - 2022-1-10
### Cambiado
- Toda la información de los txts ahora se almacenan en la base de datos
### Mejorado
- Mensajes de ayuda de comandos
- Mensaje de ayuda cuando se usa el nombre de un comando como el nombre de un sticker

### Eliminado
- Comando upuser
- Task para actualizar la base de datos de usuarios
- Comando dankmeme
- Archivos .txt

## [3.3] - 2022-1-10
### Añadido
- Imagen de docker en ghcr

## [3.2] - 2022-1-7

### Arreglado

- Error en clear que borraba un mensaje menos de los que debería
- Error al añadir memes

### Cambiado

- Nombre de arctic_fox a arctic
- Cambios en on_member_join
- Eliminado valor times_joined de la tabla usuarios de sqlite
- Nombre que utilizar al añadir a la base de datos de usuarios

### Eliminado

- Eliminadas funciones yaml no necesarias

## [3.1] - 2021-12-25

### Añadido

- Comando huracan

### Corregido

- Error que repetia las imagenes de animals

## [3.0] - 2021-12-22

Se ha cambiado la librería hikari por nextcord

### Corregido

- Error al añadir cumpleaños
- Error en comando carnet que hacia que no se creara
- Script run_in_docker

### Añadido

- Comando votacion
- Comando sorteo
- Comando resultados
- Comando stats
- Comando addspecie
- Comando arctic
- Comando clear
- Comando skeletor
- Comando bird
- Comando pigeon
- Script para construir y ejecutar en docker
- Furry_irl en task memes
- Ejecución en modo pruebas o modo normal

### Cambiado

- Actualizados comandos fox y wolf
- Añadida eliminacion de contenedor anterior a run_in_docker

### Eliminado

- Comando sus

## [2.5] - 2021-9-29

### Añadido

- Tests para functions
- Cambio de txts por YAML
- Comando sus

### Mejoras

- Comando dankmeme: Mayor eficiencia
- Animal: Ahora usa la funcion de dankmemes

### Cambios

- Libreria discordpy por hikari y hikari-lightbulb

## [2.1] - 2021-9-11

### Arreglado

- Añadido Dockerfile

## [2.0] - 2021-9-11

### Añadido

- Comando radiopatio
- Comando countmemes
- Respuesta muuu cuando alguien dice vaca o vacas
- Creacion de archivos/carpetas necesarias si no existen al ejecutar el bot

### Cambiado

- Ejecución del bot en un contenedor de docker
- Movidas variables ranks, species, jojos, colors y color_codes a txts

### Arreglado

- Tratamiento de errores para nombres de memes y stickers
- Funcion para obtener de reddit en dankmemes
- Error en carnet que no cogia un usuario como argumento

### Eliminado

- Comandos no utilizados
  - trauma
  - cringe
  - burn
  - smash
  - tehc
