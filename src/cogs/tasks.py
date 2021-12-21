import asyncio
import logging
import nextcord
from nextcord.ext import commands, tasks
from datetime import datetime, timedelta
import random
from utils.database import create_connection, get_birthdays
from utils.functions import get_hot_subreddit_image, reddit_memes_history_txt, yaml_f

log = logging.getLogger(__name__)


class tasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Start tasks
        self.meme.start()
        self.birthday.start()

    @tasks.loop(hours=1)
    async def meme(self):
        """Sends a random meme"""
        try:

            num = random.randint(0, 2)
            if num == 0:
                subreddit = "dankmemes"
                not_flair = None

            elif num == 1:
                subreddit = "furry_irl"
                not_flair = "Actual Yiff"

            else:
                subreddit = "SpanishMeme"
                not_flair = None
            meme = get_hot_subreddit_image(
                sub_reddit=subreddit,
                posts_limit=1000,
                history_file=reddit_memes_history_txt,
                not_flair=not_flair,
            )

            await self.bot.memes_channel.send(meme)
        except Exception as error:
            log.error("Error ocured on task meme: {}".format(error))
        else:
            log.info("Sent meme from {}".format(subreddit))

    @tasks.loop(hours=1)
    async def birthday(self):
        """Checks if today is somebody's birthday"""
        try:

            now = datetime.now()

            # Get month and day
            month = str(now.month)
            day = str(now.day)
            if len(month) == 1:
                month = "0" + month
            if len(day) == 1:
                day = "0" + day
            today = month + "-" + day

            # Get yaml info
            con = create_connection(str(self.bot.server.id))
            birthdays = get_birthdays(con)
            for id, birthday in birthdays:
                if birthday != None and today in birthday:
                    member = await self.bot.fetch_user(id)
                    await self.bot.general_channel.send(
                        "Es el cumple de " + member.mention + ". Felicidades!!!!!!!!!"
                    )

        except Exception as error:
            log.error("Error ocured on task birthday: {}".format(error))
        else:
            log.info("Sent birthday message of " + member.username)

    @meme.before_loop
    @birthday.before_loop
    async def prep(self):
        log.info("Waiting to execute tasks")

        hours_from_now = 1
        minutes_from_now = 0
        seconds_from_now = 0
        now = datetime.now()
        after = now + timedelta(
            hours=hours_from_now, minutes=minutes_from_now, seconds=seconds_from_now
        )
        # Comment to try tasks that are not at oclock
        after = after.replace(minute=0, second=0)

        delta = (after - now).total_seconds()

        log.info("Waiting {} seconds".format(delta))

        await asyncio.sleep(delta)


def setup(bot: commands.Bot):
    bot.add_cog(tasks(bot))
