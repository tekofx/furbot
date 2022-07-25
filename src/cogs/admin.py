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

log = logger.getLogger(__name__)
PREDEFINED_CHANNELS = [
    {
        "type": "general",
        "description": "Canal para enviar mensajes generales",
    },
    {
        "type": "audit",
        "description": "Canal para que los administradores vean mensajes del estado y las acciones que realizo.",
    },
    {
        "type": "lobby",
        "description": "Canal para mandar mensajes de bienvenida",
    },
    {
        "type": "noticias",
        "description": "Canal para publicar noticias de nuevas versiones",
    },
    {
        "type": "games",
        "description": "Para mandar juegos que estén gratis",
    },
    {"type": "wordle", "description": "Canal para jugar a wordle"},
    {"type": "numbers", "description": "Canal jugar a contar numeros"},
    {
        "type": "ordure",
        "description": "Canal para enviar cosas bizarras",
    },
]

CHANNEL_POLICIES = [
    {
        "channel_policy": "imagenes",
        "description": "Canal para solo enviar imágenes. Se borrarán todos los mensajes que no sean imágenes.",
    },
    {
        "channel_policy": "links",
        "description": "Canal para solo enlaces. Se borrarán todos los mensajes que no sean enlaces.",
    },
    {
        "channel_policy": "arte",
        "description": "Canal para subir arte. Pueden ser videos/imagenes/audios",
    },
]

emojis = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪", "🟫", "⬜"]


