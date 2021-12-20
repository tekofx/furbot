import logging
from nextcord.ext import commands
import nextcord
from utils.database import create_color, create_connection, create_rank, create_specie
from utils.functions import yaml_f

log = logging.getLogger(__name__)


class administration(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
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
    async def add_species(self, ctx: commands.Context, specie: nextcord.Role):
        """[Admin] Añade una especie al bot

        Uso:
            fur addspecie <rol>
        """
        server = str(ctx.guild.id)
        con = create_connection(server)
        specie_data = [specie.id, specie.name]
        create_specie(con, specie_data)
        await ctx.send("Especie {} añadida".format(specie.mention))
        log.info("Added specie " + specie.name)

    @commands.command(name="addrank")
    async def add_rank(self, ctx: commands.Context, rank: nextcord.Role):
        """[Admin] Añade un rank al bot

        Uso:
            fur addrank <rol>
        """
        server = str(ctx.guild.id)
        con = create_connection(server)
        rank_data = [rank.id, rank.name]
        create_rank(con, rank_data)
        await ctx.send("Rank {} añadido".format(rank.mention))
        log.info("Added rank " + rank.name)

    @commands.command(name="addcolor")
    async def add_color(self, ctx: commands.Context, color: nextcord.Role):
        """[Admin] Añade un color al bot

        Uso:
            fur addcolor <rol>
        """
        server = str(ctx.guild.id)
        con = create_connection(server)
        color_data = [color.id, color.name]
        create_color(con, color_data)
        await ctx.send("Color {} añadido".format(color.mention))
        log.info("Added color " + color.name)


def setup(bot: commands.Bot):
    bot.add_cog(administration(bot))
