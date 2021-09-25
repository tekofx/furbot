import datetime
from discord.ext import tasks
import logging
import discord
import os
from functions import (
    bot,
    get_hot_subreddit_image,
    reddit_memes_history_txt,
    yaml_f,
)

general_channel = int(os.getenv("GENERAL_CHANNEL"))


@tasks.loop(minutes=1)
async def dankmemes():
    now = datetime.datetime.now()
    if now.minute == 0:
        channel = bot.get_channel(int(os.getenv("MEMES_CHANNEL")))
        if now.hour % 2 == 0:
            await channel.send(
                get_hot_subreddit_image(("dankmemes"), 10, reddit_memes_history_txt)
            )
        else:
            await channel.send(
                get_hot_subreddit_image(("memes"), 10, reddit_memes_history_txt)
            )
        logging.info("Dankmeme sent")


@tasks.loop(seconds=1)
async def cumpleaños():
    """Sends a felicitation for birthday"""
    now = datetime.datetime.now()
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    month = str(now.month)
    day = str(now.day)
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    today = month + "-" + day

    if hour == "9" and minute == "0" and second == "0":
        content = yaml_f.get_cumpleaños()
        fechas = content[0]
        users = content[1]
        channel = bot.get_channel(general_channel)
        for x in range(len(fechas)):
            if today == fechas[x]:

                user = await bot.fetch_user(int(users[x]))
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
