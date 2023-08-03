from typing import Any, Coroutine
import nextcord
from nextcord.interactions import Interaction

class SendMessageButton(nextcord.ui.View):
    def __init__(self,bot):
        super().__init__()
        self.bot=bot
    
    @nextcord.ui.button(label="Abrir modal", style=nextcord.ButtonStyle.primary)
    async def open_modal(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = ErrorModal(self.bot)
        await interaction.response.send_message("Completa los campos", view=modal, ephemeral=True)


class ErrorModal(nextcord.ui.Modal):
    def __init__(self,bot) -> None:
        super().__init__("Notificar un error al desarrollador")
        self.bot=bot
        print(1)
        
        self.titulo=nextcord.ui.TextInput(label="Titulo",placeholder="Escribe brevemente el error ocurrido",required=True)
        print(2)
        self.add_item(self.titulo)
        self.descripcion=nextcord.ui.TextInput(label="Descripcion",placeholder="Describe el error",required=True)
        self.add_item(self.descripcion)
        print(3)
        
        
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, None]:
        print(self.titulo.value)
        print(self.descripcion.value)
        embed=nextcord.Embed(title=self.titulo.value,description=self.descripcion.value,type="rich")
        print(4)
        owner=await self.bot.fetch_user(self.bot.owner_id)
        await owner.send(embed=embed)
        
        await interaction.send("Mensaje de error enviado al desarrollador")
            
        
        