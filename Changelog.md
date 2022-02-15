# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v3.9] - 2022-2-14
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
