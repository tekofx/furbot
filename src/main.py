import discord
from discord.ext import commands, tasks
from discord.flags import MessageFlags
from dotenv import load_dotenv
import os
import setproctitle
import logging
from functions import (
    get_random_line_of_file,
    setup_directories,
    setup_files,
    setup_logs,
    get_hot_subreddit_image,
    cumpleaños_txt,
    get_files_in_directory_with_substring,
    jojos_txt,
    stickers_path,
    exists_file,
    reddit_memes_history_txt,
    yaml_f,
    magnet_id,
    bot,
)
from tasks import dankmemes, cumpleaños, es_viernes

# Get info from .env
load_dotenv()
token = os.getenv("DISCORD_TOKEN")


# Activity for the bot
status = discord.Status.online

# Set prefixes for bot commands
prefixes = ["fur ", "Fur ", "FUR "]


# Remove some commands to use their names
bot.remove_command("trauma")
bot.remove_command("enana")
bot.remove_command("avatar")

# Set process name
setproctitle.setproctitle("furbot")


# When the bot starts
@bot.event
async def on_ready():
    """Performs an action when the bot is ready"""
    setup_directories()
    setup_files()
    setup_logs()
    dankmemes.start()
    es_viernes.start()
    cumpleaños.start()
    await bot.change_presence(
        status=status, activity=discord.Game(name=yaml_f.get_activity())
    )
    print("We have logged in as {0.user}".format(bot))


@bot.event
async def on_command(ctx):
    """Performs an action when a command is used

    Args:
        ctx ([type]): [Context of the used command]
    """
    user = str(ctx.author)
    command = str(ctx.command)
    logging.info(user + " used command " + command)


@bot.event
async def on_command_error(context, error):
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
        for command in bot.commands:
            if command_used in str(command):
                output += str(command) + ", "
        if output != "Igual quisiste usar alguno de estos comandos:\n":
            await context.send(output)

    # Not admin access
    if isinstance(error, commands.CheckFailure):
        await context.send("Error: No tienes permiso para usar este comando")

    ############### Sticker errors ###################
    # Forgot to add s
    if exists_file(message_content[1] + ".png", stickers_path):
        await context.send(
            "Igual quisiste usar un sticker con `fur s " + message_content[1] + "`"
        )

    # Confuse sticker and meme
    if error.args[0] == "confused_sticker_meme":
        await context.send("Igual quisiste usar el comando `fur " + error.args[1] + "`")

    # Use list as sticker
    if error.args[0] == "use_list_as_sticker":
        await context.send("Prueba con `fur list`")

    # Wrong name of sticker
    if error.args[0] == "wrong_sticker_name":
        await context.send(
            "Igual qusiste alguno de estos stickers: "
            + get_files_in_directory_with_substring(arg1, stickers_path)
        )

    # Sticker name already exists
    if error.args[0] == "sticker_name_exists":
        await context.send("Error: El nombre de sticker ya existe")

    # Not image provided
    if error.args[0] == "not_image_provided":
        await context.send("Error: Falta una imagen")

    # Passed user as argument
    if error.args[0] == "argument_is_user":
        await context.send(
            "Error: El argumento utilizado es un usuario, el argumento debe ser una cadena de texto"
        )


# When a message is posted
@bot.event
async def on_message(message):
    """Action performed for every message in channels/DM's

    Args:
        message ([discord.Message]): Message to check
    """
    if message.content.lower() == "owo":
        await message.channel.send("OwO!")
    if "vaca " in message.content.lower() and message.author != bot.user:
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
    if (
        "jojo" in message.content.lower()
        and message.author != bot.user
        and "fur" not in message.content.lower()
    ):
        await message.channel.send(get_random_line_of_file(jojos_txt))
    if (
        ("jojo" in message.content.lower() or "jojos" in message.content.lower())
        and message.author != bot.user
        and "fur" not in message.content.lower()
    ):
        usr = await bot.fetch_user(int(magnet_id))
        string = (
            str(message.author) + " habló de jojos en este mensaje: " + message.jump_url
        )
        await usr.send(string)
    if (
        "teko" in message.content.lower()
        and "cute" in message.content.lower()
        and message.author != bot.user
    ):
        usr = await bot.fetch_user(int(magnet_id))
        string = (
            str(message.author) + " dijo Teko cute en este mensaje: " + message.jump_url
        )
        await usr.send(string)

    await bot.process_commands(message)


# Add extensions
extensions = [
    "administration",
    "animal",
    "fun",
    "memes",
    "roast",
    "stickers",
    "utilities",
]

# Set path
path = os.path.dirname(os.path.abspath(__file__))
working_dir = os.path.dirname(path)
os.chdir(working_dir)
for extension in extensions:
    bot.load_extension("cogs." + extension)

# Run bot
bot.run(token)
