import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from pyrae import dle
from core.bot import Bot
import os


class core(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(name="ping")
    async def ping(self, interaction: Interaction):
        """Comprobar si el bot está online"""
        await interaction.send("Pim pam trucu trucu")

    @nextcord.slash_command(name="rae")
    async def rae(self, interaction: Interaction, palabra: str):
        """Define una palabra"""

        msg = await interaction.send("Buscando en la RAE")

        output = str(dle.search_by_word(palabra))

        if "«Diccionario de la lengua española»" in output:
            await msg.edit(content="Termino no encontrado")
        else:
            await msg.edit(content=output)


def setup(bot: commands.Bot):
    bot.add_cog(core(bot))
