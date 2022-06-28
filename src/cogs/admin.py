import logging
from typing import List
from nextcord.ext import commands
import nextcord
from utils.database import (
    create_channel,
    create_role,
    create_post,
    get_posts,
    remove_post,
)
from asyncio import sleep
from utils.data import config_yaml
from utils.bot import Bot
import yaml

log = logging.getLogger(__name__)
ROLE_EXISTS = "UNIQUE constraint failed: roles.id"
CHANNELS = [
    {"channel_type": "general", "channel_description": "enviar mensajes generales."},
    {
        "channel_type": "audit",
        "channel_description": "que los administradores vean el estado de los servidores de Discord",
    },
    {"channel_type": "lobby", "channel_description": "mandar mensajes de bienvenida"},
    {
        "channel_type": "bot_news",
        "channel_description": "mandar info sobre nuevas versiones del bot",
    },
    {"channel_type": "games", "channel_description": "mandar juegos gratuitos"},
    {"channel_type": "wordle", "channel_description": "jugar a wordle"},
    {"channel_type": "numbers", "channel_description": "jugar a contar numeros"},
    {"channel_type": "ordure", "channel_description": "Cosas bizarras"},
]


class admin(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def addpost(
        self,
        ctx: commands.Context,
        canal: nextcord.TextChannel,
        visibilidad: str,
        *cuenta: str
    ):
        """[Admin]Permite añadir una cuenta de twitter/subreddit a un canal.
        De esta forma cada hora se publicará el último post de la cuenta en el canal. Si se añaden varias
        cuentas a la vez, se utilizará una cuenta aleatoria de las añadidas.

        Args:
            canal: canal al que enviar
            visibilidad: Si/No. Si se quiere que se cojan los posts NSFW o no
            cuenta: cuenta/cuentas de twitter/subreddit. En caso de varias cuentas separadas por espacios
        """

        if visibilidad == "nsfw" and not canal.nsfw:
            await ctx.send(
                "El canal no es NSFW, utiliza otro canal o cambia los permisos."
            )
            return

        account = []

        for arg in cuenta:

            if "twitter.com/" not in arg and "reddit.com/r/" not in arg:
                await ctx.send("Se ha introducido una cuenta no válida")
                return

            if "twitter" in arg:
                account.append("twitter@" + arg.split("/")[-1])
            else:
                account.append("reddit@" + arg.split("/")[-2])

        cuenta = " ".join(account)
        create_post(ctx.guild, [canal.id, visibilidad, cuenta])
        await ctx.send("Post creado")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rmpost(self, ctx: commands.Context, post_id: int):
        """[Admin]Permite eliminar una cuenta de twitter/subreddit de un canal.

        Args:
            id: id del post a eliminar
        """

        remove_post(ctx.guild, post_id)
        await ctx.send("Post eliminado")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def posts(self, ctx: commands.Context):
        "[Admin]Muestra los posts que se han añadido"
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

    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx: commands.Context, canal: str = None) -> None:

        """[Admin]Configurar los canales del bot

        Si no se especifica ningun canal, se configuraran todos los canales
        """

        def check(m: nextcord.Message) -> bool:
            return m.author == ctx.author and m.channel == ctx.channel

        if canal is not None:
            if not canal in self.get_channel_types():
                await ctx.send(
                    "Canal no valido, el canal debe ser uno de los siguientes: `{}`".format(
                        ", ".join(self.get_channel_types())
                    )
                )
                return
            await ctx.send("Seleccione el canal que servirá como {}".format(canal))
            msg = await self.bot.wait_for("message", check=check, timeout=60)
            channel = await self.fetch_channel_from_message_content(msg)

            create_channel(
                ctx.guild,
                [
                    channel.id,
                    canal,
                    channel.name,
                ],
            )
            await ctx.send("Canal {} configurado".format(canal))
            return

        await ctx.send(
            "Empezando configuración. Se le pedirá establecer varios canales. Si no quiere establecer un canal, escriba `skip`"
        )
        await sleep(2)
        for x in CHANNELS:
            await self.setup_channel(ctx, x["channel_type"], x["channel_description"])

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
        channel = await self.bot.fetch_channel(channel_id)
        return channel

    async def setup_channel(
        self, ctx: commands.Context, channel_type: str, channel_description: str
    ):
        def check(m: nextcord.Message) -> bool:
            return m.author == ctx.author and m.channel == ctx.channel

        # General channel
        await ctx.send(
            "Seleccione el canal {}. Se utiliza para {}".format(
                channel_type, channel_description
            )
        )
        msg = await self.bot.wait_for("message", check=check, timeout=60)
        if msg.content.lower() != "skip":

            channel = await self.fetch_channel_from_message_content(msg)

            create_channel(
                ctx.guild,
                [
                    channel.id,
                    channel_type,
                    channel.name,
                ],
            )
            await ctx.send("Canal {} añadido".format(channel_type))

    def get_channel_types(self) -> List[str]:
        """Gets the channel_types from CHANNEL

        Returns:
            List[str]: contains the channel_types
        """
        output = []
        for x in CHANNELS:
            output.append(x["channel_type"])

        return output


def setup(bot: commands.Bot):
    bot.add_cog(admin(bot))