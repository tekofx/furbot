import logging
from nextcord.ext import commands
import nextcord
from utils.database import (
    check_entry_in_database,
    create_color,
    create_connection,
    create_rank,
    create_specie,
    create_user,
    set_birthday,
    set_name,
)
from utils.functions import yaml_f
from asyncio import sleep
from utils.bot import Bot

log = logging.getLogger(__name__)


class administration(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(name="activity")
    @commands.has_permissions(administrator=True)
    async def change_activity(self, ctx: commands.Context, activity_name: str):
        """[Admin] Cambiar actividad del bot"""
        yaml_f.change_activity(activity_name)
        activity = nextcord.Game(activity_name)

        try:
            await self.bot.change_presence(
                status=nextcord.Status.online, activity=activity
            )

        except Exception:
            await ctx.respond("Error: Contacte con un administrador")
            log.error("Error: ".format(Exception))

        await ctx.respond("Cambiada actividad a " + activity_name)
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
            specie_data = [specie.id, specie.name]
            create_specie(con, specie_data)
            await ctx.send("Especie {} añadida".format(specie.mention))
            log.info("Added specie " + specie.name)

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
            rank_data = [rank.id, rank.name]
            create_rank(con, rank_data)
            await ctx.send("Rank {} añadido".format(rank.mention))
            log.info("Added rank " + rank.name)

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
            color_data = [color.id, color.name]
            create_color(con, color_data)
            await ctx.send("Color {} añadido".format(color.mention))
            log.info("Added color " + color.name)

    @commands.command(name="upuser")
    @commands.has_permissions(administrator=True)
    async def update_users(self, ctx: commands.Context):
        """[Admin] Actualiza la lista de usuarios con los usuarios que no existen\n"""
        guild = await self.bot.fetch_guild(ctx.guild.id)
        server = str(ctx.guild.id)

        con = create_connection(server)
        try:

            members = guild.fetch_members()
            async for member in members:
                set_name(member.id, member.name)

                if not member.bot and not check_entry_in_database(
                    con, "users", member.id
                ):
                    member_data = [member.id, member.name, member.joined_at]
                    create_user(con, member_data)
                else:
                    set_name(member.id, member.name)

        except Exception as error:
            log.error("{}".format(error))
        else:

            await ctx.send("Actualizada lista de usuarios")
            log.info("Updated users in database")

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
        """[Admin] Elimina mensajes de un canal"""
        messages_to_delete = []
        async for message in ctx.channel.history(limit=num + 1):
            messages_to_delete.append(message)
        await ctx.channel.delete_messages(messages_to_delete)
        message = await ctx.send("Eliminados {} mensajes".format(num))
        await sleep(5)
        await message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(administration(bot))