class admin(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def votacion(
        self, ctx: commands.Context, titulo: str, descripcion: str, *opciones
    ):
        """Crea una votacion

        Args:
            titulo (str): de la votacion
            descripcion (str): texto descriptivo sobre lo que se va a votar
            opciones (str): opciones de la votacion. Debe escribirse cada votacion entre comillas.

        Ej:
            fur votacion "Votacion seria" "Votad alguna opcion" "Enviar un meme" "Enviar un sticker"
        """
        await ctx.message.delete(delay=1)
        embed = nextcord.Embed(title=titulo, description=descripcion)
        for opcion, emoji in zip(opciones, emojis):
            embed.add_field(name=opcion, value=emoji, inline=True)

        msg = await ctx.send(embed=embed)
        for emoji, op in zip(emojis, opciones):
            try:
                await msg.add_reaction(emoji)
            except Exception as error:
                log.error(error)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def channels(self, ctx: commands.Context):
        channels = get_channels(ctx.guild)
        channels = list(channels)

        output = "Canal: tipo | politica\n"
        for channel in channels:
            x = await self.bot.fetch_channel(channel[0])
            channel_type = channel[1]
            channel_policy = channel[2]
            output += "- {}: {} | {}\n".format(x.mention, channel_type, channel_policy)
        await ctx.send(output)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def tipos(self, ctx: commands.Context):
        """[Admin] Muestra los tipos de canales predefinidos"""
        output = ""
        for x in PREDEFINED_CHANNELS:
            output += "{} - {}\n".format(x["type"], x["description"])
        await ctx.send(output)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def policies(self, ctx: commands.Context):
        """[Admin] Muestra las politicas existentes"""
        output = ""
        for x in CHANNEL_POLICIES:
            output += "{} - {}\n".format(x["channel_policy"], x["description"])
        await ctx.send(output)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def rmchannelpolicy(self, ctx: commands.Context, canal: nextcord.TextChannel):
        """[Admin] Elimina politica de un canal"""
        channel = get_channel(ctx.guild, canal.id)

        if channel[1] is None:  # If has no type
            remove_channel(ctx.guild, canal.id)
        else:
            set_channel_policy(ctx.guild, canal.id, "all")

        await ctx.send(
            f"Eliminada la politica de {canal.mention}. Ahora se puede enviar todo tipo de mensajes."
        )

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setchannelpolicy(
        self, ctx: commands.Context, canal: nextcord.TextChannel, *politica: str
    ):
        """[Admin] Establece una politica para un canal.
        Las políticas sirven para que un canal solo se pueda enviar un tipo determinado de mensaje.

        Por ejemplo, si se establece una política imgs, solo se podrá enviar imágenes.

        Args:
            canal (nextcord.TextChannel): canal que configurar
            politica (str): politica del canal
        """
        for p in politica:

            if not p in self.get_channel_of_type_policies():
                await ctx.send(
                    "Canal no valido, la politica debe ser una de las siguientes: `{}`".format(
                        ", ".join(self.get_channel_of_type_policies())
                    )
                )
                return
        politica = " ".join(politica)
        if not exists_channel(ctx.guild, canal.id):
            create_channel(ctx.guild, canal.id, politica, canal.name)
        else:
            set_channel_policy(ctx.guild, canal.id, politica)
        await ctx.send("Canal {} configurado con politica {}".format(canal, politica))
        return

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

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def addpost(
        self,
        ctx: commands.Context,
        canal: nextcord.TextChannel,
        visibilidad: str,
        intervalo: int,
        *cuenta: str,
    ):
        """[Admin] Permite añadir una cuenta de twitter/subreddit a un canal.
        De esta forma cada hora se publicará el último post de la cuenta en el canal. Si se añaden varias
        cuentas a la vez, se utilizará una cuenta aleatoria de las añadidas.

        Args:
            canal: canal al que enviar
            visibilidad: Si/No. Si se quiere que se cojan los posts NSFW o no
            intervalo: Minutos entre un post y otro
            cuenta: cuenta/cuentas de twitter/subreddit. En caso de varias cuentas separadas por espacios
        """

        if visibilidad == "nsfw" and not canal.nsfw:
            await ctx.send(
                "El canal no es NSFW, utiliza otro canal o cambia los permisos."
            )
            return

        if not canal.permissions_for(ctx.guild.me).send_messages:
            await ctx.send("No tengo permisos para enviar mensajes en este canal.")
            return

        if intervalo < 5:
            await ctx.send("El intervalo debe ser mayor que 5 minutos.")
            return

        account = []

        for arg in cuenta:

            if "twitter@" not in arg and "reddit@" not in arg:
                await ctx.send("Se ha introducido una cuenta no válida")
                await ctx.send(
                    "La cuenta tiene que ser del formato: twitter@cuenta, reddit@cuenta"
                )
                return

            account.append(arg)

        cuenta = " ".join(account)
        create_post(ctx.guild, [canal.id, visibilidad, cuenta, intervalo])
        await ctx.send("Post creado")

        # Get tasks cog and create task
        tasks = self.bot.cogs.get("tasks")
        self.bot.loop.create_task(
            tasks.post_task(ctx.guild, [canal.id, visibilidad, cuenta, 0, intervalo])
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rmpost(self, ctx: commands.Context, post_id: int):
        """[Admin] Permite eliminar una cuenta de twitter/subreddit de un canal.

        Args:
            id: id del post a eliminar
        """

        remove_post(ctx.guild, post_id)
        await ctx.send("Post eliminado")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def posts(self, ctx: commands.Context):
        "[Admin] Muestra los posts que se han añadido"
        posts = get_posts(ctx.guild)
        if not posts:
            await ctx.send("No hay posts para este servidor")
            return

        output = ""
        for post in posts:
            channel = await self.bot.fetch_channel(post[0])
            output += "-id={}\n-canal={}\n-visibilidad={}\n-cuenta/s={} \n\n".format(
                post[3], channel.mention, post[1], post[2]
            )

        await ctx.send(output)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setchannel(
        self, ctx: commands.Context, canal: nextcord.TextChannel, tipo: str
    ):
        """[Admin] Configura un los canal predefinido del bot.

        Permite establecer canales que sirvan para una función específica. Por ejemplo el canal lobby da la bienvenida
        a los miembros nuevos

        Args:
            canal (nextcord.TextChannel): canal que configurar
            tipo (str): tipo del canal
        """
        if not tipo in self.get_channel_of_type_types():
            await ctx.send(
                "Canal no valido, el canal debe ser uno de los siguientes: `{}`".format(
                    ", ".join(self.get_channel_of_type_types())
                )
            )
            return
        if not exists_channel(ctx.guild, canal.id):
            create_channel(ctx.guild, canal.id, "all", canal.name, tipo)
        else:
            set_channel_type(ctx.guild, canal.id, tipo)

        await ctx.send("Canal {} configurado como {}".format(canal.mention, tipo))
        return

    @commands.command(name="setchannels")
    @commands.has_permissions(administrator=True)
    async def setchannels(self, ctx: commands.Context) -> None:

        """[Admin] Configurar los canales predefinidos del bot.

        Permite establecer canales que sirvan para una función específica. Por ejemplo el canal lobby da la bienvenida
        a los miembros nuevos
        """

        await ctx.send(
            "Empezando configuración. Se le pedirá establecer varios canales. Si no quiere establecer un canal, escriba `skip`"
        )
        await sleep(2)
        for x in PREDEFINED_CHANNELS:
            await self.setup_channel(ctx, x["type"], x["description"])

        await ctx.send("Configuración finalizada")

    @commands.command(name="activity")
    @commands.has_permissions(administrator=True)
    async def change_activity(self, ctx: commands.Context, activity_name: str):
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
            await ctx.send("Error: Contacte con un administrador")
            log.error("Error: {}".format(error))
            return
        else:
            await ctx.send("Cambiada actividad a " + activity_name)
            log.info("Changed activity to " + activity_name)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context, num: int):
        """[Admin] Elimina mensajes de un canal

        Uso:
            fur clear <num_mensajes>
        """

        messages_to_delete = []
        # If command is a reply to a message
        if ctx.message.reference is None:
            async for message in ctx.channel.history(limit=num + 1):
                messages_to_delete.append(message)

        else:
            async for message in ctx.channel.history(
                limit=num, before=ctx.message.reference.cached_message
            ):
                messages_to_delete.append(message)
        await ctx.channel.delete_messages(messages_to_delete)
        message = await ctx.send("Eliminados {} mensajes".format(num))
        await sleep(5)
        await message.delete()
        await ctx.message.delete()

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
        self, ctx: commands.Context, channel_type: str, channel_description: str
    ):
        def check(m: nextcord.Message) -> bool:
            return m.author == ctx.author and m.channel == ctx.channel

        # General channel
        await ctx.send(
            "Seleccione el canal {}. {}".format(channel_type, channel_description)
        )
        msg = await self.bot.wait_for("message", check=check, timeout=60)
        if msg.content.lower() != "skip":
            try:
                channel = await self.fetch_channel_from_message_content(msg)
            except nextcord.errors.Forbidden:
                await ctx.send("No tengo permisos para acceder a este canal.")
                return

            if not channel.permissions_for(ctx.guild.me).send_messages:
                await ctx.send("No tengo permisos para enviar mensajes en este canal.")
                log.error(
                    "Don't have permissions to send messages in channel {}".format(
                        channel.id
                    ),
                    extra={"guild": ctx.guild.id},
                )
                return
            if not exists_channel(ctx.guild, channel.id):
                create_channel(ctx.guild, channel.id, "all", channel.name, channel_type)
            else:
                set_channel_type(ctx.guild, channel.id, channel_type)

            await ctx.send(
                "Canal {} añadido como {}".format(channel.mention, channel_type)
            )

    def get_channel_of_type_types(self) -> List[str]:
        """Gets the channel_types from CHANNEL

        Returns:
            List[str]: contains the channel_types
        """
        output = []
        for x in PREDEFINED_CHANNELS:
            output.append(x["type"])

        return output

    def get_channel_of_type_policies(self) -> List[str]:
        """Gets the channel_policies from CHANNEL

        Returns:
            List[str]: contains the channel_policies
        """
        output = []
        for x in CHANNEL_POLICIES:
            output.append(x["channel_policy"])

        return output


def setup(bot: commands.Bot):
    bot.add_cog(admin(bot))
