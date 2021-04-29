import discord
from discord.ext import commands
import os
from cogs.functions import *

help_txt = 'help.txt'


class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def version(self, context, user: discord.Member = None):
        embed = discord.Embed(title="FurBot", description='El mejor bot furro')
        embed.add_field(name='Version', value='V 2.0', inline=False)
        await context.channel.send(embed=embed)

    @commands.command(name='info')
    async def help(self, context, user: discord.Member = None):
        """Muestra la info de Zaffy
        """
        f = open(help_txt, 'r')
        general = f.read()
        await context.channel.send(general)
        f.close()


    @commands.command(name="rm")
    @commands.check(is_owner)
    async def remove_sticker(self, context, sticker):
        """ [ADMIN] Borra un sticker
        """
        os.system("rm "+stickersPath+sticker+'.png')
        logging.info("Sticker "+sticker+" deleted")
        await context.channel.send("Sticker "+sticker+" eliminado")

def setup(bot):
    bot.add_cog(Administration(bot))
