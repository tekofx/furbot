import logging
from os import error
import hikari
import lightbulb
from hikari import permissions
from functions import yaml_f

log = logging.getLogger(__name__)


class Administration(lightbulb.Plugin):
    def __init__(self, bot: lightbulb.Bot):
        super().__init__(name="Administration")
        self.bot = bot

    @lightbulb.command(name="activity")
    async def change_activity(self, ctx: lightbulb.Context, activity_name: str):
        """[Admin] Cambiar actividad del bot"""

        yaml_f.change_activity(activity_name)
        activity = hikari.Activity(name=activity_name)

        try:
            await self.bot.update_presence(activity=activity)

        except Exception:
            await ctx.respond("Error: Contacte con un administrador")
            log.error("Error: ".format(Exception))

        await ctx.respond("Cambiada actividad a " + activity_name)
        log.info("Changed activity to " + activity_name)

    @lightbulb.check(
        lightbulb.has_guild_permissions(permissions.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command(name="addspecie")
    async def add_species(self, ctx: lightbulb.Context, specie: hikari.Role):
        """Añade una especie al bot

        Uso:
            fur addspecie <rol>
        """
        yaml_f.add_species(specie.name, specie.id)
        await ctx.respond("Especie {} añadida".format(specie.mention))
        log.info("Added specie " + specie.name)


def load(bot: lightbulb.Bot):
    bot.add_plugin(Administration(bot))


def unload(bot: lightbulb.Bot):
    bot.remove_plugin("Administration")
