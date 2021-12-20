import nextcord
from nextcord import activity
from nextcord.ext import commands, tasks
import os
from pathlib import Path
import logging
from utils.functions import yaml_f

from utils.twitter import Twitter

log = logging.getLogger(__name__)

token = os.getenv("DISCORD_TOKEN")


class Bot(commands.Bot):
    def __init__(self, token):
        super().__init__(
            command_prefix=["fur ", "Fur ", "FUR "],
            description="uwu",
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
        self.nsfw_memes_channel = await self.fetch_channel(
            os.getenv("NSFW_MEMES_CHANNEL")
        )

        # Load cogs
        cogs = os.listdir("src/cogs/")

        for c in cogs:
            if c.endswith(".py"):
                log.info("Loaded {}".format(c))
                print("src/cogs/" + c)
                self.load_extension("cogs." + c[:-3])

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


## Get info from .env
# token = os.getenv("DISCORD_TOKEN")
# magnet_id = int(os.getenv("MAGNET"))
# angel_id = int(os.getenv("ANGEL"))
#
#
# general_channel = int(os.getenv("GENERAL_CHANNEL"))
#
#
## Activity for the bot
# status = nextcord.Status.online
# activity = nextcord.Game("owo what's this")
#
## Set prefixes for bot commands
# prefixes = ["fur ", "Fur ", "FUR "]
# bot = commands.Bot(command_prefix=prefixes)
#
#
## Remove some commands to use their names
# bot.remove_command("trauma")
# bot.remove_command("enana")
# bot.remove_command("avatar")
#
## Set process name
# setproctitle.setproctitle("furbot")
#
#


#
#
# @bot.event
# async def on_command_error(context, error):
#    """Checks error on commands
#    Args:
#        context ([type]): [Where the command was used]
#        error ([type]): [Error of the command]
#    """
#    message_content = str(context.message.content)
#    message_content = message_content.split(" ")
#    command_used = message_content[1]
#    if len(message_content) >= 3:
#        arg1 = message_content[2]
#
#    # Argument missing
#    if isinstance(error, commands.MissingRequiredArgument):
#        await context.send(
#            "Error: Faltan parámetros, escribe `fur help "
#            + command_used
#            + "` para ver ayuda sobre este comando"
#        )
#
#    # Command does not exist
#    if isinstance(error, commands.CommandNotFound):
#        await context.send(
#            "Error: Comando no existente, escribe `fur help` para ver los comandos disponibles"
#        )
#
#        # Check if exists a similar command
#        output = "Igual quisiste usar alguno de estos comandos:\n"
#        for command in bot.commands:
#            if command_used in str(command):
#                output += str(command) + ", "
#        if output != "Igual quisiste usar alguno de estos comandos:\n":
#            await context.send(output)
#
#    # Not admin access
#    if isinstance(error, commands.CheckFailure):
#        await context.send("Error: No tienes permiso para usar este comando")
#
#    ############### Sticker errors ###################
#    # Forgot to add s
#
#    # Confuse sticker and meme
#    if error.args[0] == "confused_sticker_meme":
#        await context.send("Igual quisiste usar el comando `fur " + error.args[1] + "`")
#
#    # Use list as sticker
#    if error.args[0] == "use_list_as_sticker":
#        await context.send("Prueba con `fur list`")
#
#    # Sticker name already exists
#    if error.args[0] == "sticker_name_exists":
#        await context.send("Error: El nombre de sticker ya existe")
#
#    # Not image provided
#    if error.args[0] == "not_image_provided":
#        await context.send("Error: Falta una imagen")
#
#    # Passed user as argument
#    if error.args[0] == "argument_is_user":
#        await context.send(
#            "Error: El argumento utilizado es un usuario, el argumento debe ser una cadena de texto"
#        )
#
#

#
## Add extensions
# extensions = [
#    "administration",
#    "animal",
#    "fun",
#    "memes",
#    "roast",
#    "stickers",
#    "utilities",
# ]
#
## Set path
# path = os.path.dirname(os.path.abspath(__file__))
# working_dir = os.path.dirname(path)
# os.chdir(working_dir)
## for extension in extensions:
##    bot.load_extension("cogs." + extension)
##
## Run bot
# bot.run(token)
