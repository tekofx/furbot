from typing import List
from nextcord.ext import commands
import nextcord

from ui.Modal import Modal
from asyncio import sleep
from core.bot import Bot
from core import logger
from nextcord.ext import application_checks
from nextcord import Interaction, SlashOption


log = logger.getLogger(__name__)
PREDEFINED_CHANNELS = dict(
    {
        "General: Canal para enviar mensajes generales":"general",
        "Audit: Canal para que los administradores vean mensajes del estado y las acciones que realizo.":"audit",
        "Lobby: Canal para mandar mensajes de bienvenida":"lobby",
        "Games: Para mandar juegos que estén gratis":"games",
        "Wordle: Canal para jugar a wordle":"wordle",
        "Numbers: Canal jugar a contar numeros":"numbers",
        "Ordure: Canal para enviar cosas bizarras":"ordure",
        "Memes: Canal para enviar memes del server": "memes",
    },
)


emojis = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪", "🟫", "⬜"]


class admin(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    ############################# Canales #####################################
    @nextcord.slash_command(name="canales")
    @application_checks.has_permissions(administrator=True)
    async def canales(self, interaction: Interaction):
        pass

    @canales.subcommand(name="mostrar")
    @application_checks.has_permissions(administrator=True)
    async def show_channels(self, interaction: Interaction):
        """[Admin] Muestra los canales configurados del servidor
        """        
        channels = self.bot.db.get_channels(interaction.guild)
        channels = list(channels)
        
        if channels==[]:
            return await interaction.send("No hay canales configurados")

        output = "Canal: tipo\n"
        for channel in channels:
            channel_id = channel[0]
            channel_type = channel[2]
            x = await self.bot.fetch_channel(channel_id)
            output += f"- {x.mention}: {channel_type}\n"
        await interaction.send(output)

    @application_checks.has_permissions(administrator=True)
    @canales.subcommand(name="configurar")
    async def channels_set_all(self, interaction: Interaction) -> None:
        """[Admin] Configurar todos los canales predefinidos del bot.
        Permite establecer canales que sirvan para una función específica. Por ejemplo el canal lobby da la bienvenida
        a los miembros nuevos. No se puede usar el mismo canal para dos funciones distintas.
        """

        await interaction.send(
            "Empezando configuración. Se le pedirá establecer varios canales. Si no quiere establecer un canal, escriba `skip`"
        )
        await sleep(2)
        for x, y in PREDEFINED_CHANNELS.items():
            await self.setup_channel(interaction, y, x)

        await interaction.channel.send("Configuración finalizada")
        
        
    ############################# Canal #####################################
    
    @nextcord.slash_command(name="canal")
    @application_checks.has_permissions(administrator=True)
    async def canal(self, interaction: Interaction):
        pass
    
    @application_checks.has_permissions(administrator=True)
    @canal.subcommand(name="establecer_tipo")
    async def channel_set_type(
        self,
        interaction: Interaction,
        canal: nextcord.TextChannel | nextcord.ForumChannel,
        tipo: str = SlashOption(name="tipo", choices=PREDEFINED_CHANNELS),
    ):
        """[Admin] Configura un canal predefinido del bot.

        Permite establecer canales que sirvan para una función específica. Por ejemplo el canal lobby da la bienvenida
        a los miembros nuevos

        Args:
            canal (nextcord.TextChannel): canal que configurar
            tipo (str): tipo del canal
        """
        if not tipo in self.get_channel_of_type_types():
            await interaction.send(
                "Canal no valido, el canal debe ser uno de los siguientes: `{}`".format(
                    ", ".join(self.get_channel_of_type_types())
                )
            )
            return
        
        if not self.bot.db.exists_channel(canal):
            self.bot.db.insert_channel(canal,tipo)
        else:
            self.bot.db.update_channel_type(canal,tipo)

        await interaction.send(
            "Canal {} configurado como {}".format(canal.mention, tipo)
        )
        return

    
    ############################# Post #####################################
    
    @nextcord.slash_command(name="post")
    @application_checks.has_permissions(administrator=True)
    async def post(self, interaction: Interaction):
        pass
    
    
   
    @application_checks.has_permissions(administrator=True)
    @post.subcommand(name="añadir")
    async def post_add(
        self,
        interaction: Interaction,
        canal: nextcord.TextChannel,
        servicio: str = SlashOption(
            name="servicio",
            description="Red social de la cuenta",
            required=True,
            choices={"Twitter": "twitter", "Reddit": "reddit","Mastodon":"mastodon","E621":"e621", "E926":"e926"},
        ),
        cuenta: str = SlashOption(name="cuenta", required=True),
        visibilidad: str = SlashOption(
            name="visibilidad", required=True, choices={"SFW": "sfw", "NSFW": "nsfw"}
        ),
        intervalo: int = SlashOption(required=False,min_value=5)
    ):
        """[Admin] Permite añadir una cuenta de twitter/subreddit/mastodon a un canal.
        De esta forma cada hora se publicará el último post de la cuenta en el canal. Si se añaden varias
        cuentas a la vez, se utilizará una cuenta aleatoria de las añadidas.

        Args:
            canal: canal al que enviar
            servicio: Red social. Twitter/Reddit/Mastodon
            cuenta: Cuenta de twitter, subreddit de Reddit o usuario@instancia de Mastodon
            visibilidad: Si/No. Si se quiere que se cojan los posts NSFW o no
            intervalo: Minutos entre un post y otro. Debe ser mayor a los 5 mins
        """

        if visibilidad == "nsfw" and not canal.nsfw:
            await interaction.send(
                "El canal no es NSFW, utiliza otro canal o cambia los permisos."
            )
            return

        if not canal.permissions_for(interaction.guild.me).send_messages:
            await interaction.send(
                "No tengo permisos para enviar mensajes en este canal."
            )
            return
        
        if servicio == "e621" and canal.nsfw==False:
            await interaction.send("No se puede usar e621 en un canal SFW")
            return

        if servicio == "reddit":
            exists = await self.bot.reddit.exists_subreddit(cuenta)
            if not exists:
                await interaction.send(
                    f"El subreddit {cuenta} no existe, comprueba el subreddit y vuelve a intentarlo"
                )
                return

        if servicio == "twitter":
            var = self.bot.twitter.exists_account(cuenta)

            if not var:
                await interaction.send(
                    f"La cuenta {cuenta} no existe, comprueba la cuenta y vuelve a intentarlo"
                )
                return
            
        if servicio =="mastodon":
            if not "@" in cuenta:
                return await interaction.send("La cuenta debe ser usuario@instancia")
            instance=cuenta.split("@")[1]
            usuario=cuenta.split("@")[0]
            var=self.bot.mastodon.exists_account(usuario,instance)
            if not var:
                await interaction.send(
                    f"La cuenta {cuenta} no existe, comprueba la cuenta y vuelve a intentarlo"
                )
                return
            
        if self.bot.db.exists_post(canal,servicio,cuenta):
            await interaction.send("El post ya existe, escoge otra cuenta o canal")
            return
        
        post_id=self.bot.db.insert_post(canal,visibilidad,servicio,cuenta,intervalo)
        await interaction.send("Post creado")

        # Get tasks cog and create task
        tasks = self.bot.cogs.get("Tasks")

        task = self.bot.loop.create_task(
            tasks.post_task(
                interaction.guild, canal.id, visibilidad, servicio, cuenta, intervalo
            )
        )
        
        # Add task to tasks dict
        self.bot.tasks[post_id] = task
    
    def check_fields(self,interaction:Interaction,canal:nextcord.TextChannel,servicio:str, cuenta:str,visibilidad: str = SlashOption(
            name="visibilidad", required=True, choices={"SFW": "sfw", "NSFW": "nsfw"})):
        
        if visibilidad == "nsfw" and not canal.nsfw:
            raise ValueError("El canal no es NSFW, utiliza otro canal o cambia los permisos.")

        if not canal.permissions_for(interaction.guild.me).send_messages:
            raise ValueError("No tengo permisos para enviar mensajes en este canal.")
        if self.bot.db.exists_post(canal,servicio,cuenta):
            raise ValueError("El post ya existe, escoge otra cuenta o canal")
        
    def create_task(self, interaction:Interaction, canal:nextcord.TextChannel,servicio:str,cuenta:str,visibilidad: str = SlashOption(
            name="visibilidad", required=True, choices={"SFW": "sfw", "NSFW": "nsfw"}), intervalo: int = SlashOption(required=False,min_value=5)):
        post_id=self.bot.db.insert_post(canal,visibilidad,servicio,cuenta,intervalo)

        # Get tasks cog and create task
        tasks = self.bot.cogs.get("Tasks")

        task = self.bot.loop.create_task(
            tasks.post_task(
                interaction.guild, canal.id, visibilidad, servicio, cuenta, intervalo
            )
        )
        
        # Add task to tasks dict
        self.bot.tasks[post_id] = task
        
    @application_checks.has_permissions(administrator=True)
    @post.subcommand(name="twitter")
    async def post_add_twitter(self,interaction: Interaction,
        canal: nextcord.TextChannel,
        cuenta: str = SlashOption(name="cuenta", required=True),
        visibilidad: str = SlashOption(
            name="visibilidad", required=True, choices={"SFW": "sfw", "NSFW": "nsfw"}
        ),
        intervalo: int=5):
        """[Admin] Programa un post de twitter
        De esta forma cada hora se publicará el último post de la cuenta en el canal. Si se añaden varias
        cuentas a la vez, se utilizará una cuenta aleatoria de las añadidas.

        Args:
            canal: canal al que enviar
            cuenta: Cuenta de twitter
            visibilidad: Si/No. Si se quiere que se cojan los posts NSFW o no
            intervalo: Minutos entre un post y otro. Debe ser mayor a los 5 mins
        """
        
        try:
            self.check_fields(interaction,canal,"twitter",cuenta,visibilidad)
        except ValueError as error:
            await interaction.send(error.args[0])
            return
            
            
        var = self.bot.twitter.exists_account(cuenta)

        if not var:
            await interaction.send(
                f"La cuenta {cuenta} no existe, comprueba la cuenta y vuelve a intentarlo"
            )
            return
        
        self.create_task(interaction,canal,"twitter",cuenta,visibilidad,intervalo)
        await interaction.send("Post creado")
        
    @application_checks.has_permissions(administrator=True)
    @post.subcommand(name="mastodon")
    async def post_add_mastodon(self,interaction: Interaction,
        canal: nextcord.TextChannel,
        usuario: str = SlashOption(name="usuario", required=True),
        instancia:str = SlashOption(name="instancia", required=True),
        visibilidad: str = SlashOption(
            name="visibilidad", required=True, choices={"SFW": "sfw", "NSFW": "nsfw"}
        ),
        intervalo: int=5):
        """[Admin] Programa un post de mastodon
        De esta forma cada hora se publicará el último post de la cuenta en el canal. Si se añaden varias
        cuentas a la vez, se utilizará una cuenta aleatoria de las añadidas.

        Args:
            canal: canal al que enviar
            usuario: Cuenta de mastodon
            visibilidad: Si/No. Si se quiere que se cojan los posts NSFW o no
            intervalo: Minutos entre un post y otro. Debe ser mayor a los 5 mins
        """
        
        cuenta=usuario+"@"+instancia
        
        try:
            self.check_fields(interaction,canal,"mastodon",cuenta,visibilidad)
        except ValueError as error:
            await interaction.send(error.args[0])
            return
        
        
        var=self.bot.mastodon.exists_account(usuario,instancia)
        if not var:
            await interaction.send(
                f"La cuenta {cuenta} no existe, comprueba la cuenta y vuelve a intentarlo"
            )
            return
        
        self.create_task(interaction,canal,"mastodon",cuenta,visibilidad,intervalo)
        await interaction.send("Post creado")
        
    @application_checks.has_permissions(administrator=True)
    @post.subcommand(name="reddit")
    async def post_add_reddit(self,interaction: Interaction,
        canal: nextcord.TextChannel,
        subreddit: str = SlashOption(name="subreddit", required=True),
        visibilidad: str = SlashOption(
            name="visibilidad", required=True, choices={"SFW": "sfw", "NSFW": "nsfw"}
        ),
        intervalo: int=5):
        """[Admin] Programa un post de reddit
        De esta forma cada hora se publicará el último post de la cuenta en el canal. Si se añaden varias
        cuentas a la vez, se utilizará una cuenta aleatoria de las añadidas.

        Args:
            canal: canal al que enviar
            subreddit: Subreddit de reddit
            visibilidad: Si/No. Si se quiere que se cojan los posts NSFW o no
            intervalo: Minutos entre un post y otro. Debe ser mayor a los 5 mins
        """
        try:
            self.check_fields(interaction,canal,"reddit",subreddit,visibilidad)
        except ValueError as error:
            await interaction.send(error.args[0])
            return
        
        
        exists = await self.bot.reddit.exists_subreddit(subreddit)
        if not exists:
            await interaction.send(
                f"El subreddit {subreddit} no existe, comprueba el subreddit y vuelve a intentarlo"
            )
            return
        
        self.create_task(interaction,canal,"twitter",subreddit,visibilidad,intervalo)
        await interaction.send("Post creado")
        
    @application_checks.has_permissions(administrator=True)
    @post.subcommand(name="e621")
    async def post_add_e621(self,interaction: Interaction,
        canal: nextcord.TextChannel,
        tags: str = SlashOption(name="tags", required=True),
        intervalo: int=5):
        """[Admin] Programa un post de e621
        De esta forma cada hora se publicará el último post de la cuenta en el canal. Si se añaden varias
        cuentas a la vez, se utilizará una cuenta aleatoria de las añadidas.

        Args:
            canal: canal al que enviar
            tags: Tags que buscar de e621. Separar las tags con comas. Para evitar posts con un tag concreto usar -tag
            visibilidad: Si/No. Si se quiere que se cojan los posts NSFW o no
            intervalo: Minutos entre un post y otro. Debe ser mayor a los 5 mins
        """
        
        try:
            self.check_fields(interaction,canal,"e621",tags,"nsfw")
        except ValueError as error:
            await interaction.send(error.args[0])
            return
        
        if canal.nsfw==False:
            await interaction.send("No se puede usar e621 en un canal SFW")
            return
        
        
        self.create_task(interaction,canal,"e621",tags,"nsfw",intervalo)
        await interaction.send("Post creado")
        
    @application_checks.has_permissions(administrator=True)
    @post.subcommand(name="e926")
    async def post_add_e926(self,interaction: Interaction,
        canal: nextcord.TextChannel,
        tags: str = SlashOption(name="tags", required=True),
        intervalo: int=5):
        """[Admin] Programa un post de e926
        De esta forma cada hora se publicará el último post de la cuenta en el canal. Si se añaden varias
        cuentas a la vez, se utilizará una cuenta aleatoria de las añadidas.

        Args:
            canal: canal al que enviar
            tags: Tags que buscar de e926. Separar las tags con comas. Para evitar posts con un tag concreto usar -tag
            visibilidad: Si/No. Si se quiere que se cojan los posts NSFW o no
            intervalo: Minutos entre un post y otro. Debe ser mayor a los 5 mins
        """
        
        try:
            self.check_fields(interaction,canal,"e926",tags,"sfw")
        except ValueError as error:
            await interaction.send(error.args[0])
            return
        
        
        self.create_task(interaction,canal,"e926",tags,"sfw",intervalo)
        await interaction.send("Post creado")
            

    @application_checks.has_permissions(administrator=True)
    @post.subcommand(name="eliminar")
    async def post_rm(self, interaction: Interaction, post_id: int):
        """[Admin] Permite eliminar un post 

        Args:
            post_id: id del post a eliminar
        """

        # Remove from db
        self.bot.db.remove_post(interaction.channel,post_id)

        # Cancel the task
        self.bot.tasks[post_id].cancel()

        # Remove from tasks dict
        del self.bot.tasks[post_id]
        
        await interaction.send("Post eliminado")

    @application_checks.has_permissions(administrator=True)
    @post.subcommand(name="lista")
    async def post_list(self, interaction: Interaction):
        """[Admin] Muestra los posts que se han añadido"""
        posts=self.bot.db.get_posts(interaction.guild)
        if not posts:
            await interaction.send("No hay posts para este servidor")
            return

        output = ""
        for post in posts:
            post_id,guild_id, channel_id, visibility, service, account, interval = post
            
            channel = await self.bot.fetch_channel(channel_id)
            output += f"-id={post_id}\n-canal={channel.mention}\n-visibilidad={visibility}\n-servicio={service}\n-cuenta={account} \n-intevalo={interval}m\n\n"

        await interaction.send(output)
        
    ############################## BORRAR ##############################

    @nextcord.slash_command(name="borrar")
    @application_checks.has_permissions(administrator=True)
    async def clear(self, interaction: Interaction, num: int):
        """[Admin] Elimina mensajes de un canal

        Args:
            num: Número de mensajes que borrar
        """

        messages_to_delete = []
        # If command is a reply to a message
        async for message in interaction.channel.history(limit=num + 1):
            messages_to_delete.append(message)

        await interaction.channel.delete_messages(messages_to_delete)
        message = await interaction.send("Eliminados {} mensajes".format(num))
        await sleep(5)
        await message.delete()

    async def fetch_channel_from_message_content(
        self, message: nextcord.Message
    ) -> nextcord.TextChannel:
        """Gets a channel from a message content

        Args:
            message (nextcord.Message): message to get the channel from

        Returns:
            nextcord.TextChannel: channel
        """

        channel_id = message.content.replace("<#", "").replace(">", "")
        try:
            channel = await self.bot.fetch_channel(channel_id)
        except nextcord.errors.Forbidden as error:
            log.error(
                "Don't have permissions to fetch channel {}: {}".format(
                    channel_id, error
                ),
                extra={"guild": message.guild.name},
            )
            raise error
        return channel

    async def setup_channel(
        self, interaction: Interaction, channel_type: str, channel_description: str
    ):
        def check(m: nextcord.Message) -> bool:
            return m.author == interaction.user and m.channel == interaction.channel

        # General channel
        await interaction.channel.send(
            "Seleccione el canal {}. {}".format(channel_type, channel_description)
        )
        msg = await self.bot.wait_for("message", check=check, timeout=60)
        if msg.content.lower() != "skip":
            try:
                channel = await self.fetch_channel_from_message_content(msg)
            except nextcord.errors.Forbidden:
                await interaction.channel.send(
                    "No tengo permisos para acceder a este canal."
                )
                return

            if not channel.permissions_for(interaction.guild.me).send_messages:
                await interaction.channel.send(
                    "No tengo permisos para enviar mensajes en este canal."
                )
                log.error(
                    "Don't have permissions to send messages in channel {}".format(
                        channel.id
                    ),
                    extra={"guild": interaction.guild.name},
                )
                return
            
            if not self.bot.db.exists_channel(channel):
                self.bot.db.insert_channel(channel,channel_type)
            else:
                self.bot.db.update_channel_type(channel,channel_type)

            await interaction.channel.send(
                "Canal {} añadido como {}".format(channel.mention, channel_type)
            )

    def get_channel_of_type_types(self) -> List[str]:
        """Gets the channel_types from CHANNEL

        Returns:
            List[str]: contains the channel_types
        """
        output = []
        for x in PREDEFINED_CHANNELS.values():
            output.append(x)

        return output

   


def setup(bot: commands.Bot):
    bot.add_cog(admin(bot))
