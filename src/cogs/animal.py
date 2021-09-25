from discord.ext import commands
from functions import (
    get_hot_subreddit_image,
)

animal_history_txt = "files/resources/data/animal_history.txt"


class Animal(commands.Cog):
    """Fotos de animalitos"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fox(self, context):
        """Fotos de zorros hermosos -/////-

        Envia una foto de r/foxes
        """
        message = await context.channel.send("Buscando fotos de zorros hermosos")
        await context.channel.send(
            get_hot_subreddit_image("foxes", 100, animal_history_txt, "Pics!")
        )
        await message.delete()

    @commands.command()
    async def wolf(self, context):
        """Fotos de lobos lobitos lobones

        Envia una foto de r/wolves
        """
        message = await context.channel.send("Buscando fotos de lobos lobitos lobones")
        await context.channel.send(
            get_hot_subreddit_image("wolves", 100, animal_history_txt, "Pics")
        )
        await message.delete()


def setup(bot):
    bot.add_cog(Animal(bot))
