import hikari
import lightbulb
from functions import yaml_f


class Administration(lightbulb.Plugin):
    @lightbulb.command(name="activity")
    async def change_activity(
        self, ctx: lightbulb.Context, activity_name: str, activity_type: str = None
    ):
        """[Admin] Cambiar actividad del bot"""
        if activity_type is None:
            activity_type = 1

        else:

            if activity_type.lower() == "play":
                activity_type = 1

            if activity_type.lower() == "watch":
                activity_type = 3

        yaml_f.change_activity(activity_name)
        activity = hikari.Activity(name=activity_name, type=2)

        try:
            await bot_instance.update_presence(activity=activity)

        except FileNotFoundError:
            await ctx.respond("Error: No se ha podido establecer la actividad")

        await ctx.respond("Cambiada actividad a " + activity_name)


def load(bot: lightbulb.Bot):
    global bot_instance
    bot_instance = bot
    bot.add_plugin(Administration)
