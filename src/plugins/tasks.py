import logging
import lightbulb
from datetime import datetime, timedelta
import asyncio
from utils.functions import get_hot_subreddit_image, reddit_memes_history_txt, yaml_f
import random
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.base import BaseScheduler

log = logging.getLogger(__name__)


class Tasks(lightbulb.Plugin):
    def __init__(self, bot: lightbulb.Bot):
        super().__init__(name="Tasks")
        self.bot = bot

        # Tasks
        self.get_channels_tasks = self.bot.scheduler.add_job(
            self.get_channels, CronTrigger(minute=55, second=0)
        )
        self.meme_task = self.bot.scheduler.add_job(
            self.meme, CronTrigger(minute=55, second=10)
        )
        self.cumpleaños_task = self.bot.scheduler.add_job(
            self.cumpleaños, CronTrigger(hour=8, minute=10, second=0)
        )
        self.save_users_task = self.bot.scheduler.add_job(
            self.save_users, CronTrigger(minute=55, second=30)
        )

    async def get_channels(self):
        """Get channels objects"""
        self.general_channel = await self.bot.rest.fetch_channel(
            self.bot.general_channel_id
        )
        self.memes_channel = await self.bot.rest.fetch_channel(
            self.bot.memes_channel_id
        )
        self.vf_server = await self.bot.rest.fetch_guild(self.bot.villafurrense_id)

    async def meme(self):
        """Sends a random meme"""
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

        await self.memes_channel.send(attachment=meme)
        log.info("Sent meme from {}".format(subreddit))

    async def cumpleaños(self):
        """Checks if today is somebody's birthday"""
        now = datetime.now()
        hour = now.hour

        # Get month and day
        month = str(now.month)
        day = str(now.day)
        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day
        today = month + "-" + day

        # Get yaml info
        content = yaml_f.get_cumpleaños()
        user_ids = content[1]
        dates = content[2]
        index = dates.index(today)
        member = await self.bot.rest.fetch_user(user_ids[index])
        await self.general_channel.send(
            "Es el cumple de " + member.mention + ". Felicidades!!!!!!!!!"
        )
        log.info("Sent birthday message of " + member.username)

    async def save_users(self):
        """Saves users in Villafurrense to yaml file"""
        members = self.bot.rest.fetch_members(self.vf_server)
        output = {}
        async for i, member in members.enumerate():
            if not member.is_bot:
                users = {
                    member.username: {
                        "id": int(member.id),
                        "times_joined": 0,
                        "joined_date": member.joined_at,
                    }
                }
                output.update(users)

        yaml_f.set_user_list(output)


def load(bot: lightbulb.Bot):
    bot.add_plugin(Tasks(bot))


def unload(bot: lightbulb.Bot):
    bot.remove_plugin("Tasks")


async def wait_until_hour(hour: int, minute: int, second: int):
    """Waits until a time

    Args:
        hour (int): hour of time
        minute (int): minute of time
        second (int): second of time
    """
    now = datetime.now()
    now_after = now + timedelta(hours=hour, minutes=minute, seconds=second)

    if now_after.day != now.day:  # The hour is on following day
        now = now + timedelta(days=1)
    var = datetime(now.year, now.month, now.day, hour, minute, second)
    wait_seconds = (var - now).seconds
    await asyncio.sleep(wait_seconds)


async def wait_time(hours: int, minutes: int, seconds: int):
    """Wait a determine time

    Args:
        hours (int): hours to wait
        minutes (int): minutes to wait
        seconds (int): seconds to wait
    """
    wait_seconds = timedelta(
        hours=hours, minutes=minutes, seconds=seconds
    ).total_seconds()
    await asyncio.sleep(wait_seconds)
