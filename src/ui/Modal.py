from typing import Any, Coroutine, Optional
import nextcord
from nextcord.interactions import Interaction
from nextcord.utils import MISSING
class Modal(nextcord.ui.Modal):
    def __init__(self, ) -> None:
        super().__init__("Votacion")
        
        self.titulo="Votacion"
        
        
        
        self.opcion1=nextcord.ui.TextInput(label="Opcion 1",placeholder="Escribe la opcion 1")
        self.opcion2=nextcord.ui.TextInput(label="Opcion 2",placeholder="Escribe la opcion 2")
        self.opcion3=nextcord.ui.TextInput(label="Opcion 3",placeholder="Escribe la opcion 3")
        self.opcion4=nextcord.ui.TextInput(label="Opcion 4",placeholder="Escribe la opcion 4")
        
        self.add_item(self.opcion1)
        self.add_item(self.opcion2)
        self.add_item(self.opcion3)
        self.add_item(self.opcion4)
        
        self.aceptar=nextcord.ui.Button(label="Aceptar",style=nextcord.ButtonStyle.green)
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, None]:
        text=f"Opción 1: {self.opcion1.value}\nOpción 2: {self.opcion2.value}\nOpción 3: {self.opcion3.value}\nOpción 4: {self.opcion4.value}"
        
        return interaction.response.send_message(text)
        