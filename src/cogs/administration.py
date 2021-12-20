import logging
from os import name
from nextcord import activity
from nextcord.ext import commands
import nextcord
from nextcord.ext.commands.core import has_permissions
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


def setup(bot: commands.Bot):
    bot.add_cog(administration(bot))
