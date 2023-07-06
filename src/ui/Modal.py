from typing import Any, Coroutine
import nextcord
from nextcord.interactions import Interaction
emojis = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪", "🟫", "⬜"]
class Modal(nextcord.ui.Modal):
    def __init__(self, num_options:int) -> None:
        super().__init__("Votacion")
        
        self.num_options=num_options
        
        self.titulo=nextcord.ui.TextInput(label="Titulo",placeholder="Escribe el titulo de la votacion",required=True)
        self.add_item(self.titulo)
        self.descripcion=nextcord.ui.TextInput(label="Descripcion",placeholder="Escribe la descripcion de la votacion",required=True)
        self.add_item(self.descripcion)
        self.options=[]
        for x in range(0,num_options):
            option=nextcord.ui.TextInput(label=f"Opcion {x}",placeholder=f"Escribe la opcion {x}",required=True)
            self.options.append(option)
            self.add_item(option)
        
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, None]:
        embed=nextcord.Embed(title=self.titulo.value)
        embed.description=self.descripcion.value
        for x in self.options:
            i=self.options.index(x)
            embed.add_field(name=f"Opción {emojis[i]}",value=x.value)      
            
        msg=await interaction.response.send_message(embed=embed)
        msg=await msg.fetch()
        for x in self.options:
            i=self.options.index(x)
            await msg.add_reaction(emojis[i])
        