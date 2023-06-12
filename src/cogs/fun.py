import nextcord
from nextcord.ext import commands
import random
from core.bot import Bot
from nextcord import Interaction
import os


class fun(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(name="pene")
    async def penis(self, interaction: Interaction, usuario: nextcord.Member = None):
        """Muestra tu tamaño de tula o el de otro"""
        num = random.randint(1, 15)
        output = "El pene de {}\n"
        if usuario is None:
            usuario = interaction.user.mention
        else:
            usuario = usuario.mention

        output += "8"
        for x in range(num):
            output += "="
        output += "D"
        await interaction.send(output.format(usuario))

    @nextcord.slash_command(name="comunista")
    async def communist(
        self, interaction: Interaction, usuario: nextcord.Member = None
    ):
        """Comprueba si eres comunista"""
        num = random.randint(0, 100)

        output = "{} es {}% comunista"

        if usuario is None:
            usuario = interaction.user.mention
        else:
            usuario = usuario.mention

        await interaction.send(output.format(usuario, num))
        
    @nextcord.slash_command(name="femboy")
    async def femboy(
        self, interaction: Interaction, usuario: nextcord.Member = None
    ):
        """Eres femboy?"""
        num = random.randint(0, 100)

        output = "{} es {}% femboy"

        if usuario is None:
            usuario = interaction.user.mention
        else:
            usuario = usuario.mention

        await interaction.send(output.format(usuario, num))

    @nextcord.slash_command(name="capitalista")
    async def capitalist(
        self, interaction: Interaction, usuario: nextcord.Member = None
    ):
        """Eres capitalista?"""
        num = random.randint(0, 100)

        output = "{} es {}% capitalista"

        if usuario is None:
            usuario = interaction.user.mention
        else:
            usuario = usuario.mention

        await interaction.send(output.format(usuario, num))

    @nextcord.slash_command(name="gay")
    async def gay(self, interaction: Interaction, usuario: nextcord.Member = None):
        """Eri gei?"""
        num = random.randint(0, 100)

        output = "{} es {}% gay"

        if usuario is None:
            usuario = interaction.user.mention
        else:
            usuario = usuario.mention

        await interaction.send(output.format(usuario, num))

    @nextcord.slash_command(name="hetero")
    async def straight(self, interaction: Interaction, usuario: nextcord.Member = None):
        """Hetero"""
        num = random.randint(0, 100)

        output = "{} es {}% hetero"

        if usuario is None:
            usuario = interaction.user.mention
        else:
            usuario = usuario.mention

        await interaction.send(output.format(usuario, num))


def setup(bot: commands.Bot):
    bot.add_cog(fun(bot))
