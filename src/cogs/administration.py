import discord
from discord.ext import commands
from functions import (
    delete_content_in_file,
    help_txt,
    activity_txt,
    write_in_file,
)
import logging

from main import es_viernes


class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    async def help(self, context, user: discord.Member = None):
        """Muestra la info de Zaffy"""
        f = open(help_txt, "r")
        general = f.read()
        await context.channel.send(general)
        f.close()

    @commands.command(name="activity")
    @commands.has_permissions(administrator=True)
    async def change_activity(self, context, activity_name: str, activity: str = None):
        """[Admin] Cambiar actividad del bot"""
        if activity is None:
            delete_content_in_file(activity_txt)
            write_in_file(activity_txt, activity_name)
            try:
                with open(activity_txt) as f:
                    aux = f.readline()
                await self.bot.change_presence(activity=discord.Game(name=aux))
            except discord.HTTPException:
                logging.error("Error: activity.txt not found")
                await context.channel.send(
                    "Error: No se ha encontrado el archivo activity.txt"
                )
                await context.channel.send("Contacte con un administrador")

        else:
            if activity.lower() == "watching":
                await self.bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.watching, name=activity_name
                    )
                )
            if activity.lower() == "streaming":
                await self.bot.change_presence(
                    activity=discord.Streaming(name="My Stream", url=activity_name)
                )
            if activity.lower() == "listening":
                await self.bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.listening, name=activity_name
                    )
                )

        await context.channel.send("Cambiada actividad a " + activity_name)


def setup(bot):
    bot.add_cog(Administration(bot))
