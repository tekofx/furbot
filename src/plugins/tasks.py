from hikari.messages import Attachment
import lightbulb
import datetime
import asyncio
import os
from dotenv import load_dotenv
from functions import get_hot_subreddit_image, reddit_memes_history_txt, yaml_f

load_dotenv()
general_channel_id = os.getenv("GENERAL_CHANNEL")
memes_channel_id = os.getenv("MEMES_CHANNEL")


class Tasks(lightbulb.Plugin):
    def __init__(self, bot: lightbulb.Bot):
        self.name = "Tasks"
        self.bot = bot
        # task starts here
        self.general_channel = self.bot.cache.get_guild_channel(general_channel_id)
        self.memes_channel = self.bot.cache.get_guild_channel(memes_channel_id)

        # Tasks
        self.loop = asyncio.get_event_loop()
        self.tasks_manager_task = self.loop.create_task(self.tasks_manager())

    @lightbulb.command()
    async def stop(self):
        pass

    async def tasks_manager(self):
        while True:
            if datetime.datetime.now().minute == 15:
                await self.dankmeme()
                await self.es_viernes()
                await self.cumpleaños()
                await asyncio.sleep(60)

            else:

                await asyncio.sleep(10)

    async def dankmeme(self):
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
        hour = str(now.hour)
        minute = str(now.minute)
        second = str(now.second)

        if hour == "9":
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
            user_names = content[0]
            user_ids = content[1]
            dates = content[2]
            for x in range(len(dates)):
                if today == dates[x]:

                    # FIXME: Does not work
                    # user = self.vf_server.get_member(int(user_ids[x]))

                    await self.general_channel.send(
                        "Es el cumple de " + user_names[x] + ". Felicidades!!!!!!!!!"
                    )
                    # logging.info("Birthday of " + user.name)

    # TODO: Comprobar
    def cancel(self, task_name: str):
        self._task.cancel()


def load(bot: lightbulb.Bot):
    # TODO: Ver si se puede añadir Tasks como plugin
    # bot.add_plugin(Tasks(bot))
    t = Tasks(bot)
