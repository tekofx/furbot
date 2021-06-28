import discord
from discord.ext import commands
import os
from cogs.functions import is_admin, stickersPath, help_txt, admin, activity_txt
import logging


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
    @commands.check(is_admin)
    async def change_activity(self, context, activity_name: str, activity: str = None):
        """[Admin] Cambiar actividad del bot"""
        if activity == None:
            open(activity_txt, "w").close()
            var = "echo " + activity_name + ">>" + activity_txt
            os.system(var)
            try:
                with open(activity_txt) as f:
                    aux = f.readline()
                await self.bot.change_presence(activity=discord.Game(name=aux))
            except:
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

    @commands.command(name="admin")
    async def check_admin(self, context):
        """Comprueba si eres admin del bot"""
        output = "No eres admin del bot"
        if context.author.id in admin:
            output = "Eres admin del bot"
        await context.channel.send(output)


def setup(bot):
    bot.add_cog(Administration(bot))
