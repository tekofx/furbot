import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from pyrae import dle
from core.bot import Bot
import datetime
from ui.Modal import Modal

class Utils(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(name="ping")
    async def ping(self, interaction: Interaction):
        """Comprobar si el bot está online"""
        await interaction.send("Pim pam trucu trucu")
        
        
    @nextcord.slash_command(name="votacion")
    async def votacion(
        self,
        interaction: Interaction,
    ):
        """Crea una votacion

        """
        await interaction.response.send_modal(Modal())

    @nextcord.slash_command(name="rae")
    async def rae(self, interaction: Interaction, palabra: str):
        """Define una palabra"""

        msg = await interaction.send("Buscando en la RAE")

        output = str(dle.search_by_word(palabra))

        if "«Diccionario de la lengua española»" in output:
            await msg.edit(content="Termino no encontrado")
        else:
            await msg.edit(content=output)

    @nextcord.slash_command(name="cumple")
    async def birthday(self, interaction: Interaction):
        pass

    @birthday.subcommand(name="añadir")
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
        self.bot.db.set_user_birthday(interaction.user, birth_date)
        await interaction.send("Cumpleaños guardado en la base de datos")

    @birthday.subcommand(name="ver")
    async def birthday_get(self, interaction: Interaction, usuario: nextcord.Member):

        user=self.bot.db.get_user(usuario)
        cumple=user[4]
        if not cumple:
            await interaction.send(
                f"No existe el cumpleaños de {usuario.display_name} en la base de datos"
            )
            return
        await interaction.send(
            f"El cumpleaños de {usuario.display_name} es el {cumple.day}-{cumple.month}-{cumple.year}"
        )


def setup(bot: commands.Bot):
    bot.add_cog(Utils(bot))
