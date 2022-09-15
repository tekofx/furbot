import asyncio
from utils import logger
import requests
import nextcord
from nextcord.ext import commands, tasks
from datetime import datetime, timedelta
import random
from utils.database import (
    check_entry_in_database,
    check_record_in_database,
    clean_records_no_account,
    create_record,
    create_user,
    exists_channel_of_type,
    get_posts,
    get_users_with_joined_date_today,
)
from utils.bot import Bot


log = logger.getLogger(__name__)


class tasks(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        # Start tasks
        self.update_users.start()
        self.free_games.start()
        self.joined_date.start()
        self.estaciones.start()
        # Get posts from database
        for guild in self.bot.guilds:
            posts = get_posts(guild)
            if posts:
                for post in posts:

                    self.bot.loop.create_task(self.post_task(guild, post))
                    log.info(
                        f"Created post task of account {post[2]}",
                        extra={"guild": guild.id},
                    )

    @tasks.loop(hours=1)
    async def estaciones(self):
        now = datetime.now()
        if now.hour != 10:
            return
        msg = None
        if now.month == 6 and now.day == 28:
            msg = "Feliz Orgullo :rainbow: :rainbow: :rainbow:"
        if now.month == 12 and now.day == 25:
            msg = "Feliz Navidad :santa: :santa: :santa:"
        if now.month == 1 and now.day == 1:
            msg = "Feliz Año Nuevo :christmas_tree: :christmas_tree: :christmas_tree:"
        if now.month == 10 and now.day == 31:
            msg = "Feliz Halloween :ghost: :ghost: :ghost:"

        if msg:
            for guild in self.bot.guilds:
                if not exists_channel_of_type(guild, "general"):
                    continue

                await self.bot.channel_send(guild, "general", msg)

    @tasks.loop(hours=2)
    async def free_games(self):
        r = requests.get("https://www.gamerpower.com/api/giveaways?type=game")

        for guild in self.bot.guilds:
            if not exists_channel_of_type(guild, "games"):
                continue

            # Remove games records that are not fetched by the api
            ids = [str(i["id"]) for i in r.json()]
            clean_records_no_account(guild, "game", ids)

            for x in r.json():
                if not check_record_in_database(guild, x["id"]):
                    create_record(guild, "game", x["id"])
                    title = x["title"]
                    decription = x["description"]
                    url = x["open_giveaway_url"]
                    thumbnail = x["thumbnail"]
                    platform = x["platforms"]

                    embed = nextcord.Embed(title=title)
                    embed.add_field(name="Descripcion", value=decription, inline=False)
                    embed.add_field(name="Plataforma", value=platform, inline=False)
                    embed.add_field(name="Link", value=url, inline=False)
                    embed.set_image(url=thumbnail)

                    await self.bot.channel_send(
                        guild, channel_type="games", msg="a", embed=embed
                    )

    async def post_task(self, guild: nextcord.Guild, post: list):
        """Creates a new task

        Args:
            guild (nextcord.Guild): guild
            post (list): post to be posted
        """
        channel_id = post[0]
        nsfw = post[1]
        account = post[2]
        post_inteval = post[4]
        if nsfw == "nsfw":
            nsfw = True
        else:
            nsfw = False
        try:
            channel = await self.bot.fetch_channel(channel_id)
        except nextcord.errors.Forbidden:
            log.error(
                f"{guild.name} - {channel_id} is not accesible",
                extra={"guild": guild.id},
            )
            await self.bot.channel_send(
                guild,
                "audit",
                "Error al intentar publicar en canal el post id={}: No tengo acceso al canal".format(
                    account
                ),
            )
            return

        if not channel.permissions_for(guild.me).send_messages:
            log.error(
                f"{guild.name} - {channel.name} doesn't have permission to send messages in ",
                extra={"guild": guild.id},
            )
            await self.bot.channel_send(
                guild,
                "audit",
                "Error al intentar publicar en canal {} post {}: No tengo permiso para enviar mensajes".format(
                    channel.mention, account
                ),
            )
            return

        log.info(f"Started task {account}", extra={"guild": guild.id})

        # Wait until oclock to run post
        await self.wait_until_oclock()

        # Loop execution
        while True:
            if " " in account:  # Multiple accounts
                post_account = account.split(" ")
                post_account = random.choice(post_account)

            if "twitter" in post_account:
                twitter_account = post_account.replace("twitter@", "")
                embed = self.bot.twitter.get_latest_image_not_repeated(
                    guild, twitter_account, "twitter"
                )

            else:
                reddit_account = post_account.replace("reddit@", "")
                embed = await self.bot.reddit.get_hot_pic_not_repeated(
                    guild, reddit_account, "reddit", nsfw
                )
            try:
                await channel.send(embed=embed)
                log.info(f"Post from {post_account} sent", extra={"guild": guild.id})
            except Exception as error:
                log.error(
                    f"Could not send post from {post_account} in {guild.name}: {error}",
                    extra={"guild": guild.id},
                )
            await asyncio.sleep(post_inteval * 60)

    @tasks.loop(hours=1)
    async def update_users(self):
        """Updates the users database"""
        async for guild in self.bot.fetch_guilds():
            members = await guild.fetch_members().flatten()
            for member in members:
                entry_in_database = check_entry_in_database(guild, "users", member.id)
                if not entry_in_database and not member.bot:
                    # Add to database
                    try:
                        joined_date = datetime.strftime(member.joined_at, "%Y-%m-%d")
                        create_user(guild, [member.id, member.name, joined_date])
                    except Exception as error:
                        log.error(
                            "Error creating user on join: {}".format(error),
                            extra={"guild": guild.id},
                        )

    @tasks.loop(hours=1)
    async def joined_date(self):
        """Checks if today is somebody's birthday"""

        now = datetime.now()
        if now.hour != 10:
            return
        now = datetime(now.year, now.month, now.day)

        for guild in self.bot.guilds:

            if not exists_channel_of_type(guild, "general"):
                continue

            members = get_users_with_joined_date_today(guild)

            for member in members:
                member_id = member[0]
                joined_date = member[1]

                member = await guild.fetch_member(member_id)
                years = now.year - int(joined_date.split("-")[0])

                if years == 0:
                    return

                await self.bot.channel_send(
                    guild,
                    "general",
                    "Felicidades {}, hoy cumples {} años en el server".format(
                        member.mention, years
                    ),
                )

    @free_games.before_loop
    @joined_date.before_loop
    async def wait_until_oclock(self):
        """Waits some time to execute tasks"""

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

        await asyncio.sleep(delta)


def setup(bot: commands.Bot):
    bot.add_cog(tasks(bot))
