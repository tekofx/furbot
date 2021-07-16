import discord
from discord.ext import commands
import random
import os
from cogs.functions import cracker_id, creator_id, magnet_id, enanas_path


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
            usuario = str(context.author)[:-5]
        else:
            usuario = str(user)[:-5]

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
            usuario = str(context.author)[:-5]
        else:
            usuario = str(user)[:-5]
        await context.channel.send(output.format(usuario, num))

    @commands.command()
    async def gay(self, context, *, user: discord.Member = None):
        """Maricon el ultimo"""

        num = random.randint(0, 100)
        output = "{} es {}% gay"
        if user is None:
            if context.author.id == cracker_id:
                num = 100
                usuario = "Cracker"
            elif context.author.id == creator_id:
                num = 100
                usuario = "Teko"
            elif context.author.id == magnet_id:
                num = 100
                usuario = "Magnet"
            else:
                usuario = str(context.author)[:-5]
        else:
            if user.id == cracker_id:
                num = 100
                usuario = "Cracker"
            elif user.id == magnet_id:
                num = 100
                usuario = "Magnet"
            elif user.id == creator_id:
                num = 100
                usuario = "Teko"
            else:
                usuario = str(user)[:-5]

        await context.channel.send(output.format(usuario, num))

    @commands.command()
    async def str8(self, context, *, user: discord.Member = None):
        """Super str8 el ultimo"""

        num = random.randint(0, 100)
        output = "{} es {}% hetero"
        if user is None:
            if context.author.id == cracker_id:
                num = 0
                usuario = "Cracker"
            elif context.author.id == creator_id:
                num = 0
                usuario = "Teko"
            elif context.author.id == magnet_id:
                num = 0
                usuario = "Magnet"
            else:
                usuario = str(context.author)[:-5]
        else:
            if user.id == cracker_id:
                num = 0
                usuario = "Cracker"
            elif user.id == magnet_id:
                num = 0
                usuario = "Magnet"
            elif user.id == creator_id:
                num = 0
                usuario = "Teko"
            else:
                usuario = str(user)[:-5]

        await context.channel.send(output.format(usuario, num))

    @commands.command()
    async def capitalist(self, context, *, user: discord.Member = None):
        """Serás capitalista y te convertirás en el nuevo lobo de Wall Street?"""

        num = random.randint(0, 100)
        output = "{} es {}% capitalista"
        if user is None:
            usuario = str(context.author)[:-5]
        else:
            usuario = str(user)[:-5]
        await context.channel.send(output.format(usuario, num))

    @commands.command()
    async def enana(self, context, enana_name: str = None):
        """Elije una enana o consigue una aleatoria de forma totalmente gratuita

        Uso:
            fur enana           ---> Enana aleatoria
            fur enana <palabra> ---> Enana que contega palabra
        """

        if enana_name is None:
            output = random.choice(os.listdir(enanas_path))
            name = output.split("/")[-1]  # Remove path
            name = name[:-4]  # Remove extension

            await context.channel.send(name, file=discord.File(enanas_path + output))

        else:
            for filenames in os.listdir(enanas_path):
                if enana_name.lower() in filenames.lower():
                    output = filenames
                    break

            await context.channel.send(file=discord.File(enanas_path + output))

    @commands.command()
    async def enanalist(self, context):

        """Lista todas las enanas existentes"""
        output = os.listdir(enanas_path)
        output[:] = [s.replace(".png", "") for s in output]
        output[:] = [s.replace("'", "") for s in output]
        await context.channel.send(output)


def setup(bot):
    bot.add_cog(Fun(bot))
