import logging
from hikari.messages import Attachment
import lightbulb
import datetime
import asyncio
import os
from dotenv import load_dotenv
from functions import get_hot_subreddit_image, reddit_memes_history_txt, yaml_f

load_dotenv()
villafurrense_id = os.getenv("VILLAFURRENSE")
general_channel_id = os.getenv("GENERAL_CHANNEL")
memes_channel_id = os.getenv("MEMES_CHANNEL")

log = logging.getLogger(__name__)


class Tasks(lightbulb.Plugin):
    def __init__(self, bot: lightbulb.Bot):
        super().__init__(name="Tasks")
        self.bot = bot

        # Tasks
        self.loop = asyncio.get_event_loop()
        self.tasks_manager_task = self.loop.create_task(self.tasks_manager())

    async def tasks_manager(self):
        self.general_channel = await self.bot.rest.fetch_channel(general_channel_id)
        self.memes_channel = await self.bot.rest.fetch_channel(memes_channel_id)
        self.vf_server = await self.bot.rest.fetch_guild(villafurrense_id)

        while True:
            if datetime.datetime.now().min == 0:
                log.info("Executing tasks")
                await self.save_users()
                await self.cumpleaños()
                await self.meme()
                await self.es_viernes()
                await asyncio.sleep(50)

    async def meme(self):
        if datetime.datetime.now().hour % 2 == 0:
            meme = get_hot_subreddit_image(
                sub_reddit="dankmemes",
                posts_limit=1000,
                history_file=reddit_memes_history_txt,
                not_flair=None,
            )

        else:
            meme = get_hot_subreddit_image(
                sub_reddit="furry_irl",
                posts_limit=1000,
                history_file=reddit_memes_history_txt,
                not_flair="Actual Yiff",
            )

        await self.memes_channel.send(attachment=meme)
        log.info("Sent meme")

    async def es_viernes(self):
        """Sends es_viernes.mp4 every friday at 9:00"""
        if (
            datetime.datetime.today().weekday() == 4
            and datetime.datetime.now().time().hour == 9
        ):
            # logging.info("Es viernes sent")
            await self.general_channel.send(attachment="resources/es_viernes.mp4")
            log.info("Sent es_viernes.mp4")

    async def cumpleaños(self):
        now = datetime.datetime.now()
        hour = now.hour

        if hour == 9:
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
            for x in range(len(dates)):
                if today == dates[x]:
                    member = await self.bot.rest.fetch_user(user_ids[x])
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


def load(bot: lightbulb.Bot):
    bot.add_plugin(Tasks(bot))


def unload(bot: lightbulb.Bot):
    bot.remove_plugin("Tasks")
