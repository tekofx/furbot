import discord
from discord import activity
from discord.ext import commands
from dotenv import load_dotenv
import os
import setproctitle
from cogs.functions import get_hot_subreddit_image, creator, setup_logs, general_channel
import logging
from discord.ext import tasks
import datetime
import asyncio


# Get info from .env
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
creator_id=os.getenv('BOT_CREATOR')
usr1_id=os.getenv('MAGNET')

# Activity for the bot
status = discord.Status.online
activity = discord.Game("owo what's this")

# Set prefixes for bot commands
prefixes = ['fur ', 'Fur ', 'FUR ']
bot = commands.Bot(command_prefix=prefixes, owner_id=int(creator))

# Remove some commands to use their names
bot.remove_command('trauma')
bot.remove_command('enana')
bot.remove_command('avatar')

# Set process name
setproctitle.setproctitle("furbot") 


# When the bot starts
@bot.event
async def on_ready():
    """ Performs an action when the bot is ready
    """
    print('We have logged in as {0.user}'.format(bot))
    setup_logs()
    dankmemes.start()
    es_viernes.start()
    cumpleaños.start()
    await bot.change_presence(status=status, activity=activity)


@bot.event
async def on_command(ctx):
    """ Performs an action when a command is used

    Args:
        ctx ([type]): [Context of the used command]
    """
    server = ctx.guild.name
    user = str(ctx.author)
    command = str(ctx.command)
    logging.info(user+' used command '+command)

@bot.event
async def on_command_error(context, error):
    """Checks error on commands

    Args:
        context ([type]): [Where the command was used]
        error ([type]): [Error of the command]
    """
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send("Error: Faltan parámetros, escribe `fur help <comando>` para ver ayuda sobre ese comando")
    if isinstance(error,commands.CommandNotFound):
        await context.send("Error: Comando no existente, escribe `fur help` para ver los comandos disponibles")

@tasks.loop(seconds=55)
async def dankmemes():
    now = datetime.datetime.now()
    if now.minute==0:
        channel = bot.get_channel(int(os.getenv("MEMES_CHANNEL")))
        logging.info("Dankmeme sent")
        await channel.send(get_hot_subreddit_image(("dankmemes"), 10))



@tasks.loop(seconds=1)
async def cumpleaños():
    """ Sends a felicitation for birthday
    """
    now = datetime.datetime.now()
    hour=str(now.hour)
    minute=str(now.minute)
    second=str(now.second)
    now=str(now)[:-16]
    now=now[-5:]

    if hour=='09' and minute=='0' and second=='0':
        channel = bot.get_channel(general_channel)
        file1 = open('cumpleaños.txt', 'r')
        Lines = file1.readlines()
        for line in Lines:
            aux=line.split()
            if now==str(aux[0]) :
                await channel.send("Es el cumple de "+ aux[1]+'. Felicidades!!!!!!!!!')
                logging.info('Birthday of '+aux[1])


@tasks.loop(seconds=45)
async def es_viernes():
    """ Sends es_viernes.mp4 every friday at 9:00
    """
    if datetime.datetime.today().weekday()==4 and datetime.datetime.now().time().hour==9 and datetime.datetime.now().time().minute==00:
        channel = bot.get_channel(int(os.getenv("GENERAL_CHANNEL")))
        logging.info("Es viernes sent")
        await channel.send(file=discord.File("es_viernes.mp4"))

# When a message is posted
@bot.event
async def on_message(message):
    """ Action performed for every message in channels/DM's

    Args:
        message ([discord.Message]): Message to check
    """
    if message.content.lower() == 'owo':
        await message.channel.send('OwO!')
    if message.content.lower() == 'uwu':
        await message.channel.send('UwU!')
    if message.content.lower() == '7w7':
        await message.channel.send(':eyes:')
    if message.content.lower() == 'ewe':
        await message.channel.send('EwE!')
    if message.content.lower() == 'awa':
        await message.channel.send('AwA!')
    if 'jojo' in message.content.lower():
        await message.channel.send('Kono DIO da!')
    if ('jojo' in message.content.lower() or 'jojos' in message.content.lower()) and message.author!=bot.user:
        creator = await bot.fetch_user(int(creator_id))
        usr=await bot.fetch_user(int(usr1_id))   
        string = str(message.author) + " habló de jojos en este mensaje: " + message.jump_url
        await creator.send(string)
        await usr.send(string)

    await bot.process_commands(message)



# Add extensions
extensions = ["administration", "animal", "fun", "memes", "roast", "stickers", "utilities"]
for extension in extensions:
    bot.load_extension("cogs." + extension)

# Runs bot
bot.run(token)
