import nextcord
from nextcord.errors import Forbidden
from nextcord.ext import commands
import os
import yaml
import logging
from utils.database import (
    check_entry_in_database,
    create_connection,
    create_user,
    get_channel,
    setup_database,
)
from utils.reddit import Reddit
from utils.twitter import Twitter
from utils.data import resources_path

log = logging.getLogger(__name__)
token = os.getenv("DISCORD_TOKEN")
MAX_JOIN_TIMES = 3


class Bot(commands.Bot):
    def __init__(self, token):
        intents = nextcord.Intents.default()
        intents.members = True
        super().__init__(
            command_prefix=["fur ", "Fur ", "FUR "],
            description="uwu",
            intents=intents,
        )

        self.token = token
        self._twitter = Twitter()
        self._reddit = Reddit()

    @property
    def twitter(self) -> Twitter:
        return self._twitter

    @property
    def reddit(self) -> Reddit:
        return self._reddit

    @property
    def general_channel(self):
        return self._general_channel

    @property
    def memes_channel(self):
        return self._memes_channel

    @property
    def audit_channel(self):
        return self._audit_channel

    @property
    def lobby_channel(self):
        return self._lobby_channel

    @property
    def server(self):
        return self._server

    async def on_ready(self):
        """Performs an action when the bot is ready"""

        # Load cogs
        cogs = os.listdir("src/cogs/")

        for c in cogs:
            if c.endswith(".py"):
                self.load_extension("cogs." + c[:-3])
                log.info("Loaded {}".format(c))

        # Setup databases
        guilds = self.fetch_guilds()
        async for guild in guilds:

            server = str(guild.id)
            con = setup_database(server)

        log.info("We have logged in as {}".format(self.user))

    async def on_member_join(self, member: nextcord.Member):
        # Message in lobby
        mensaje_lobby = """Bienvenid@ a {} {}. No olvides mirar el canal de normas y pasarlo bien""".format(
            member.guild.name, member.mention
        )
        await self.channel_send(member.guild, "lobby", mensaje_lobby)

        con = create_connection(str(member.guild.id))
        entry_in_database = check_entry_in_database(con, "users", member.id)
        if not entry_in_database and member.bot:
            # Add to database
            author_id = member.id
            author_name = member.name

            user_data = [
                author_id,
                author_name,
                member.joined_at,
            ]
            try:
                create_user(con, user_data)
            except Exception as error:
                log.error("Error creating user on join: {}".format(error))
            else:
                log.info("Created user {} with id {}".format(author_name, author_id))
        await self.audit_channel.send("{} se ha unido".format(member.name))
        con.close()

    def run(self):
        # Set activity
        self.status = nextcord.Status.online

        # Get activity
        with open(resources_path + "config.yaml", "r") as stream:
            try:
                content = yaml.safe_load(stream)
            except yaml.YAMLError as error:
                log.error("Error at getting YAML content: {}".format(error))

        activity = nextcord.Game(content["activity"])
        self.activity = activity

        super().run(token=self.token)

    async def on_message(self, message: nextcord.Message):
        """Action performed for every message in channels/DM's
        Args:
            message ([nextcord.Message]): Message to check
        """
        if not message.author.bot:

            if message.content.lower() == "owo":
                await message.channel.send("OwO!")
            if "vaca " in message.content.lower():
                await message.channel.send("Muuu!")
            if "vacas " in message.content.lower():
                await message.channel.send("Muuu Muuu!")
            if message.content.lower() == "uwu":
                await message.channel.send("UwU!")
            if message.content.lower() == "7w7":
                await message.channel.send(":eyes:")
            if message.content.lower() == "ewe":
                await message.channel.send("EwE!")
            if message.content.lower() == "awa":
                await message.channel.send("AwA!")

        await self.process_commands(message)

    async def on_command(self, ctx):

        user = str(ctx.author)
        command = str(ctx.command)
        log.info(user + " used command " + command)

    async def channel_send(self, server_id: int, channel_type: str, msg: str):
        # Create database connection
        con = create_connection(str(server_id))

        # Get general_channel id
        general_id = get_channel(con, channel_type)
        con.close()

        if general_id != 0:
            try:
                # Fetch general_channel
                general_channel = await self.fetch_channel(general_id)
            except Forbidden as error:
                log.error(
                    "Error getting {} channel from server {}: {}".format(
                        channel_type, server_id, error
                    )
                )
                raise Forbidden

            # Send message
            await general_channel.send(msg)

    async def on_command_error(
        self, context: commands.Context, error: commands.CommandError
    ) -> None:
        """Checks error on commands
        Args:
            context ([type]): [Where the command was used]
            error ([type]): [Error of the command]
        """
        message_content = str(context.message.content)
        message_content = message_content.split(" ")
        command_used = message_content[1]

        if isinstance(error, commands.errors.UserInputError):
            log.error("UserInputError: {}".format(error))
            await context.send("Comprueba que la información introducida es correcta")

        # Argument missing
        if isinstance(error, commands.MissingRequiredArgument):
            await context.send("Error: Faltan parámetros")
            await context.send_help(self.get_command(command_used))

        # Command does not exist
        if isinstance(error, commands.CommandNotFound):
            await context.send(
                "Error: Comando no existente, escribe `fur help` para ver los comandos disponibles"
            )
            # Check if exists a similar command
            output = "Igual quisiste usar alguno de estos comandos:\n"
            for command in self.commands:
                if command_used in str(command):
                    output += str(command) + ", "
            if output != "Igual quisiste usar alguno de estos comandos:\n":
                await context.send(output)

        # Not admin access
        if isinstance(error, commands.CheckFailure):
            await context.send("Error: No tienes permiso para usar este comando")
