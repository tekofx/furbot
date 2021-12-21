import nextcord
from nextcord import activity
from nextcord.ext import commands, tasks
import os
from pathlib import Path
import logging
from utils.database import setup_database
from utils.functions import yaml_f
from nextcord import Intents

from utils.twitter import Twitter

log = logging.getLogger(__name__)

token = os.getenv("DISCORD_TOKEN")


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
        self.twitter = Twitter()

    async def on_ready(self):
        """Performs an action when the bot is ready"""
        # Get channels and server
        log.info("Fetching needed channels")
        self.general_channel = await self.fetch_channel(os.getenv("GENERAL_CHANNEL"))
        log.info("Loaded general channel")
        self.memes_channel = await self.fetch_channel(os.getenv("MEMES_CHANNEL"))
        log.info("Loaded memes channel")
        self.audit_channel = await self.fetch_channel(os.getenv("AUDIT_CHANNEL"))
        log.info("Loaded audit channel\n")
        self.server = await self.fetch_guild(os.getenv("VILLAFURRENSE"))
        log.info("Loaded VF server")


        # Load cogs
        cogs = os.listdir("src/cogs/")

        for c in cogs:
            if c.endswith(".py"):
                log.info("Loaded {}".format(c))
                self.load_extension("cogs." + c[:-3])

        # Setup databases
        guilds = self.fetch_guilds()
        async for guild in guilds:

            server = str(guild.id)
            con = setup_database(server)

        log.info("We have logged in as {}".format(self.user))

    def run(self):
        # Set activity
        self.status = nextcord.Status.online
        activity = nextcord.Game(yaml_f.get_activity())
        self.activity = activity

        super().run(token=self.token)

    async def on_message(self, message):
        """Action performed for every message in channels/DM's
        Args:
            message ([discord.Message]): Message to check
        """
        if message.content.lower() == "owo":
            await message.channel.send("OwO!")
        if "vaca " in message.content.lower() and message.author != self.user:
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

    async def on_command_error(self, context: commands.Context, error):
        """Checks error on commands
        Args:
            context ([type]): [Where the command was used]
            error ([type]): [Error of the command]
        """
        message_content = str(context.message.content)
        message_content = message_content.split(" ")
        command_used = message_content[1]
        if len(message_content) >= 3:
            arg1 = message_content[2]

        # Argument missing
        if isinstance(error, commands.MissingRequiredArgument):
            await context.send(
                "Error: Faltan parámetros, escribe `fur help "
                + command_used
                + "` para ver ayuda sobre este comando"
            )

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
