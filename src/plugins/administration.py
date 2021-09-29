import hikari
import lightbulb
from functions import yaml_f


class Administration(lightbulb.Plugin):
    @lightbulb.command(name="activity")
    async def change_activity(self, ctx: lightbulb.Context, activity_name: str):
        """[Admin] Cambiar actividad del bot"""

        yaml_f.change_activity(activity_name)
        activity = hikari.Activity(name=activity_name)

        try:
            await bot_instance.update_presence(activity=activity)

        except FileNotFoundError:
            await ctx.respond("Error: No se ha podido establecer la actividad")

        await ctx.respond("Cambiada actividad a " + activity_name)


def load(bot: lightbulb.Bot):
    global bot_instance
    bot_instance = bot
    bot.add_plugin(Administration)
