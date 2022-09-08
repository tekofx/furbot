from typing import List
from nextcord.ext import commands
import nextcord
from utils.database import (
    create_channel,
    create_post,
    exists_channel,
    get_channel,
    get_channels,
    get_posts,
    remove_channel,
    remove_post,
    set_channel_policy,
    set_channel_type,
)

from asyncio import sleep
from utils.data import config_yaml
from utils.bot import Bot
import yaml
from utils import logger
from nextcord.ext import application_checks
from nextcord import Interaction, SlashOption
import os


log = logger.getLogger(__name__)
PREDEFINED_CHANNELS = dict(
    {
        "general": "Canal para enviar mensajes generales",
        "audit": "Canal para que los administradores vean mensajes del estado y las acciones que realizo.",
        "lobby": "Canal para mandar mensajes de bienvenida",
        "noticias": "Canal para publicar noticias de nuevas versiones",
        "games": "Para mandar juegos que estén gratis",
        "wordle": "Canal para jugar a wordle",
        "numbers": "Canal jugar a contar numeros",
        "ordure": "Canal para enviar cosas bizarras",
    },
)


CHANNEL_POLICIES_OPTIONS = {
    "Solo imágenes": "imagenes",
    "Solo enlaces": "links",
    "Videos, imágenes y audios": "arte",
}

CHANNEL_POLICIES = {
    "imagenes": "Canal para solo enviar imágenes. Se borrarán todos los mensajes que no sean imágenes.",
    "links": "Canal para solo enlaces. Se borrarán todos los mensajes que no sean enlaces.",
    "arte": "Canal para subir arte. Pueden ser videos/imagenes/audios",
}


emojis = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪", "🟫", "⬜"]


