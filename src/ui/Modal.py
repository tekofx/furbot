from typing import Any, Coroutine, Optional
import nextcord
from nextcord.interactions import Interaction
from nextcord.utils import MISSING
class Modal(nextcord.ui.Modal):
    def __init__(self, ) -> None:
        super().__init__("Votacion")
        
        self.titulo="Votacion"
        
        self.opcion1=nextcord.ui.TextInput(label="Opcion 1",placeholder="Escribe la opcion 1",required=True)
        self.opcion2=nextcord.ui.TextInput(label="Opcion 2",placeholder="Escribe la opcion 2", required=True)
        self.opcion3=nextcord.ui.TextInput(label="Opcion 3",placeholder="Escribe la opcion 3",required=False)
        self.opcion4=nextcord.ui.TextInput(label="Opcion 4",placeholder="Escribe la opcion 4",required=False)
        
        self.add_item(self.opcion1)
        self.add_item(self.opcion2)
        self.add_item(self.opcion3)
        self.add_item(self.opcion4)
        
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, None]:
        embed=nextcord.Embed(title=self.titulo)
        embed.add_field(name="Opción 1",value=self.opcion1.value)      
        return await interaction.response.send_message(embed=embed,ephemeral=True)
        