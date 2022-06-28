import nextcord
from nextcord.errors import Forbidden
from nextcord.ext import commands
import os
import yaml
import logging
from utils.database import (
    check_entry_in_database,
    check_record_in_database,
    create_record,
    create_user,
    exists_channel,
    get_channel,
    setup_database,
)
from utils.reddit import Reddit
from utils.twitter import Twitter
import requests
from utils.data import Data, config_yaml

log = logging.getLogger(__name__)
token = os.getenv("DISCORD_TOKEN")
MAX_JOIN_TIMES = 3


class Bot(commands.Bot):
    def __init__(self, token):
        intents = nextcord.Intents.default()
        intents.members = True
        intents.message_content = True
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

    async def new_github_release(self):
        "Checks if there is a new release on github and sends a message to the channel"
        r = requests.request(
            "GET", "https://api.github.com/repos/tekofx/furbot/releases"
        )
        r = r.json()
        version = r[0]["tag_name"]
        release_changelog = r[0]["body"]
        url = r[0]["html_url"]
        embed = nextcord.Embed(title="Nueva versión " + version, description=url)
        embed.set_thumbnail(
            url="https://raw.githubusercontent.com/tekofx/furbot/main/assets/furbot_logo.png"
        )
        release_changelog = release_changelog.replace("\r", "")
        release_changelog = release_changelog.split("#")
        for i in release_changelog:
            if i != "":
                i = i.splitlines()
                var = "\n".join(i[1:])
                embed.add_field(name=i[0], value=var, inline=False)
        for guild in self.guilds:
            if not exists_channel(guild, "bot_news"):
                continue

            if not check_record_in_database(guild, r[0]["url"]):
                create_record(guild, ["github", r[0]["url"]])

                await self.channel_send(guild, "bot_news", "a", embed)

    async def on_ready(self):
        """Performs an action when the bot is ready"""

        for guild in self.guilds:
            # Setup folders
            data = Data(guild)
            data.setup_folders()
            data.setup_files()
            del data

            # Setup database
            setup_database(guild)

        # Check if there is a new release on github
        await self.new_github_release()

        # Set activity
        with open(config_yaml, "r") as stream:
            try:
                content = yaml.safe_load(stream)
            except yaml.YAMLError as error:
                log.error("Error at getting YAML content: {}".format(error))

        activity = nextcord.Game(content["activity"])
        await self.change_presence(activity=activity, status=nextcord.Status.online)

        # Load cogs
        cogs = os.listdir("src/cogs/")

        for c in cogs:
            if c.endswith(".py"):
                self.load_extension("cogs." + c[:-3])
                log.info("Loaded {}".format(c))

        log.info("We have logged in as {}".format(self.user))

    async def on_member_join(self, member: nextcord.Member):
        # Message in lobby
        mensaje_lobby_usuario = """Bienvenid@ a {} {}. No olvides mirar el canal de normas y pasarlo bien""".format(
            member.guild.name, member.mention
        )
        mensaje_lobby_bot = "Se ha añadido el bot {}".format(member.mention)

        if not member.bot:
            await self.channel_send(member.guild, "lobby", mensaje_lobby_usuario)
        else:
            await self.channel_send(member.guild, "lobby", mensaje_lobby_bot)

        entry_in_database = check_entry_in_database(member.guild, "users", member.id)
        if not entry_in_database and not member.bot:
            # Add to database
            try:
                create_user(member.guild, [member.id, member.name, member.joined_at])
            except Exception as error:
                log.error("Error creating user on join: {}".format(error))
            else:
                log.info("Created user {} with id {}".format(member.name, member.id))

    async def on_member_remove(self, member: nextcord.Member):
        # When a user leaves a server
        mensaje_lobby_usuario = "{}({}) se fue, una pena. ".format(
            member.mention, member.name
        )
        mensaje_lobby_bot = "Se ha eliminado el bot {}({})".format(
            member.mention, member.name
        )

        if not member.bot:
            await self.channel_send(member.guild, "lobby", mensaje_lobby_usuario)
        else:
            await self.channel_send(member.guild, "lobby", mensaje_lobby_bot)

    def run(self):

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
            if message.content.lower() == "a" or message.content.lower() == "ª":
                msg = await message.channel.send("Cuidado con Thedax!")
                await msg.delete(delay=5)

        await self.process_commands(message)

    async def on_command(self, ctx):

        user = str(ctx.author)
        command = str(ctx.command)
        log.info(user + " used command " + command)

    async def channel_send(
        self,
        guild: nextcord.Guild,
        channel_type: str,
        msg: str,
        embed: nextcord.Embed = None,
    ):
        """Send message to a determinated channel

        Args:
            guild (nextcord.Guild): guild to send the message
            channel_type (str): determinated channel to send the message
            msg (str): message to send
            embed (nextcord.Embed, optional): Embed to send. Defaults to None.

        Raises:
            Forbidden: If the bot doesn't have permissions to send the message
        """

        # Get general_channel id
        general_id = get_channel(guild, channel_type)

        if general_id != 0:
            try:
                # Fetch general_channel
                general_channel = await self.fetch_channel(general_id)
            except Forbidden as error:
                log.error(
                    "Error getting {} channel from server {}: {}".format(
                        channel_type, guild, error
                    )
                )
                raise Forbidden

            # Send message
            if embed:
                await general_channel.send(embed=embed)
            else:
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
            bot_commands = []
            for command in self.commands:
                if command_used in command.name:
                    bot_commands.append(command.name)

            if len(bot_commands) > 0:
                output = "Igual quisiste usar: {}\n".format(",".join(bot_commands))
                await context.send(output)

        # Not admin access
        if isinstance(error, commands.CheckFailure):
            await context.send("Error: No tienes permiso para usar este comando")
