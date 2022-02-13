import logging
import nextcord
from nextcord.ext import commands
import os
import requests
from utils.database import create_connection, create_record
from utils.bot import Bot
from utils.data import resources_path, temp_path


log = logging.getLogger(__name__)
temp_image = "image.jpg"


class animal(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def fox(self, ctx: commands.Context):
        """Fotos de zorros hermosos"""
        message = await ctx.send("Buscando fotos de zorros hermosos")
        con = create_connection(str(ctx.guild.id))

        with ctx.typing():

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image_not_repeated(
                "hourlyFox", con
            )

            # Write in history
            create_record(con, ["twitter", tweet_image_url])

            # Download image
            r = requests.get(tweet_image_url, allow_redirects=True)
            open(temp_path + temp_image, "wb").write(r.content)

        image = nextcord.File(temp_path + temp_image)
        await ctx.send(file=image)
        os.remove(temp_path + temp_image)
        await message.delete()

    @commands.command(name="arctic")
    async def arctic_fox(self, ctx: commands.Context):
        """Fotos de zorros articos"""
        message = await ctx.send("Buscando fotos de zorros árticos hermosos")
        con = create_connection(str(ctx.guild.id))

        with ctx.typing():

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image_not_repeated(
                "DailyArcticFox", con
            )

            # Write in history
            create_record(con, ["twitter", tweet_image_url])

            # Download image
            r = requests.get(tweet_image_url, allow_redirects=True)
            open(temp_path + temp_image, "wb").write(r.content)
        image = nextcord.File(temp_path + temp_image)
        await ctx.send(file=image)
        os.remove(temp_path + temp_image)
        await message.delete()

    @commands.command()
    async def wolf(self, ctx: commands.Context):
        """Fotos de lobetes"""
        message = await ctx.send("Buscando fotos de lobos lobitos lobones")
        con = create_connection(str(ctx.guild.id))

        with ctx.typing():

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image_not_repeated(
                "hourlywolvesbot", con
            )

            # Write in history
            create_record(con, ["twitter", tweet_image_url])

            # Download image
            r = requests.get(tweet_image_url, allow_redirects=True)
            open(temp_path + temp_image, "wb").write(r.content)
        image = nextcord.File(temp_path + temp_image)
        await ctx.send(file=image)
        os.remove(temp_path + temp_image)
        await message.delete()

    @commands.command()
    async def bird(self, ctx: commands.Context):
        """Fotos de pajaros"""
        message = await ctx.send("Buscando fotos de pajaritos")
        con = create_connection(str(ctx.guild.id))

        with ctx.typing():

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image_not_repeated(
                "eugeniogarcia2", con
            )

            # Write in history
            create_record(con, ["twitter", tweet_image_url])

            # Download image
            r = requests.get(tweet_image_url, allow_redirects=True)
            open(temp_path + temp_image, "wb").write(r.content)
        image = nextcord.File(temp_path + temp_image)
        await ctx.send(file=image)
        os.remove(temp_path + temp_image)
        await message.delete()

    @commands.command()
    async def pigeon(self, ctx: commands.Context):
        """Fotos de palomas"""
        message = await ctx.send("Buscando fotos de palomas")
        con = create_connection(str(ctx.guild.id))

        with ctx.typing():

            # Image url
            tweet_image_url = self.bot.twitter.get_latest_image_not_repeated(
                "a_london_pigeon", con
            )

            # Write in history
            create_record(con, ["twitter", tweet_image_url])

            # Download image
            r = requests.get(tweet_image_url, allow_redirects=True)
            open(temp_path + temp_image, "wb").write(r.content)
        image = nextcord.File(temp_path + temp_image)
        await ctx.send(file=image)
        os.remove(temp_path + temp_image)
        await message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(animal(bot))
