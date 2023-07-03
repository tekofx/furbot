import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from pyrae import dle
from core.bot import Bot
import datetime
from ui.Modal import Modal
from ui.Button import Button

class Utils(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(name="ping")
    async def ping(self, interaction: Interaction):
        """Comprobar si el bot está online"""
        await interaction.send("Pim pam trucu trucu")
        
    @nextcord.slash_command(name="e621")
    async def e621(self, interaction:Interaction, tags:str):
        """Envia una imagen de e621 con los tags especificados.

        Args:
            tags (str): Tags de la imagen. Deben estar separados por espacios
        """
        if not interaction.channel.is_nsfw():
            await interaction.send("Este comando solo se puede usar en canales NSFW")
            return
        await self.send_e621_post(interaction,tags)
        
    async def send_e621_post(self,interaction:Interaction,tags:str):
        post=self.bot.e621.get_post_not_repeated(interaction.guild,tags)
        if post is None:
            await interaction.send("No se ha encontrado nada con esa/s tags. Comprueba que las tags existen")
            return
        button=Button()
        await interaction.send(post.file.url,view=button)
        await button.wait()
        if button.value is None:
            return
        if button.value:
            
            await self.send_e621_post(interaction,tags)
        
    @nextcord.slash_command(name="e926")
    async def e926(self, interaction:Interaction, tags:str):
        """Envia una imagen de e926 con los tags especificados.

        Args:
            tags (str): Tags de la imagen. Deben estar separados por espacios
        """
        await self.send_e926_post(interaction,tags)
    
            
    async def send_e926_post(self,interaction:Interaction,tags:str):
        post=self.bot.e926.get_post_not_repeated(interaction.guild,tags)
        if post is None:
            await interaction.send("No se ha encontrado nada con esa/s tags. Comprueba que las tags existen")
            return
        button=Button()
        await interaction.send(post.file.url,view=button)
        await button.wait()
        if button.value is None:
            return
        if button.value:
            await self.send_e926_post(interaction,tags)
        
        
    @nextcord.slash_command(name="avatar")
    async def avatar(self, interaction: Interaction, usuario: nextcord.Member):
        """Muestra el avatar de un usuario"""
        await interaction.send(usuario.avatar_url)
        
        
    @nextcord.slash_command(name="votacion")
    async def votacion(
        self,
        interaction: Interaction,
        opciones:int
    ):
        """Crea una votacion
        
        Args:
            opciones: Número de opciones entre las que votar

        """
        await interaction.response.send_modal(Modal(opciones))

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
        """Mira el cumpleaños de un usuario

        Args:
            usuario (nextcord.Member): Usuario del que ver el cumpleaños
        """

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
