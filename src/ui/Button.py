from typing import Optional
import nextcord
from nextcord import Interaction
from core.bot import Bot
class Button(nextcord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value=None
        
    @nextcord.ui.button(label="Enviar otra imagen",style=nextcord.ButtonStyle.primary,emoji="➕")
    async def mas(self,button:nextcord.ui.Button,interaction:Interaction):
        await interaction.response.defer()
        self.value=True
        self.stop()
        