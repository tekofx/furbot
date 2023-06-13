from nextcord.ext import commands
from core.bot import Bot
from core import logger
import nextcord
from nextcord import Interaction
import os
from nextcord import Interaction, SlashOption
log = logger.getLogger(__name__)


animals={"Zorro":"hourlyFox", "Zorro Ártico":"DailyArcticFox", "Lobo":"hourlywolvesbot", "Pájaro":"kerrybv1", "Paloma":"a_london_pigeon", "Lagarto":"HourlyLizards", "Gato":"HourlyCats"}
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
    async def animal(self, interaction: Interaction, animal: str = SlashOption(
            name="animal", required=True, choices=animals
        ),num:int=None):
        """Fotos de animales

        Args:
            animal (str): Animal a buscar
            num (int, optional): Numero de fotos.
        """
        await self.send_animal_pics_twitter(interaction, animal, num)



def setup(bot: commands.Bot):
    bot.add_cog(Animal(bot))
