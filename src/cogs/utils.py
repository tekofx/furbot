import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from pyrae import dle
from utils.bot import Bot

test_guild = 0


class utils(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="ping",
        description="Comprobar si el bot está online",
    )
    async def ping(self, interaction: Interaction):
        await interaction.send("Pim pam trucu trucu")

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="rae",
        description="Comprobar si el bot está online",
    )
    async def rae(self, interaction: Interaction, palabra: str):

        msg = await interaction.send("Buscando en la RAE")

        output = str(dle.search_by_word(palabra))

        if "«Diccionario de la lengua española»" in output:
            await msg.edit(content="Termino no encontrado")
        else:
            await msg.edit(content=output)


def setup(bot: commands.Bot):
    bot.add_cog(utils(bot))
