from cogs.functions import *
import datetime
from discord.ext import tasks




@tasks.loop(minutes=1)
async def dankmemes():
    now = datetime.datetime.now()
    if now.minute == 0:
        channel = bot.get_channel(int(os.getenv("MEMES_CHANNEL")))
        if now.hour % 2 == 0:
            await channel.send(get_hot_subreddit_image(("dankmemes"), 10))
        else:
            await channel.send(get_hot_subreddit_image(("memes"), 10))
        logging.info("Dankmeme sent")

@tasks.loop(seconds=1)
async def cumpleaños():
    """Sends a felicitation for birthday"""
    now = datetime.datetime.now()
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    now = str(now)[:-16]
    now = now[-5:]

    if hour == "9" and minute == "0" and second == "0":
        channel = bot.get_channel(general_channel)
        file1 = open(cumpleaños_txt, "r")
        Lines = file1.readlines()
        for line in Lines:
            aux = line.split()
            if now == str(aux[0]):
                user = await bot.fetch_user(int(aux[1]))
                await channel.send(
                    "Es el cumple de " + user.mention + ". Felicidades!!!!!!!!!"
                )
                logging.info("Birthday of " + user.name)


@tasks.loop(seconds=45)
async def es_viernes():
    """Sends es_viernes.mp4 every friday at 9:00"""
    if (
        datetime.datetime.today().weekday() == 4
        and datetime.datetime.now().time().hour == 9
        and datetime.datetime.now().time().minute == 00
    ):
        channel = bot.get_channel(int(os.getenv("GENERAL_CHANNEL")))
        logging.info("Es viernes sent")
        await channel.send(file=discord.File("resources/es_viernes.mp4"))