from nextcord.ext import commands
from utils.bot import Bot
from utils import logger
import nextcord
from nextcord import Interaction
import os

log = logger.getLogger(__name__)
local_guild = os.getenv("LOCAL_GUILD")


class animal(commands.Cog):
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

    @nextcord.slash_command(
        guild_ids=[local_guild],
        name="fox",
        description="Fotos de zorros hermosos",
    )
    async def fox(self, interaction: Interaction, num: int = None):
        """Fotos de zorros hermosos"""
        await self.send_animal_pics_twitter(interaction, "hourlyFox", num)

    @nextcord.slash_command(
        guild_ids=[local_guild],
        name="arctic_fox",
        description="Fotos de zorros articos",
    )
    async def arctic_fox(self, interaction: Interaction, num: int = None):
        await self.send_animal_pics_twitter(interaction, "ArcticHourly", num)

    @nextcord.slash_command(
        guild_ids=[local_guild],
        name="wolf",
        description="Fotos de lobetes",
    )
    async def wolf(self, interaction: Interaction, num: int = None):
        await self.send_animal_pics_twitter(interaction, "hourlywolvesbot", num)

    @nextcord.slash_command(
        guild_ids=[local_guild],
        name="bird",
        description="Fotos de pajaros",
    )
    async def bird(self, interaction: Interaction, num: int = None):
        await self.send_animal_pics_twitter(interaction, "kerrybv1", num)

    @nextcord.slash_command(
        guild_ids=[local_guild],
        name="pigeon",
        description="Fotos de palomas",
    )
    async def pigeon(self, interaction: Interaction, num: int = None):
        await self.send_animal_pics_twitter(interaction, "a_london_pigeon", num)

    @nextcord.slash_command(
        guild_ids=[local_guild],
        name="lizard",
        description="Fotos de lagartitos",
    )
    async def lizard(self, interaction: Interaction, num: int = None):
        await self.send_animal_pics_twitter(interaction, "HourlyLizards", num)

    @nextcord.slash_command(
        guild_ids=[local_guild],
        name="cat",
        description="Fotos de gatitos",
    )
    async def cat(self, interaction: Interaction, num: int = None):
        await self.send_animal_pics_twitter(interaction, "HourlyCats", num)


def setup(bot: commands.Bot):
    bot.add_cog(animal(bot))
