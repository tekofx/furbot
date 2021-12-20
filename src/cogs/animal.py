import logging
import nextcord
from nextcord.ext import commands
import os

import requests

from utils.functions import write_in_file

log = logging.getLogger(__name__)

animal_history_txt = "files/resources/data/animal_history.txt"


class animal(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def fox(self, ctx: commands.Context):
        """Fotos de zorros hermosos"""
        with ctx.typing():
            message = await ctx.send("Buscando fotos de zorros hermosos")

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image("hourlyFox")

            # Write in history
            write_in_file(animal_history_txt, tweet_image_url + "\n")

            # Download image
            r = requests.get(tweet_image_url, allow_redirects=True)
            open("files/" + "image.jpg", "wb").write(r.content)

        image = nextcord.File("files/" + "image.jpg")
        await ctx.send(file=image)
        os.remove("files/image.jpg")
        await message.delete()

    @commands.command()
    async def arctic_fox(self, ctx: commands.Context):
        """Fotos de zorros articos"""
        with ctx.typing():
            message = await ctx.send("Buscando fotos de zorros hermosos")

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image("DailyArcticFox")

            # Write in history
            write_in_file(animal_history_txt, tweet_image_url + "\n")

            # Download image
            r = requests.get(tweet_image_url, allow_redirects=True)
            open("files/" + "image.jpg", "wb").write(r.content)
        image = nextcord.File("files/" + "image.jpg")
        await ctx.send(file=image)
        os.remove("files/image.jpg")
        await message.delete()

    @commands.command()
    async def wolf(self, ctx: commands.Context):
        """Fotos de zorros hermosos"""
        with ctx.typing():
            message = await ctx.send("Buscando fotos de lobos lobitos lobones")

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image("hourlywolvesbot")

            # Write in history
            write_in_file(animal_history_txt, tweet_image_url + "\n")

            # Download image
            r = requests.get(tweet_image_url, allow_redirects=True)
            open("files/" + "image.jpg", "wb").write(r.content)
        image = nextcord.File("files/" + "image.jpg")
        await ctx.send(file=image)
        os.remove("files/image.jpg")
        await message.delete()

    @commands.command()
    async def bird(self, ctx: commands.Context):
        """Fotos de pajaros"""
        with ctx.typing():
            message = await ctx.send("Buscando fotos de pajaritos")

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image("eugeniogarciac2")

            # Write in history
            write_in_file(animal_history_txt, tweet_image_url + "\n")

            # Download image
            r = requests.get(tweet_image_url, allow_redirects=True)
            open("files/" + "image.jpg", "wb").write(r.content)
        image = nextcord.File("files/" + "image.jpg")
        await ctx.send(file=image)
        os.remove("files/image.jpg")
        await message.delete()

    @commands.command()
    async def pigeon(self, ctx: commands.Context):
        """Fotos de palomas"""
        with ctx.typing():
            message = await ctx.send("Buscando fotos de palomas")

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image("a_london_pigeon")

            # Write in history
            write_in_file(animal_history_txt, tweet_image_url + "\n")

            # Download image
            r = requests.get(tweet_image_url, allow_redirects=True)
            open("files/" + "image.jpg", "wb").write(r.content)
        image = nextcord.File("files/" + "image.jpg")
        await ctx.send(file=image)
        os.remove("files/image.jpg")
        await message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(animal(bot))
