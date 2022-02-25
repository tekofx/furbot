import logging
from typing import List
from nextcord.ext import commands
import nextcord
from utils.database import (
    create_channel,
    create_connection,
    create_role,
    set_birthday,
)
from asyncio import sleep
from utils.data import config_yaml
from utils.bot import Bot
import yaml

log = logging.getLogger(__name__)
ROLE_EXISTS = "UNIQUE constraint failed: roles.id"
CHANNELS = [
    {"channel_type": "general", "channel_description": "los mensajes de cumpleaños."},
    {
        "channel_type": "audit",
        "channel_description": "mostrar las acciones que hace el bot a los administradores.",
    },
    {"channel_type": "memes", "channel_description": "mandar memes cada hora"},
    {"channel_type": "lobby", "channel_description": "mandar mensajes de bienvenida"},
    {
        "channel_type": "bot_news",
        "channel_description": "mandar info sobre nuevas versiones del bot",
    },
    {"channel_type": "games", "channel_description": "mandar juegos gratuitos"},
]


class administration(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx: commands.Context, canal: str = None) -> None:
        """Configurar los canales del bot

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

    @commands.command(name="addspecie")
    @commands.has_permissions(administrator=True)
    async def add_species(self, ctx: commands.Context, *species: nextcord.Role):
        """[Admin] Añade una especie al bot

        Uso:
            fur addspecie <rol>
        """
        for specie in species:
            try:
                create_role(ctx.guild, specie.id, specie.name, "specie")
            except Exception as error:
                if ROLE_EXISTS in error.args:
                    await ctx.send(
                        "No se pudo añadir la especie {}. Esa especie ya existe en la base de datos".format(
                            specie.mention
                        )
                    )
            else:
                log.info("Added specie " + specie.name)
                await ctx.send("Especie {} añadida".format(specie.mention))

    @commands.command(name="addrank")
    @commands.has_permissions(administrator=True)
    async def add_rank(self, ctx: commands.Context, *ranks: nextcord.Role):
        """[Admin] Añade un rank al bot

        Uso:
            fur addrank <rol>
        """
        for rank in ranks:
            try:
                create_role(ctx.guild, rank.id, rank.name, "rank")
            except Exception as error:
                if ROLE_EXISTS in error.args:
                    await ctx.send(
                        "No se pudo añadir el rango {}. Ese rango ya existe en la base de datos".format(
                            rank.mention
                        )
                    )
            else:
                log.info("Added rank " + rank.name)
                await ctx.send("Rango {} añadido".format(rank.mention))

    @commands.command(name="addcolor")
    @commands.has_permissions(administrator=True)
    async def add_color(self, ctx: commands.Context, *colors: nextcord.Role):
        """[Admin] Añade un color al bot

        Uso:
            fur addcolor <rol>
        """
        for color in colors:
            try:
                create_role(ctx.guild, color.id, color.name, "color")
            except Exception as error:
                if ROLE_EXISTS in error.args:
                    await ctx.send(
                        "No se pudo añadir el color {}. Ese color ya existe en la base de datos".format(
                            color.mention
                        )
                    )
            else:
                log.info("Added color " + color.name)
                await ctx.send("Color {} añadido".format(color.mention))

    @commands.command()
    async def addcumple(
        self, ctx: commands.Context, birthday: str, user: nextcord.Member
    ):
        """[Admin] Añade el cumpleaños de alguien al bot

        Uso:
            fur addcumple <dia>-<mes> @<usuario>

        Ejemplo:
            fur addcumple 16-1 @Teko
        """

        set_birthday(ctx.guild, user.id, birthday)
        await ctx.send("Añadido cumpleaños de " + user.display_name)

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
    bot.add_cog(administration(bot))
