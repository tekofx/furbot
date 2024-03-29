# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v6.3.1] - 2023-07-24
- Añadido pool a e631/e926
- Arreglo en comando tiempo
- Cambiado e621/e926 a embed

## [v6.3.0] - 2023-07-19
- Añadido comando tiempo

## [v6.2.0] - 2023-07-18
- Aumentado tamaño de las tags que se pueden añadir a un post de e621/e926
- Modificados comandos de post

## [v6.1.8] - 2023-07-09
- Arreglado error al obtener el avatar de un usuario en los comandos meme
- Downgrade de la version de pillow

## [v6.1.7] - 2023-07-09
- Arreglado error comando avatar

## [v6.1.5] - 2023-07-06
- Modificado comando votacion

## [v6.1.4] - 2023-07-06
- Arreglado error en comando avatar
- Añadidas opciones titulo y descripcion en comando votacion

## [v6.1.3] - 2023-07-05
Añadido comando avatar

## [v6.1.2] - 2023-07-05
Añadidas tags al enviar post de e621/e926

## [v6.1.1] - 2023-07-03
Arreglado error con tags de e621/e926

## [v6.1.0] - 2023-07-03

### Añadido
- Soporte para e621 y e926

### Eliminado
- Anuncio de caracteristicas nuevas al actualizar bot


## [v6.0.3] - 2023-06-25

Arreglado error que spammeaba cuando es el aniversario de entrada al server


## [v6.0.2] - 2023-06-13

Modificada implementacion de la base de datos y otras mejoras

### Modificado

- Los comandos de animales se han sustiuido por un unico comando /animal

## [v6.0.1] - 2023-06-12

Arreglado error en la conexión con la base de datos

## [v6.0.0] - 2023-06-12

Cambios importantes.

### Modificado

- Se ha cambiado el motor de la base de datos a uno más eficiente
- Renombrados comandos para ser más entendibles
- Modificadas descripciones para ser más entendibles

## [v5.4.0] - 2023-03-13

Debido al aumento de ataques de spam y la inutilidad de discord para detectar el spam, se ha añadido al bot la opción de detectar el spam, aislar indefinidamente al usuario y borrar los mensajes de spam.

### Añadido

- Antispam: Aisla de forma indefinida a un usuario que spamee el mismo mensaje aunque sea en varios canales y borra los mensajes de spam.

## [v5.3.2] - 2023-02-15

Correccion de errores

### Arreglado

- Actualizado Python a versión 3.10

## [v5.3.1] - 2023-02-15

Correccion de errores

### Arreglado

- Actualizada libreria de discord

## [v5.3.0] - 2023-02-15

Cambios en el funcionamiento de los memes

### Añadido

- Comando meme count: Cuenta el numero de memes que hay para un usuario o en general
- Ahora los memes se añaden por medio de un foro, en el que el bot preguntará que miembros aparecen en el meme.

### Modificado

- Cambiado comando /canales rmchannelpolicy a /canales rmpolicy

### Arreglado

- Error en /post list que no mostraba el intervalo de los posts

## [v5.2.2] - 2023-01-29

Correción de error en comando birthday get

### Arreglado

- Error al usar birthday get en un usuario sin cumpleaños

## [v5.2.1] - 2023-01-29

Correción de error

### Arreglado

- Cambiado el servidor principal con el que sincronizar los comandos. Esto producia un error al iniciar el bot.

## [v5.2.0] - 2023-01-29

Nuevas opciones de cumpleaños

### Añadido

- Comando birthday set: Añade tu cumpleaños al bot
- Comando birtday get: Obtén el cumpleaños de un usuario
- Task birthday: El bot felicitará a los usuarios que hayan añadido su cumpleaños

## [v5.1.0] - 2023-01-08

Primera versión del año!

### Añadido

- Comando femboy: Descubre que porcentaje de femboy hay en ti

## [v5.0.7] - 2022-11-18

Versión menor con mejoras y actualización de librerías

### Modificado

- Ahora al usar un comando como horny, patada, jojo, etc, se menciona al usuario.

## [v5.0.6] - 2022-10-17

Parche para arreglar problemas y errores

### Arreglado

- Error en posts con varias cuentas
- Añadido mensaje al usar fur en vez de /

### Modificado

- Cambiado mensaje de bienvenida al server para que mencione al usuario

## [v5.0.5] - 2022-10-15

Parche para arreglar un problema con los posts

### Arreglado

- Error con task que publicaba cada minuto

## [v5.0.4] - 2022-10-15

Pequeña actualizacion con mejoras de las tasks y mensajes de error

### Arreglado

- Error con posts que hacia que siempre se publicara con la misma cuenta (otra vez)

### Añadido

- Al crear un post se comprueba si la/s cuenta/s introducidas existen
- Se enviará un mensaje privado a los nuevos miembros

### Eliminado

- Comando activity

## [v5.0.3] - 2022-09-23

Versión menor que arregla un par de errores con los posts

### Añadido

- Al añadir un meme se añade una estrella de reacción

### Arreglado

- Error con posts que hacia que siempre se publicara con la misma cuenta
- Retraso que se forma poco a poco segun se van enviando posts

## [v5.0.2] - 2022-09-08

Cambios menores debido al cambio a comandos /

### Modificado

- Ahora al añadir un meme con meme add se envia el meme por el canal para que se pueda ver

### Arreglado

- Error que no dejaba enviar memes al especificar el nombre

## [v5.0.1] - 2022-09-06

