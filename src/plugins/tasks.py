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


class Tasks(lightbulb.Plugin):
    def __init__(self, bot: lightbulb.Bot):
        super().__init__(name="Tasks")
        self.bot = bot
        self.general_channel = self.bot.cache.get_guild_channel(general_channel_id)
        self.memes_channel = self.bot.cache.get_guild_channel(memes_channel_id)
        self.vf_server = self.bot.cache.get_guild(villafurrense_id)

        # Tasks
        self.loop = asyncio.get_event_loop()
        self.tasks_manager_task = self.loop.create_task(self.tasks_manager())

    async def tasks_manager(self):
        while True:
            if datetime.datetime.now().minute == 0:
                await self.cumpleaños()
                await self.meme()
                await self.es_viernes()
            await asyncio.sleep(60)

    async def meme(self):
        if datetime.datetime.now().hour % 2 == 0:
            meme = get_hot_subreddit_image(
                ("dankmemes"), 1000, reddit_memes_history_txt, None
            )

        else:
            meme = get_hot_subreddit_image(
                ("furry_irl"), 1000, reddit_memes_history_txt, None
            )
        await self.memes_channel.send(attachment=meme)

    async def es_viernes(self):
        """Sends es_viernes.mp4 every friday at 9:00"""
        if (
            datetime.datetime.today().weekday() == 4
            and datetime.datetime.now().time().hour == 9
        ):
            # logging.info("Es viernes sent")
            await self.general_channel.send(attachment="resources/es_viernes.mp4")
        await asyncio.sleep(50)

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


def load(bot: lightbulb.Bot):
    # TODO: Ver si se puede añadir Tasks como plugin
    t = Tasks(bot)
