import discord
import random
from discord.ext import commands
import logging
from cogs.functions import insults_txt, is_admin, magnet_id, animos_txt


class roast(commands.Cog):
    """Insultos varios"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def garich(self, context):
        """Gala rich"""
        output = "Gala rich porque compra Axe, tiene 5 Alexas, tiene una limpiadora que le regala cosas y tiene una tele 4k"
        await context.channel.send(output)

    @commands.command()
    async def tecute(self, context):
        """Teko cute"""
        if context.author.id == magnet_id:
            await context.channel.send("Teko cute")
        else:
            await context.channel.send("Teko NO cute")

    @commands.command()
    async def teodio(self, context, *, user: discord.Member = None):
        """Muestra tu odio al bot"""
        if user == None:
            usuario = context.author.mention
        else:
            usuario = user.mention
        output = "{} %s " % ("Yo te odio mas pedazo de basura")
        await context.reply(output.format(usuario))

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
            with open(insults_txt) as f:
                insults = f.readlines()

            output = "{} %s " % (random.choice(insults))
            await context.reply(output.format(usuario))
        except:
            logging.error("Error at getting insults.txt")

    @commands.check(is_admin)
    @commands.command()
    async def addinsult(self, context, *insults: str):
        """[ADMIN] Añade insulto

        Uso:
            fur addinsulto <insulto>
            fur addinsulto <insulto1> <insulto2>...

        Ejemplo:
            fur addinsulto "feo" "horrible"
        """
        try:
            f = open(insults_txt, "a")
            for insult in insults:
                insult = insult.replace('"', "")
                f.write(insult + "\n")
            f.close()
            await context.channel.send("Insulto/s añadido/s")
        except:
            logging.error("Error at getting insults.txt")

    @commands.command()
    async def animo(self, context, *, user: discord.Member = None):
        """Anima a la gente"""
        if user == None:
            usuario = context.author.mention
        else:
            usuario = user.mention
        try:
            with open(animos_txt) as f:
                animos = f.readlines()

            output = "{} %s " % (random.choice(animos))
            await context.reply(output.format(usuario))
        except:
            logging.error("Error at getting animos.txt")

    @commands.check(is_admin)
    @commands.command()
    async def addanimo(self, context, *animos: str):
        """[ADMIN] Añade animos

        Uso:
            fur addanimo <animo>
            fur addanimo <animo1> <animo2>...

        Ejemplo:
            fur addanimo "guapo" "hermoso"
        """
        try:
            f = open(animos_txt, "a")
            for animo in animos:
                animo = animo.replace('"', "")
                f.write(animo + "\n")
            f.close()
            await context.channel.send("animo/s añadido/s")
        except:
            logging.error("Error at getting animos.txt")


def setup(bot):
    bot.add_cog(roast(bot))
