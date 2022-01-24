import asyncio
import logging
from nextcord.ext import commands, tasks
from datetime import datetime, timedelta
import random
from utils.database import (
    check_entry_in_database,
    create_connection,
    create_user,
    get_birthdays,
)
from utils.bot import Bot

log = logging.getLogger(__name__)


class tasks(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        # Start tasks
        self.meme.start()
        self.birthday.start()
        self.update_users.start()

    @tasks.loop(hours=6)
    async def update_users(self):
        """Updates the users database"""
        async for guild in self.bot.fetch_guilds():
            members = await guild.fetch_members().flatten()
            con = create_connection(str(guild.id))
            for member in members:
                entry_in_database = check_entry_in_database(con, "users", member.id)
                if not entry_in_database and not member.bot:
                    # Add to database
                    author_id = member.id
                    author_name = member.name

                    user_data = [
                        author_id,
                        author_name,
                        member.joined_at,
                    ]
                    try:
                        create_user(con, user_data)
                    except Exception as error:
                        log.error("Error creating user on join: {}".format(error))
                    else:
                        log.info(
                            "Created user {} with id {}".format(author_name, author_id)
                        )

    @tasks.loop(hours=1)
    async def meme(self):
        """Sends a random meme"""

        for guild in self.bot.guilds:

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

                con = create_connection(str(guild.id))
                meme = await self.bot.reddit.get_hot_subreddit_image(
                    sub_reddit=subreddit,
                    posts_limit=1000,
                    database_connection=con,
                    not_flair=not_flair,
                )

                await self.bot.memes_channel_send(guild.id, meme)

            except Exception as error:
                log.error("Error ocured on task meme: {}".format(error))
            else:
                log.info("Sent meme from {}".format(subreddit))

    @tasks.loop(hours=1)
    async def birthday(self):
        """Checks if today is somebody's birthday"""

        now = datetime.now()
        if now.hour == 8:
            try:
                # Get month and day
                month = str(now.month)
                day = str(now.day)
                if len(month) == 1:
                    month = "0" + month
                if len(day) == 1:
                    day = "0" + day
                today = month + "-" + day

                # Get yaml info
                for guild in self.bot.guilds:
                    con = create_connection(str(guild.id))
                    birthdays = get_birthdays(con)
                    for id, birthday in birthdays:
                        print(id, birthday)
                        if birthday != None and today in birthday:
                            member = await self.bot.fetch_user(id)
                            await self.bot.general_channel_send(
                                guild.id,
                                "Es el cumple de "
                                + member.mention
                                + ". Felicidades!!!!!!!!!",
                            )

                            log.info("Sent birthday message of " + member.display_name)

            except Exception as error:
                log.error("Error ocured on task birthday: {}".format(error))

    @update_users.before_loop
    @meme.before_loop
    @birthday.before_loop
    async def prep(self):
        """Waits some time to execute tasks"""
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
