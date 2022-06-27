import io
import logging
import nextcord
from nextcord.ext import commands
import os
import requests
from utils.database import check_record_in_database, create_connection, create_record
from utils.bot import Bot


log = logging.getLogger(__name__)
temp_image = "image.jpg"


class animal(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send_animal_pics_twitter(
        self, ctx: commands.Context, username: str, num: int
    ):
        if num is None:
            num = 1

        # Get images
        tweet_images_urls = self.bot.twitter.get_latest_images_not_repeated(
            ctx.guild, username, num
        )
        for tweet in tweet_images_urls:

            # Write in history
            create_record(ctx.guild, ["twitter", tweet])
            await ctx.send(tweet)

    @commands.command()
    async def fox(self, ctx: commands.Context, num: int = None):
        """Fotos de zorros hermosos"""
        message = await ctx.send("Buscando fotos de zorros hermosos")
        await self.send_animal_pics_twitter(ctx, "hourlyFox", num)
        await message.delete()

    @commands.command(name="arctic")
    async def arctic_fox(self, ctx: commands.Context, num: int = None):
        """Fotos de zorros articos"""
        message = await ctx.send("Buscando fotos de zorros árticos hermosos")
        await self.send_animal_pics_twitter(ctx, "DailyArcticFox", num)
        await message.delete()

    @commands.command()
    async def wolf(self, ctx: commands.Context, num: int = None):
        """Fotos de lobetes"""
        message = await ctx.send("Buscando fotos de lobos lobitos lobones")
        await self.send_animal_pics_twitter(ctx, "hourlywolvesbot", num)
        await message.delete()

    @commands.command()
    async def bird(self, ctx: commands.Context, num: int = None):
        """Fotos de pajaros"""
        message = await ctx.send("Buscando fotos de pajaritos")
        await self.send_animal_pics_twitter(ctx, "kerrybv1", num)
        await message.delete()

    @commands.command()
    async def pigeon(self, ctx: commands.Context, num: int = None):
        """Fotos de palomas"""
        message = await ctx.send("Buscando fotos de palomas")
        await self.send_animal_pics_twitter(ctx, "a_london_pigeon", num)
        await message.delete()

    @commands.command()
    async def lizard(self, ctx: commands.Context, num: int = None):
        """Fotos de lagartitos"""
        message = await ctx.send("Buscando fotos de laganitos")
        await self.send_animal_pics_twitter(ctx, "HourlyLizards", num)
        await message.delete()

    @commands.command()
    async def cat(self, ctx: commands.Context, num: int = None):
        """Fotos de gatitos"""
        message = await ctx.send("Buscando fotos de gatitos")

        if num is None:
            num = 1

        aux = 0

        with ctx.typing():

            # Get pics from reddit
            reddit_image_urls = await self.bot.reddit.get_hot_subreddit_images(
                "catpictures", 50, num
            )

            # Select pic
            for x in reddit_image_urls:
                if aux == num:
                    break

                if not check_record_in_database(ctx.guild, x):
                    aux += 1

                    # Write in history
                    create_record(ctx.guild, ["reddit", x])

                    # Download image
                    await ctx.send(x)
        await message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(animal(bot))
