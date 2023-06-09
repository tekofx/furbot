from nextcord.ext import commands
from core.bot import Bot
from core import logger
import nextcord
from nextcord import Interaction
import os

log = logger.getLogger(__name__)


class Animal(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send_animal_pics_twitter(
        self, interaction: Interaction, username: str, num: int
    ):
        if num is None:
            num = 1
        # Get images
        tweet_images_urls = self.bot.twitter.get_latest_images_not_repeated(
            interaction.guild, username, num, "animal"
        )
        for tweet in tweet_images_urls:
            await interaction.send(tweet)
            
    @nextcord.slash_command(name="animal")
    async def animal(self, interaction: Interaction):
        pass

    @animal.subcommand(name="zorro")
    async def fox(self, interaction: Interaction, num: int = None):
        """Fotos de zorros hermosos"""
        await self.send_animal_pics_twitter(interaction, "hourlyFox", num)

    @animal.subcommand(name="zoro_artico")
    async def arctic_fox(self, interaction: Interaction, num: int = None):
        """Fotos de zorros articos

        Args:
            num (int, optional): numero de fotos
        """
        await self.send_animal_pics_twitter(interaction, "DailyArcticFox", num)

    @animal.subcommand(name="lobo")
    async def wolf(self, interaction: Interaction, num: int = None):
        """Fotos de lobetes

        Args:
            num (int, optional): numero de fotos
        """
        await self.send_animal_pics_twitter(interaction, "hourlywolvesbot", num)

    @animal.subcommand(name="pajaro")
    async def bird(self, interaction: Interaction, num: int = None):
        """Fotos de pajaros

        Args:
            num (int, optional): numero de fotos
        """
        await self.send_animal_pics_twitter(interaction, "kerrybv1", num)

    @animal.subcommand(name="paloma")
    async def pigeon(self, interaction: Interaction, num: int = None):
        """Fotos de palomas

        Args:
            num (int, optional): numero de fotos
        """
        await self.send_animal_pics_twitter(interaction, "a_london_pigeon", num)

    @animal.subcommand(name="lagarto")
    async def lizard(self, interaction: Interaction, num: int = None):
        """Fotos de lagartitos

        Args:
            num (int, optional): numero de fotos
        """
        await self.send_animal_pics_twitter(interaction, "HourlyLizards", num)

    @animal.subcommand(name="gato")
    async def cat(self, interaction: Interaction, num: int = None):
        """Fotos de gatitos

        Args:
            num (int, optional): numero de fotos
        """
        await self.send_animal_pics_twitter(interaction, "HourlyCats", num)


def setup(bot: commands.Bot):
    bot.add_cog(Animal(bot))
