import discord
import random
import os
from discord.ext import commands
import logging

insultsPath = 'insults.txt'


class roast(commands.Cog):
    """Insultos varios """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def aputo(self, context):
        """Asriel puto
        """
        await context.channel.send("Asriel puto")

    @commands.command()
    async def cputo(self, context):
        """Cracker puto
        """
        await context.channel.send("Cracker puto")

    @commands.command()
    async def caputo(self, context):
        """Capi puto
        """
        await context.channel.send("Capi puto")

    @commands.command()
    async def daputo(self, context):
        """Dachi puto
        """
        await context.channel.send("Dachi puto")

    @commands.command()
    async def gaputo(self, context):
        """Gala puto
        """
        await context.channel.send("Gala puto")

    @commands.command()
    async def garich(self, context):
        """Gala rich
        """
        output="Gala rich porque compra Axe, tiene 5 Alexas, tiene una limpiadora que le regala cosas y tiene una tele 4k"
        await context.channel.send(output)

    @commands.command()
    async def magnetputo(self, context):
        """Magnet puto
        """
        await context.channel.send("Magnet puto")
    @commands.command()
    async def peputo(self, context):
        """Pen puto
        """
        await context.channel.send("Pen puto")

    @commands.command()
    async def teputo(self, context):
        """Teko puto
        """
        await context.channel.send("Teko puto")

    @commands.command()
    async def teodio(self, context, *, user: discord.Member = None):
        """Muestra tu odio al bot
        """
        if user==None:
            usuario = context.author.mention
        else:
            usuario = user.mention
        output = '{} %s ' % ('Yo te odio mas pedazo de basura')
        await context.channel.send(output.format(usuario))

    @commands.command()
    async def sliputo(self, context):
        """Sliva puto
        """
        await context.channel.send("Sliva puto")

    @commands.command()
    async def steputo(self, context):
        """Stewan puto
        """
        await context.channel.send("Stewan puto")

    @commands.command(name='tputo')
    async def tputo(self, context):
        """Thedax puto
        """
        await context.channel.send("Thedax puto")

    @commands.command()
    async def zaputo(self, context):
        """Zaffy puto
        """
        await context.channel.send("Zaffy puto")

    @commands.command()
    async def insult(self, context, *, user: discord.Member = None):
        """Insulta gente 7w7

            Genera un insulto aleatorio
        """
        if user == None:
            usuario = context.author.mention
        else:
            usuario = user.mention
        try:
            with open(insultsPath) as f:
                insults = f.readlines()

            output = '{} %s ' % (random.choice(insults))
            await context.channel.send(output.format(usuario))
        except:
            logging.error("Error at getting insults.txt")


def setup(bot):
    bot.add_cog(roast(bot))