Correccion de errores

### Arreglado

- Error que impide funcionar los comandos nada mas iniciar el bot

## [v5.0.0] - 2022-09-06

Ahora Furbot funciona por medio de comandos de barra diagonal, para usarlos basta con escribir / y seleccionar el comando a usar. Debido a este cambio hay comandos que han sufrido cambios

### Eliminado

- Comandos carnet, teodio, insult, animo, addinsult, addanimo
- Cog roast

### Modificado

- Debido a los cambios en la politica de bots de Discord, ahora los comandos se invocan con / y algunos comandos han cambiado de nombre
- Los comandos relacionados con stickers o memes se pueden invocar poniendo /sticker o /meme respectivamente
- Ahora las noticias tienen un apartado de descripción donde se resumen las novedades

## [v4.7.11] - 2022-07-25

### Arreglado

- Error que congelaba los posts

## [v4.7.10] - 2022-07-25

### Arreglado

- Error que congelaba los posts

## [v4.7.9] - 2022-07-25

### Añadido

- Mensajes dependiendo del dia del año. Por ejemplo del orgullo o navidad.
- Comando votacion: Permite crear una votacion

### Eliminado

- Task discord status que mostraba el estado del servidor de discord.

### Modificado

- Ahora al crear un post se puede elegir cada cuantos minutos se publique. El tiempo minimo es de 5 mins.
- Los admins no podrán saltarse las politicas de un canal
- Ahora las cuentas de los posts tienen que seguir el formato twitter@username y reddit@subreddit

## [v4.7.8] - 2022-07-08

### Añadido

- Ordure ahora publica también videos

## [v4.7.7] - 2022-07-08

### Añadido

- Ahora aparecerá que el bot está escribiendo al enviar un meme.

### Arreglado

- Administracion de politicas de canales

## [v4.7.6] - 2022-07-01

### Arreglado

- Error que coge menos posts de reddit

## [v4.7.5] - 2022-07-01

### Arreglado

- Error al obtener posts de reddit

## [v4.7.4] - 2022-07-01

### Arreglado

- Error en posts

## [v4.7.3] - 2022-07-01

### Arreglado

- Restriccion que impedia a un admin escribir por un canal con politica

### Añadido

- Mejor administración de historial para todo el contenido que se obtiene de reddit y twitter. Como se va a borrar y crear un nuevo historial se repetirá ciertos contenidos.

### Cambiado

- Ahora se usa la cuenta de twitter ArcticHourly para el comando arctic

## [v4.7.2] - 2022-07-01

### Arreglado

- Error con posts que no se publicaban a en punto

## [v4.7.1] - 2022-07-01

### Arreglado

- Error que detenia la publicación de posts
- Error al crear un post con una url de twitter con parámetros a parte del nombre de usuario

## [v4.7.0] - 2022-6-30

### Cambiado

- Eliminados comandos addcolor, addrank y addspecie
- Modificado comando posts
- Cog administration ahora se llama admin
- Cog utilities ahora se llama utils
- Subreddit del comando cat. Ahora se usa la cuenta de twitter HourlyCats.
- Cambiado texto de comando str8
- Eliminados puntos de wordle

### Añadido

- Al usar los comandos addpost y setup se comprobará si el bot tiene acceso a los canales que se especifiquen y si tiene permiso para enviar mensajes.
- Comprobacion de permisos de canal en task post
- Comando setchannelpolicy. Con este comando se puede establecer que tipo de contenido se puede enviar en un canal. Si un mensaje no tiene ese tipo de contenido se eliminará.
- Comando setchannel. Establecer un canal para que sea un canal predefinido. Por ejemplo en el canal lobby se da la bienvenida a los miembros nuevos. Los canales predefinidos que hay son lobby, general, audit, noticias, games, wordle, numbers y ordure
- Comando setchannels. Parecido a setchannel pero permite ir estableciendo los canales uno a uno.
- Comando rmchannelpolicy. Elimina la politica de un canal.
- Comando channels. Muestra los canales configurados, mostrando el tipo de canal y su politica.
- Eliminación de contenido que no cumpla las politicas de un canal

### Arreglado

- Task joined_date que felicita a los usuarios al cumplir x años en el servidor

## [v4.6.2] - 2022-6-27

### Arreglado

- Error en task post con los posts NSFW

## [v4.6.1] - 2022-6-27

### Arreglado

- Error en task post que hacia que no se ejecutase cada hora en punto

## [v4.6.0] - 2022-6-27

### Añadido

- Task post. Permite añadir cuentas de twitter/subreddits para que el bot suba a un canal establecido los posts que hagan estas cuentas.
- Commando posts [Admin]. Permite ver los posts que se han configurado.
- Comando addpost [Admin]. Permite añadir posts
- Commando rmpost [Admin]. Permite eliminar posts

### Eliminado

- Task meme. Se puede hacer lo mismo con la task post, pudiendo personalizar en que canales se suben memes y desde que cuentas.
- Respuesta cuando alguien pone a

## [v4.5] - 2022-6-27

### Cambios

- Mejorado el funcionamiento de la base de datos
- Eliminados comandos cowsay, impostor, omni, shef, undertale, mierda

### Añadido

- Comando lizard

### Arreglado

- Error en comandos de animales que repetia siempre la misma imagen

## [v4.3.13] - 2022-6-24

### Cambios

- Modificada task ordure para que publique cada post nuevo

## [v4.3.12] - 2022-6-24

### Añadido

- Task ordure bizarre

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
