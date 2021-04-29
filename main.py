import discord
from discord import activity
from discord.ext import commands
from dotenv import load_dotenv
import os
import setproctitle
from cogs.functions import *
import logging
from discord.ext import tasks
import datetime


# Get info from .env
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
creator_id=os.getenv('BOT_CREATOR')
usr1_id=os.getenv('MAGNET')


status = discord.Status.online
activity = discord.Game("owo what's this")

prefixes = ['fur ', 'Fur ', 'FUR ']
bot = commands.Bot(command_prefix=prefixes, owner_id=int(creator))
bot.remove_command('trauma')
bot.remove_command('enana')
bot.remove_command('avatar')
setproctitle.setproctitle("furbot")  # <-- setting the process name


# When the bot starts
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    setup_logs()
    dankmemes.start()
    es_viernes.start()
    await bot.change_presence(status=status, activity=activity)


@bot.event
async def on_command(ctx):
    server = ctx.guild.name
    user = str(ctx.author)
    command = str(ctx.command)
    logging.info(user+' used command '+command)

@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send("Error: Faltan parámetros")
    if isinstance(error,commands.CommandNotFound):
        await context.send("Error: Comando no existente")

@tasks.loop(seconds=45)
async def dankmemes():
    now = datetime.datetime.now()
    if now.minute==0:
        channel = bot.get_channel(int(os.getenv("MEMES_CHANNEL")))
        logging.info("Dankmeme sent")
        await channel.send(get_top_reddit_image("dankmemes", 3))


@tasks.loop(seconds=45)
async def es_viernes():
    
    if datetime.datetime.today().weekday()==4 and datetime.datetime.now().time().hour==9 and datetime.datetime.now().time().minute==00:
        channel = bot.get_channel(int(os.getenv("GENERAL_CHANNEL")))
        logging.info("Es viernes sent")
        await channel.send(file=discord.File("es_viernes.mp4"))

# When a message is posted
@bot.event
async def on_message(message):
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


bot.run(token)
