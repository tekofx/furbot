import nextcord
from nextcord.ext import commands
import random
from utils.bot import Bot
from nextcord import Interaction

test_guild = 0


class fun(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="penis",
        description="Buena tula",
    )
    async def penis(self, interaction: Interaction, usuario: nextcord.Member = None):
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

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="communist",
        description="Serás un comunista bolivariano que apoya al Coletas?",
    )
    async def communist(
        self, interaction: Interaction, usuario: nextcord.Member = None
    ):
        num = random.randint(0, 100)

        output = "{} es {}% comunista"

        if usuario is None:
            usuario = interaction.user.mention
        else:
            usuario = usuario.mention

        await interaction.send(output.format(usuario, num))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="capitalist",
        description="Serás capitalista y te convertirás en el nuevo lobo de Wall Street?",
    )
    async def capitalist(
        self, interaction: Interaction, usuario: nextcord.Member = None
    ):
        num = random.randint(0, 100)

        output = "{} es {}% capitalista"

        if usuario is None:
            usuario = interaction.user.mention
        else:
            usuario = usuario.mention

        await interaction.send(output.format(usuario, num))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="gay",
        description="Maricon el ultimo",
    )
    async def gay(self, interaction: Interaction, usuario: nextcord.Member = None):
        num = random.randint(0, 100)

        output = "{} es {}% gay"

        if usuario is None:
            usuario = interaction.user.mention
        else:
            usuario = usuario.mention

        await interaction.send(output.format(usuario, num))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="str8",
        description="Super str8 el ultimo",
    )
    async def straight(self, interaction: Interaction, usuario: nextcord.Member = None):
        num = random.randint(0, 100)

        output = "{} es {}% gay"

        if usuario is None:
            usuario = interaction.user.mention
        else:
            usuario = usuario.mention

        await interaction.send(output.format(usuario, num))


def setup(bot: commands.Bot):
    bot.add_cog(fun(bot))
