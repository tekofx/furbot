import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from pyrae import dle
from core.bot import Bot
from core.database import set_birthday, get_birthday
import datetime


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

    @nextcord.slash_command(name="birthday")
    async def birthday(self, interaction: Interaction):
        pass

    @birthday.subcommand(name="add")
    async def birthday_add(
        self, interaction: Interaction, dia: int, mes: int, año: int
    ):
        """Añade tu cumpleaños al bot para que te felicite

        Args:
            dia (int): del 1 al 31
            mes (int): del 1 al 12
            año (int): numero de 4 digitos

        """

        birth_date = datetime.date(año, mes, dia)
        set_birthday(interaction.guild, interaction.user, birth_date)
        await interaction.send("Cumpleaños guardado en la base de datos")

    @birthday.subcommand(name="get")
    async def birthday_get(self, interaction: Interaction, usuario: nextcord.Member):

        cumple = get_birthday(interaction.guild, usuario)
        await interaction.send(
            f"El cumpleaños de {usuario.display_name} es el {cumple.day}-{cumple.month}-{cumple.year}"
        )


def setup(bot: commands.Bot):
    bot.add_cog(core(bot))