class admin(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(name="votacion")
    @application_checks.has_permissions(administrator=True)
    async def votacion(
        self,
        interaction: Interaction,
        titulo: str,
        descripcion: str,
        opciones: str,
    ):
        """Crea una votacion

        Args:
            titulo (str): de la votacion
            descripcion (str): texto descriptivo sobre lo que se va a votar
            opciones (str): opciones de la votacion. Separado por comas.

        Ej:
            fur votacion "Votacion seria" "Votad alguna opcion" "Enviar un meme" "Enviar un sticker"
        """
        msg = await interaction.send("Votacion")
        await msg.delete()
        embed = nextcord.Embed(title=titulo, description=descripcion)
        opciones = opciones.split(",")
        for opcion, emoji in zip(opciones, emojis):
            embed.add_field(name=opcion, value=emoji, inline=True)

        msg = await interaction.channel.send(embed=embed)
        for emoji, op in zip(emojis, opciones):
            try:
                await msg.add_reaction(emoji)
            except Exception as error:
                log.error(error)

    @nextcord.slash_command(name="canales")
    @application_checks.has_permissions(administrator=True)
    async def canales(self, interaction: Interaction):
        pass

    @canales.subcommand(name="mostrar")
    @application_checks.has_permissions(administrator=True)
    async def show_channels(self, interaction: Interaction):
        channels = get_channels(interaction.guild)
        channels = list(channels)

        output = "Canal: tipo | politica\n"
        for channel in channels:
            x = await self.bot.fetch_channel(channel[0])
            channel_type = channel[1]
            channel_policy = channel[2]
            output += "- {}: {} | {}\n".format(x.mention, channel_type, channel_policy)
        await interaction.send(output)
        pass

    @application_checks.has_permissions(administrator=True)
    @canales.subcommand(name="rmchannelpolicy")
    async def canales_rmchannelpolicy(
        self, interaction: Interaction, canal: nextcord.TextChannel
    ):
        """[Admin] Elimina politica de un canal"""
        channel = get_channel(interaction.guild, canal.id)

        if channel[1] is None:  # If has no type
            remove_channel(interaction.guild, canal.id)
        else:
            set_channel_policy(interaction.guild, canal.id, "all")

        await interaction.send(
            f"Eliminada la politica de {canal.mention}. Ahora se puede enviar todo tipo de mensajes."
        )

    @application_checks.has_permissions(administrator=True)
    @canales.subcommand(name="list")
    async def channels_list(self, interaction: Interaction):
        pass

    @channels_list.subcommand(name="tipos")
    @application_checks.has_permissions(administrator=True)
    async def channel_types(self, interaction: Interaction):
        output = ""
        for x, y in PREDEFINED_CHANNELS.items():
            output += "{} - {}\n".format(x, y)
        await interaction.send(output)

    @application_checks.has_permissions(administrator=True)
    @channels_list.subcommand(name="politicas")
    async def channle_policies(self, interaction: Interaction):
        output = ""
        for x, y in CHANNEL_POLICIES.items():
            output += "{} - {}\n".format(x, y)
        await interaction.send(output)

    @application_checks.has_permissions(administrator=True)
    @canales.subcommand(name="set")
    async def channel_set(self, interaction: Interaction):
        pass

    @application_checks.has_permissions(administrator=True)
    @channel_set.subcommand(name="policy")
    async def channel_set_policy(
        self,
        interaction: Interaction,
        canal: nextcord.TextChannel,
        politica: str = SlashOption(name="politica", choices=CHANNEL_POLICIES_OPTIONS),
    ):
        if not politica in self.get_channel_of_type_policies():
            await interaction.send(
                "Canal no valido, la politica debe ser una de las siguientes: `{}`".format(
                    ", ".join(self.get_channel_of_type_policies())
                )
            )
            return
        if not exists_channel(interaction.guild, canal.id):
            create_channel(interaction.guild, canal.id, politica, canal.name)
        else:
            set_channel_policy(interaction.guild, canal.id, politica)
        await interaction.send(
            "Canal {} configurado con politica {}".format(canal, politica)
        )
        return

    @application_checks.has_permissions(administrator=True)
    @channel_set.subcommand(name="type")
    async def channel_set_type(
        self,
        interaction: Interaction,
        canal: nextcord.TextChannel,
        tipo: str = SlashOption(name="tipo", choices=PREDEFINED_CHANNELS.keys()),
    ):
        """[Admin] Configura un canal predefinido del bot.

        Permite establecer canales que sirvan para una función específica. Por ejemplo el canal lobby da la bienvenida
        a los miembros nuevos

        Args:
            canal (nextcord.TextChannel): canal que configurar
            tipo (str): tipo del canal
        """
        if not tipo in self.get_channel_of_type_types():
            await interaction.send(
                "Canal no valido, el canal debe ser uno de los siguientes: `{}`".format(
                    ", ".join(self.get_channel_of_type_types())
                )
            )
            return
        if not exists_channel(interaction.guild, canal.id):
            create_channel(interaction.guild, canal.id, "all", canal.name, tipo)
        else:
            set_channel_type(interaction.guild, canal.id, tipo)

        await interaction.send(
            "Canal {} configurado como {}".format(canal.mention, tipo)
        )
        return

    @application_checks.has_permissions(administrator=True)
    @channel_set.subcommand(name="all")
    async def channel_set_all(self, interaction: Interaction) -> None:

        """[Admin] Configurar los canales predefinidos del bot.

        Permite establecer canales que sirvan para una función específica. Por ejemplo el canal lobby da la bienvenida
        a los miembros nuevos
        """

        await interaction.send(
            "Empezando configuración. Se le pedirá establecer varios canales. Si no quiere establecer un canal, escriba `skip`"
        )
        await sleep(2)
        for x, y in PREDEFINED_CHANNELS.items():
            await self.setup_channel(interaction, x, y)

        await interaction.channel.send("Configuración finalizada")

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return
        guild = message.guild
        channel = get_channel(guild, message.channel.id)
        if not channel:
            return

        channel_policy = channel[2]
        if channel_policy == "all":
            return

        if channel_policy == "links" and "https://" in message.content:
            return

        if channel_policy == "imagenes" and message.attachments:
            if "image" in message.attachments[0].content_type:
                return

        if channel_policy == "arte":
            if message.attachments and (
                "image" in message.attachments[0].content_type
                or "video" in message.attachments[0].content_type
            ):
                await message.add_reaction("⭐")
                """ thread = "Publicación de " + message.author.name
                await message.create_thread(name=thread) """
                return
            if "https://" in message.content:
                await message.add_reaction("⭐")
                """thread = "Publicación de " + message.author.name
                await message.create_thread(name=thread)"""
                return

        await message.delete()
        msg = await message.channel.send(
            f"En este canal solo se pueden enviar {channel_policy}. Puedes abrir un hilo si quieres escribir texto sobre algún mensaje."
        )
        await msg.delete(delay=5)

    @nextcord.slash_command(name="post")
    @application_checks.has_permissions(administrator=True)
    async def post(self, interaction: Interaction):
        pass

    @application_checks.has_permissions(administrator=True)
    @post.subcommand(name="add")
    async def post_add(
        self,
        interaction: Interaction,
        canal: nextcord.TextChannel,
        intervalo: int,
        cuentas: str,
        visibilidad: str = SlashOption(
            name="visibilidad", choices={"SFW": "sfw", "NSFW": "nsfw"}
        ),
    ):
        """[Admin] Permite añadir una cuenta de twitter/subreddit a un canal.
        De esta forma cada hora se publicará el último post de la cuenta en el canal. Si se añaden varias
        cuentas a la vez, se utilizará una cuenta aleatoria de las añadidas.

        Args:
            canal: canal al que enviar
            visibilidad: Si/No. Si se quiere que se cojan los posts NSFW o no
            intervalo: Minutos entre un post y otro
            cuentas: cuenta/cuentas de twitter/subreddit. En caso de varias cuentas separadas por espacios
        """

        if visibilidad == "nsfw" and not canal.nsfw:
            await interaction.send(
                "El canal no es NSFW, utiliza otro canal o cambia los permisos."
            )
            return

        if not canal.permissions_for(interaction.guild.me).send_messages:
            await interaction.send(
                "No tengo permisos para enviar mensajes en este canal."
            )
            return

        if intervalo < 5:
            await interaction.send("El intervalo debe ser mayor que 5 minutos.")
            return

        account = []

        cuentas = cuentas.split(" ")

        for arg in cuentas:

            if "twitter@" not in arg and "reddit@" not in arg:
                await interaction.send("Se ha introducido una cuenta no válida")
                await interaction.send(
                    "La cuenta tiene que ser del formato: twitter@cuenta, reddit@cuenta"
                )
                return

            account.append(arg)

        cuenta = " ".join(account)
        create_post(interaction.guild, [canal.id, visibilidad, cuenta, intervalo])
        await interaction.send("Post creado")

        # Get tasks cog and create task
        tasks = self.bot.cogs.get("tasks")
        self.bot.loop.create_task(
            tasks.post_task(
                interaction.guild, [canal.id, visibilidad, cuenta, 0, intervalo]
            )
        )

    @application_checks.has_permissions(administrator=True)
    @post.subcommand(name="rm")
    async def post_rm(self, interaction: Interaction, post_id: int):
        """[Admin] Permite eliminar una cuenta de twitter/subreddit de un canal.

        Args:
            id: id del post a eliminar
        """

        remove_post(interaction.guild, post_id)
        await interaction.send("Post eliminado")

    @application_checks.has_permissions(administrator=True)
    @post.subcommand(name="list")
    async def post_list(self, interaction: Interaction):
        "[Admin] Muestra los posts que se han añadido"
        posts = get_posts(interaction.guild)
        if not posts:
            await interaction.send("No hay posts para este servidor")
            return

        output = ""
        for post in posts:
            channel = await self.bot.fetch_channel(post[0])
            output += "-id={}\n-canal={}\n-visibilidad={}\n-cuenta/s={} \n\n".format(
                post[3], channel.mention, post[1], post[2]
            )

        await interaction.send(output)

    @nextcord.slash_command(name="activity")
    @application_checks.has_permissions(administrator=True)
    async def change_activity(self, interaction: Interaction, activity_name: str):
        """[Admin] Cambiar actividad del bot

        Uso:
            fur activity <texto>
        """
        activity = nextcord.Game(activity_name)

        # Change activity in config.yaml
        with open(config_yaml, "r") as f:
            content = yaml.safe_load(f)
            content["activity"] = activity_name
        with open(config_yaml, "w") as f:
            yaml.dump(content, f, allow_unicode=True)

        # Change activity in bot
        try:
            await self.bot.change_presence(
                status=nextcord.Status.online, activity=activity
            )

        except Exception as error:
            await interaction.send("Error: Contacte con un administrador")
            log.error("Error: {}".format(error))
            return
        else:
            await interaction.send("Cambiada actividad a " + activity_name)
            log.info("Changed activity to " + activity_name)

    @nextcord.slash_command(name="clear")
    @application_checks.has_permissions(administrator=True)
    async def clear(self, interaction: Interaction, num: int):
        """[Admin] Elimina mensajes de un canal

        Uso:
            fur clear <num_mensajes>
        """

        messages_to_delete = []
        # If command is a reply to a message
        async for message in interaction.channel.history(limit=num + 1):
            messages_to_delete.append(message)

        await interaction.channel.delete_messages(messages_to_delete)
        message = await interaction.send("Eliminados {} mensajes".format(num))
        await sleep(5)
        await message.delete()

    async def fetch_channel_from_message_content(
        self, message: nextcord.Message
    ) -> nextcord.TextChannel:
        """Gets a channel from a message content

        Args:
            message (nextcord.Message): message to get the channel from

        Returns:
            nextcord.TextChannel: channel
        """

        channel_id = message.content.replace("<#", "").replace(">", "")
        try:
            channel = await self.bot.fetch_channel(channel_id)
        except nextcord.errors.Forbidden as error:
            log.error(
                "Don't have permissions to fetch channel {}: {}".format(
                    channel_id, error
                ),
                extra={"guild": message.guild.id},
            )
            raise error
        return channel

    async def setup_channel(
        self, interaction: Interaction, channel_type: str, channel_description: str
    ):
        def check(m: nextcord.Message) -> bool:
            return m.author == interaction.user and m.channel == interaction.channel

        # General channel
        await interaction.channel.send(
            "Seleccione el canal {}. {}".format(channel_type, channel_description)
        )
        msg = await self.bot.wait_for("message", check=check, timeout=60)
        if msg.content.lower() != "skip":
            try:
                channel = await self.fetch_channel_from_message_content(msg)
            except nextcord.errors.Forbidden:
                await interaction.channel.send(
                    "No tengo permisos para acceder a este canal."
                )
                return

            if not channel.permissions_for(interaction.guild.me).send_messages:
                await interaction.channel.send(
                    "No tengo permisos para enviar mensajes en este canal."
                )
                log.error(
                    "Don't have permissions to send messages in channel {}".format(
                        channel.id
                    ),
                    extra={"guild": interaction.guild.id},
                )
                return
            if not exists_channel(interaction.guild, channel.id):
                create_channel(
                    interaction.guild, channel.id, "all", channel.name, channel_type
                )
            else:
                set_channel_type(interaction.guild, channel.id, channel_type)

            await interaction.channel.send(
                "Canal {} añadido como {}".format(channel.mention, channel_type)
            )

    def get_channel_of_type_types(self) -> List[str]:
        """Gets the channel_types from CHANNEL

        Returns:
            List[str]: contains the channel_types
        """
        output = []
        for x in PREDEFINED_CHANNELS.keys():
            output.append(x)

        return output

    def get_channel_of_type_policies(self) -> List[str]:
        """Gets the channel_policies from CHANNEL

        Returns:
            List[str]: contains the channel_policies
        """
        output = []
        for x in CHANNEL_POLICIES.keys():
            output.append(x)

        return output


def setup(bot: commands.Bot):
    bot.add_cog(admin(bot))
