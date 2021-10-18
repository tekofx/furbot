import logging
import lightbulb
from datetime import datetime, timedelta
import asyncio
from utils.functions import get_hot_subreddit_image, reddit_memes_history_txt, yaml_f
import random

log = logging.getLogger(__name__)


class Tasks(lightbulb.Plugin):
    def __init__(self, bot: lightbulb.Bot):
        super().__init__(name="Tasks")
        self.bot = bot

        # Tasks
        self.loop = asyncio.get_event_loop()
        self.tasks_manager_task = self.loop.create_task(self.tasks_manager())

    async def tasks_manager(self):
        self.general_channel = await self.bot.rest.fetch_channel(
            self.bot.general_channel_id
        )
        self.memes_channel = await self.bot.rest.fetch_channel(
            self.bot.memes_channel_id
        )
        self.vf_server = await self.bot.rest.fetch_guild(self.bot.villafurrense_id)

        # The tasks will be run every hour at minute 0
        while True:
            # Wait until time
            now = datetime.now()
            hour = now.hour + 1
            minute = 0
            second = 5

            log.info(
                "Waiting until {} to run tasks".format(
                    str(hour) + ":" + str(minute) + ":" + str(second)
                )
            )
            await wait_until_hour(hour, minute, second)

            # Execute tasks
            log.info("Executing tasks")
            await self.save_users()
            await self.cumpleaños()
            await self.meme()
            log.info
            await self.es_viernes()

    async def meme(self):
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
        log.info("Sent meme")

    async def es_viernes(self):
        """Sends es_viernes.mp4 every friday at 9:00"""
        if datetime.today().weekday() == 4 and datetime.now().time().hour == 9:
            # logging.info("Es viernes sent")
            await self.general_channel.send(attachment="resources/es_viernes.mp4")
            log.info("Sent es_viernes.mp4")

    async def cumpleaños(self):
        """Checks if today is somebody's birthday"""
        now = datetime.now()
        hour = now.hour

        if hour == 8:
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
                users = {member.username: int(member.id)}
                output.update(users)

        yaml_f.set_user_list(output)
        log.info("Saved user list")

    @lightbulb.command()
    async def remindme(self, ctx: lightbulb.Context, text: str, time: str):
        """Crea un recordatorio para una hora concreta

        Uso:\n
            fur remindme "Comprar leche" 17:45
        """
        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])
        log.info(
            "Waiting until {} to remind {} {}".format(time, ctx.member.username, text)
        )
        await ctx.respond("Ok, te recordaré {} a las {}".format(text, time))
        await wait_until_hour(hour, minute)
        await ctx.member.send("Recordatorio: " + text)


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
