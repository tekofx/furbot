# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2021-12-25

### Arreglado

- Error en clear que borraba un mensaje menos de los que debería
- Error al añadir memes

### Cambiado

- Nombre de arctic_fox a arctic
- Cambios en on_member_join
- Eliminado valor times_joined de la tabla usuarios de sqlite
- Nombre que utilizar al añadir a la base de datos de usuarios

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
