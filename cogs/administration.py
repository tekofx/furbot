import discord
from discord.ext import commands
import os
from cogs.functions import is_owner, stickersPath, help_txt
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

    
    @commands.command(name='activity')
    @commands.check(is_owner)
    async def change_activity(self, context, activity_name:str, activity:str):
        """ Cambiar actividad del bot 
        """
        if activity.lower()=='watching':
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_name))
        elif activity.lower()=='streaming':
            await self.bot.change_presence(activity=discord.Streaming(name="My Stream", url=activity_name))
        elif activity.lower()=='listening':
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity_name))
        else:
            await self.bot.change_presence(activity=discord.Game(name=activity_name))

        await context.channel.send("Cambiada actividad a "+activity_name)
 
def setup(bot):
    bot.add_cog(Administration(bot))
