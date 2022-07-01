import logging
from nextcord.ext import commands
from utils.database import check_record_in_database, create_record
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
            ctx.guild, username, num, "animal"
        )
        for tweet in tweet_images_urls:
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
        message = await ctx.send("Buscando fotos de lagartitos")
        await self.send_animal_pics_twitter(ctx, "HourlyLizards", num)
        await message.delete()

    @commands.command()
    async def cat(self, ctx: commands.Context, num: int = None):
        """Fotos de gatitos"""
        message = await ctx.send("Buscando fotos de gatitos")
        await self.send_animal_pics_twitter(ctx, "HourlyCats", num)
        await message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(animal(bot))
