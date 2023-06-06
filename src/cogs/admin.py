from typing import List
from nextcord.ext import commands
import nextcord
from core.database import (
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
from ui.Modal import Modal
from asyncio import sleep
from core.bot import Bot
from core import logger
from nextcord.ext import application_checks
from nextcord import Interaction, SlashOption


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
        "memes": "Canal para enviar memes del server",
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
    ):
        """Crea una votacion

        """
        await interaction.response.send_modal(Modal())

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
    @canales.subcommand(
        name="rmpolicy",
    )
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
        canal: nextcord.TextChannel | nextcord.ForumChannel,
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
        servicio: str = SlashOption(
            name="servicios",
            required=True,
            choices={"Twitter": "twitter", "Reddit": "reddit","Mastodon":"mastodon"},
        ),
        cuenta: str = SlashOption(name="cuenta", required=True),
        visibilidad: str = SlashOption(
            name="visibilidad", required=True, choices={"SFW": "sfw", "NSFW": "nsfw"}
        ),
        intervalo: int=5,
    ):
        """[Admin] Permite añadir una cuenta de twitter/subreddit a un canal.
        De esta forma cada hora se publicará el último post de la cuenta en el canal. Si se añaden varias
        cuentas a la vez, se utilizará una cuenta aleatoria de las añadidas.

        Args:
            canal: canal al que enviar
            visibilidad: Si/No. Si se quiere que se cojan los posts NSFW o no
            intervalo: Minutos entre un post y otro. Debe ser mayor a los 5 mins
            cuenta: Cuenta de twitter, subreddit de Reddit o usuario@instancia de Mastodon
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

        if servicio == "reddit":
            exists = await self.bot.reddit.exists_subreddit(cuenta)
            if not exists:
                await interaction.send(
                    f"El subreddit {cuenta} no existe, comprueba el subreddit y vuelve a intentarlo"
                )
                return

        if servicio == "twitter":
            var = self.bot.twitter.exists_account(cuenta)

            if not var:
                await interaction.send(
                    f"La cuenta {cuenta} no existe, comprueba la cuenta y vuelve a intentarlo"
                )
                return
            
        if servicio =="mastodon":
            instance=cuenta.split("@")[1]
            usuario=cuenta.split("@")[0]
            var=self.bot.mastodon.exists_account(usuario,instance)
            if not var:
                await interaction.send(
                    f"La cuenta {cuenta} no existe, comprueba la cuenta y vuelve a intentarlo"
                )
                return

        create_post(
            interaction.guild, canal.id, visibilidad, servicio, cuenta, intervalo
        )
        await interaction.send("Post creado")

        # Get tasks cog and create task
        tasks = self.bot.cogs.get("tasks")

        task = self.bot.loop.create_task(
            tasks.post_task(
                interaction.guild, canal.id, visibilidad, servicio, cuenta, intervalo
            )
        )

        # Add task to tasks dict
        task_id = int(str(interaction.guild.id) + str(canal.id))
        self.bot.tasks[task_id] = task

    @application_checks.has_permissions(administrator=True)
    @post.subcommand(name="rm")
    async def post_rm(self, interaction: Interaction, post_id: int):
        """[Admin] Permite eliminar una cuenta de twitter/subreddit de un canal.

        Args:
            post_id: id del post a eliminar
        """
        task_id = int(str(interaction.guild.id) + str(post_id))

        # Remove from db
        remove_post(interaction.guild, post_id)

        # Cancel the task
        self.bot.tasks[task_id].cancel()

        # Remove from tasks dict
        del self.bot.tasks[task_id]

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
            channel_id = post[0]
            visibility = post[1]
            service = post[2]
            account = post[3]
            post_id = post[4]
            interval = post[5]
            channel = await self.bot.fetch_channel(channel_id)
            output += f"-id={post_id}\n-canal={channel.mention}\n-visibilidad={visibility}\n-servicio={service}\n-cuenta={account} \n-intevalo={interval}m\n\n"

        await interaction.send(output)

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
                extra={"guild": message.guild.name},
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
                    extra={"guild": interaction.guild.name},
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
