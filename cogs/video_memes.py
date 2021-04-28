import random
import textwrap
import time
import wget
from PIL import ImageFont, ImageDraw
from sympy import symbols, solve
from cogs.functions import *
import discord

memeTemplatesPath = "memes_templates/"
memePath = "memes/"


class video_memes(commands.Cog):
    """Memés """

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def españa(self, context, *, user: discord.Member = None):
        """Arriba España!!!
            
            Uso: fur españa "@<usuario>
        """
        await context.channel.send('Procesando video')
        create_video_meme("españa", get_user(context, user))

        # Send meme
        await context.channel.send(file=discord.File(memeTemplatesPath + "output.mp4"))
        log("info","Meme sent")

        # Delete output
        delete_files(['output.mp4'])


    @commands.command()
    async def betis(self, context, *, user: discord.Member = None):
        """Olé mi Betis

        """
        await context.channel.send('Procesando video')
        log("info","Meme sent")
        create_video_meme("betis", get_user(context, user))

        # Send meme
        await context.channel.send(file=discord.File(memeTemplatesPath + "output.mp4"))
        log("info","Meme sent")

        # Delete output
        delete_files(['output.mp4'])


     @commands.command()
    async def communist(self, context, *, user: discord.Member = None):
        """Viva el proletariado"""
        await context.channel.send('Procesando video')
        create_video_meme("communist", get_user(context, user))

        # Send meme
        await context.channel.send(file=discord.File(memeTemplatesPath + "output.mp4"))
        log("info","Meme sent")

        # Delete output
        delete_files(['output.mp4'])


    @commands.command()
    async def falange(self, context, *, user: discord.Member = None):
        """Viva Francisco Franco!!!
            
            Uso: fur falange "@<usuario>
        """
        await context.channel.send('Procesando video')
        create_video_meme("falange", get_user(context, user))

        # Send meme
        await context.channel.send(file=discord.File(memeTemplatesPath + "output.mp4"))
        log("info","Meme sent")

        # Delete output
        delete_files(['output.mp4'])


     @commands.command()
    async def aragon(self, context, *, user: discord.Member = None):
        """Viva Aragón! (pero menos que León)"""

        await context.channel.send('Procesando video')
        create_video_meme("aragon", get_user(context, user))

        # Send meme
        await context.channel.send(file=discord.File(memeTemplatesPath + "output.mp4"))
        log("info","Meme sent")


        # Delete output
        delete_files(['output.mp4'])


    @commands.command()
    async def leon(self, context, *, user: discord.Member = None):
        """Viva León!"""

        await context.channel.send('Procesando video')
        log("info","Meme sent")
        create_video_meme("leon", get_user(context, user))

        # Send meme
        await context.channel.send(file=discord.File(memeTemplatesPath + "output.mp4"))
        log("info","Meme sent")


        # Delete output
        delete_files(['output.mp4'])



def setup(bot):
    bot.add_cog(video_memes(bot))
