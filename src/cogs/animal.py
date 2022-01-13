import logging
import nextcord
from nextcord.ext import commands
import os
import requests
from utils.functions import write_in_file
from utils.bot import Bot
from utils.data import resources_path


log = logging.getLogger(__name__)

animal_history_txt = resources_path + "animal_history.txt"


class animal(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def fox(self, ctx: commands.Context):
        """Fotos de zorros hermosos"""
        message = await ctx.send("Buscando fotos de zorros hermosos")
        with ctx.typing():

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image_not_repeated(
                "hourlyFox", animal_history_txt
            )

            # Write in history
            write_in_file(animal_history_txt, tweet_image_url + "\n")

            # Download image
            r = requests.get(tweet_image_url, allow_redirects=True)
            open("files/" + "image.jpg", "wb").write(r.content)

        image = nextcord.File("files/" + "image.jpg")
        await ctx.send(file=image)
        os.remove("files/image.jpg")
        await message.delete()

    @commands.command(name="arctic")
    async def arctic_fox(self, ctx: commands.Context):
        """Fotos de zorros articos"""
        message = await ctx.send("Buscando fotos de zorros árticos hermosos")
        with ctx.typing():

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image_not_repeated(
                "DailyArcticFox", animal_history_txt
            )

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
        message = await ctx.send("Buscando fotos de lobos lobitos lobones")
        with ctx.typing():

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image_not_repeated(
                "hourlywolvesbot", animal_history_txt
            )

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
        message = await ctx.send("Buscando fotos de pajaritos")
        with ctx.typing():

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image_not_repeated(
                "eugeniogarciac2", animal_history_txt
            )

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
        message = await ctx.send("Buscando fotos de palomas")
        with ctx.typing():

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image_not_repeated(
                "a_london_pigeon", animal_history_txt
            )

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
