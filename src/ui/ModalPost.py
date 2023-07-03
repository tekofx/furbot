from typing import Any, Coroutine
import nextcord
from core.bot import Bot
from nextcord.interactions import Interaction
class MastodonModal(nextcord.ui.Modal):
    def __init__(self,bot:Bot) -> None:
        super().__init__("Crear post de Mastodon")
        self.bot=bot
        self.canal=nextcord.ui.ChannelSelect(placeholder="Selecciona el canal")
        self.cuenta=nextcord.ui.TextInput(label="Cuenta",placeholder="Escribe el usuario de la cuenta",required=True)
        self.instancia=nextcord.ui.TextInput(label="Instancia",placeholder="Escribe la instancia del usuario",required=True)
        self.visibilidad=nextcord.ui.StringSelect(placeholder="Selecciona la visibilidad",options=[nextcord.SelectOption(label="SFW",value="sfw"),nextcord.SelectOption(label="NSFW",value="nsfw")])
        self.intervalo=nextcord.ui.TextInput(label="Intervalo",placeholder="Escribe cada cuantos minutos enviar un post de mastodon",required=True)
        
        self.add_item(self.canal)
        self.add_item(self.cuenta)
        self.add_item(self.instancia)
        self.add_item(self.visibilidad)
        self.add_item(self.intervalo)
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, None]:
        print(0)
        account=self.cuenta.value+"@"+self.instancia.value
        canal=self.canal.values[0]
        print(1)
        visibilidad=self.visibilidad.values[0]
        print(2)
        intervalo=int(self.intervalo.value)
        print(3)
        if not self.canal.permissions_for(interaction.guild.me).send_messages:
            await interaction.send(
                "No tengo permisos para enviar mensajes en este canal."
            )
            return
        if not self.bot.mastodon.exists_account(self.cuenta.value,self.instancia.value):
            await interaction.response.send_message("La cuenta no existe")
            return
        
        if self.bot.db.exists_post(canal,"mastodon",account):
            await interaction.response.send_message(f"Ya existe un post con la cuenta {account} en el canal {self.canal.value.mention}")
            return
        post_id=self.bot.db.insert_post(canal.id,visibilidad,"mastodon",account,intervalo)
          # Get tasks cog and create task
        tasks = self.bot.cogs.get("Tasks")

        task = self.bot.loop.create_task(
            tasks.post_task(
                interaction.guild,canal.id, visibilidad, "mastodon", account, intervalo
            )
        )
        
        # Add task to tasks dict
        self.bot.tasks[post_id] = task
        
        await interaction.response.send_message(f"Se ha creado un post con la cuenta {account} en el canal {self.canal.value.mention}")