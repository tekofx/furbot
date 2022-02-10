import logging
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


class administration(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx: commands.Context) -> None:
        """Configurar los canales del bot"""

        def check(m: nextcord.Message) -> bool:
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(
            "Empezando configuración. Se le pedirá establecer varios canales. Si no quiere establecer un canal, escriba `skip`"
        )
        await sleep(2)

        try:
            # General channel
            await ctx.send(
                "Seleccione el canal general. Se utiliza para los mensajes de cumpleaños."
            )
            msg = await self.bot.wait_for("message", check=check, timeout=60)
            log.info(msg.content)

            channel_id = msg.content.replace("<#", "").replace(">", "")
            channel = await self.bot.fetch_channel(channel_id)

            con = create_connection(str(ctx.guild.id))

            create_channel(
                con,
                [
                    channel.id,
                    "general",
                    channel.name,
                ],
            )

            # Audit channel
            await ctx.send(
                "Canal audit. Se usa para mostrar las acciones que hace el bot a los administradores."
            )
            msg = await self.bot.wait_for("message", check=check, timeout=60)
            log.info(msg.content)

            channel_id = msg.content.replace("<#", "").replace(">", "")
            channel = await self.bot.fetch_channel(channel_id)

            create_channel(
                con,
                [
                    channel.id,
                    "audit",
                    channel.name,
                ],
            )

            # Canal memes
            await ctx.send("Canal memes. Para mandar memes cada hora")
            msg = await self.bot.wait_for("message", check=check, timeout=60)

            channel_id = msg.content.replace("<#", "").replace(">", "")
            channel = await self.bot.fetch_channel(channel_id)

            create_channel(
                con,
                [
                    channel.id,
                    "memes",
                    channel.name,
                ],
            )

            # Canal lobby
            await ctx.send("Canal lobby. Se usa para mandar mensajes de bienvenida")
            msg = await self.bot.wait_for("message", check=check, timeout=60)

            channel_id = msg.content.replace("<#", "").replace(">", "")
            channel = await self.bot.fetch_channel(channel_id)

            create_channel(
                con,
                [
                    channel.id,
                    "lobby",
                    channel.name,
                ],
            )
        except (nextcord.Forbidden, Exception) as e:
            if isinstance(e, nextcord.Forbidden):
                await ctx.send(
                    "Error, el bot no tiene permisos para ver el canal. Vuelve a ejecutar el comando cuando el bot tenga permiso de ver el canal."
                )
            else:
                await ctx.send("Error desconocido, contacta con un administrador.")
                log.error("Unkwon error: {}".format(e))

            con.close()
            return
        else:
            await ctx.send("Añadidos canales")

            con.close()

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
            log.error("Error: ".format(error))
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
        server = str(ctx.guild.id)
        con = create_connection(server)
        for specie in species:
            try:
                create_role(con, specie.id, specie.name, "specie")
            except Exception as error:
                if "UNIQUE constraint failed: roles.id" in error.args:
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
        server = str(ctx.guild.id)
        con = create_connection(server)
        for rank in ranks:
            try:
                create_role(con, rank.id, rank.name, "rank")
            except Exception as error:
                if "UNIQUE constraint failed: roles.id" in error.args:
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
        server = str(ctx.guild.id)
        con = create_connection(server)
        for color in colors:
            try:
                create_role(con, color.id, color.name, "color")
            except Exception as error:
                if "UNIQUE constraint failed: roles.id" in error.args:
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
        con = create_connection(str(ctx.guild.id))

        set_birthday(con, user.id, birthday)
        await ctx.send("Añadido cumpleaños de " + user.display_name)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context, num: int):
        """[Admin] Elimina mensajes de un canal

        Uso:
            fur clear <num_mensajes>
        """

        messages_to_delete = []
        if ctx.message.reference is None:
            async for message in ctx.channel.history(limit=num + 1):
                messages_to_delete.append(message)

        else:
            async for message in ctx.channel.history(
                limit=num, before=ctx.message.reference.cached_message
            ):
                messages_to_delete.append(message)
                print(message.content)
        await ctx.channel.delete_messages(messages_to_delete)
        message = await ctx.send("Eliminados {} mensajes".format(num))
        await sleep(5)
        await message.delete()
        await ctx.message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(administration(bot))
