import discord
from discord.ext import commands
import random
import os
from functions import cracker_id, creator_id, magnet_id, enanas_path


class Fun(commands.Cog):
    """Cosas random y divertidas"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def penis(self, context, *, user: discord.Member = None):
        """Buena tula

        Genera un pene de tamaño aleatorio.
        Uso:
        fur penis            --> Tu tula
        fur penis @<usuario> --> La tula de @<usuario>
        """

        num = random.randint(1, 15)
        output = "El pene de {}\n"
        if user is None:
            usuario = context.author.name
        else:
            usuario = user.name

        output += "8"
        for x in range(num):
            output += "="
        output += "D"
        await context.channel.send(output.format(usuario))

    @commands.command()
    async def communism(self, context, *, user: discord.Member = None):
        """Serás un comunista bolivariano que apoya al Coletas?"""

        num = random.randint(0, 100)
        output = "{} es {}% comunista"
        if user is None:
            usuario = context.author.name
        else:
            usuario = user.name
        await context.channel.send(output.format(usuario, num))

    @commands.command()
    async def gay(self, context, *, user: discord.Member = None):
        """Maricon el ultimo"""

        num = random.randint(0, 100)
        output = "{} es {}% gay"
        if user is None:
            usuario = context.author.name
        else:
            usuario = user.name

        await context.channel.send(output.format(usuario, num))

    @commands.command()
    async def str8(self, context, *, user: discord.Member = None):
        """Super str8 el ultimo"""

        num = random.randint(0, 100)
        output = "{} es {}% hetero"
        if user is None:
            usuario = context.author.name
        else:
            usuario = user.name

        await context.channel.send(output.format(usuario, num))

    @commands.command()
    async def capitalist(self, context, *, user: discord.Member = None):
        """Serás capitalista y te convertirás en el nuevo lobo de Wall Street?"""

        num = random.randint(0, 100)
        output = "{} es {}% capitalista"
        if user is None:
            usuario = context.author.name
        else:
            usuario = user.name
        await context.channel.send(output.format(usuario, num))


def setup(bot):
    bot.add_cog(Fun(bot))
