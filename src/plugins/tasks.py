import logging
import lightbulb
from datetime import datetime
from utils.functions import get_hot_subreddit_image, reddit_memes_history_txt, yaml_f
import random
from apscheduler.triggers.cron import CronTrigger

log = logging.getLogger(__name__)


class Tasks(lightbulb.Plugin):
    def __init__(self, bot: lightbulb.BotApp):
        super().__init__(name="Tasks")
        self.bot_client = bot

        # Tasks
        self.meme_task = self.bot_client.scheduler.add_job(
            self.meme, CronTrigger(minute=0, second=10)
        )
        self.cumpleaños_task = self.bot_client.scheduler.add_job(
            self.cumpleaños, CronTrigger(hour=8, minute=0, second=0)
        )

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

        await self.bot.memes_channel.send(attachment=meme)
        log.info("Sent meme from {}".format(subreddit))

    async def cumpleaños(self):
        """Checks if today is somebody's birthday"""
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
        content = yaml_f.get_cumpleaños()
        user_ids = content[1]
        dates = content[2]
        index = dates.index(today)
        member = await self.bot.rest.fetch_user(user_ids[index])
        await self.bot.general_channel.send(
            "Es el cumple de " + member.mention + ". Felicidades!!!!!!!!!"
        )
        log.info("Sent birthday message of " + member.username)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(Tasks(bot))


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin("Tasks")
