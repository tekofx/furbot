import discord
from discord.ext import commands
from functions import yaml_f


class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="activity")
    @commands.has_permissions(administrator=True)
    async def change_activity(self, context, activity_name: str):
        """[Admin] Cambiar actividad del bot"""
        yaml_f.change_activity(activity_name)
        try:
            await self.bot.change_presence(
                activity=discord.Game(name=yaml_f.get_activity())
            )
        except discord.HTTPException:
            await context.channel.send("Error: No se ha podido establecer la actividad")

        await context.channel.send("Cambiada actividad a " + activity_name)


def setup(bot):
    bot.add_cog(Administration(bot))
