import asyncio
from core import logger
import requests
import nextcord
from nextcord.ext import commands, tasks
from datetime import datetime, timedelta
import random

from core.bot import Bot


log = logger.getLogger(__name__)


class Tasks(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        
        # Start tasks
        self.update_users.start()
        self.free_games.start()
        self.joined_date.start()
        self.estaciones.start()
        self.birthday.start()
        self.sync_commands.start()
        
        # Get posts from database
        for guild in self.bot.guilds:
            posts=self.bot.db.get_posts(guild)
            if posts:
                for post in posts:
                    post_id = post[0]
                    channel_id = post[2]
                    visibility = post[3]
                    service = post[4]
                    account = post[5]
                    interval = post[6]
                    task = self.bot.loop.create_task(
                        self.post_task(
                            guild, channel_id, visibility, service, account, interval
                        ),
                        name=post_id,
                    )
                    self.bot.tasks[post_id] = task
                    log.info(
                        f"Created post task of account {post[2]}",
                        extra={"guild": guild.name},
                    )
        

    @tasks.loop(hours=2)
    async def sync_commands(self):
        log.info("Syncing commands")
        await self.bot.sync_application_commands(self.bot._local_guild)

    @tasks.loop(hours=1)
    async def estaciones(self):
        now = datetime.now()
        if now.hour != 0:
            return
        msg = None
        if now.month == 6 and now.day == 28:
            msg = "Feliz Orgullo :rainbow: :rainbow: :rainbow:"
        if now.month == 12 and now.day == 25:
            msg = "Feliz Navidad :santa: :santa: :santa:"
        if now.month == 1 and now.day == 1:
            msg = "Feliz Año Nuevo 🎉🎉🎉"
        if now.month == 10 and now.day == 31:
            msg = "Feliz Halloween :ghost: :ghost: :ghost:"

        if msg:
            for guild in self.bot.guilds:
                
                if not self.bot.db.exists_channel_of_type(guild, "general"):
                    continue

                await self.bot.channel_send(guild, "general", msg)

    @tasks.loop(hours=2)
    async def free_games(self):
        r = requests.get("https://www.gamerpower.com/api/giveaways?type=game")

        for guild in self.bot.guilds:
            if not self.bot.db.exists_channel_of_type(guild, "games"):
                continue

            # Remove games records that are not fetched by the api
            ids = [str(i["id"]) for i in r.json()]
            self.bot.db.clean_records(guild, "game", ids)

            for x in r.json():
                
                if not self.bot.db.record_exists(guild,x["id"]):
                    self.bot.db.insert_record(guild, "game", x["id"])
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

    async def post_task(
        self,
        guild: nextcord.Guild,
        channel_id: int,
        visibility: str,
        service: str,
        account: str,
        interval: str,
    ):
        """Creates a new task

        Args:
            guild (nextcord.Guild): guild
            post (list): post to be posted
        """
        if visibility == "nsfw":
            visibility = True
        else:
            visibility = False
        try:
            channel = await self.bot.fetch_channel(channel_id)
        except nextcord.errors.Forbidden:
            log.error(
                f"{guild.name} - {channel_id} is not accesible",
                extra={"guild": guild.name},
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
                extra={"guild": guild.name},
            )
            await self.bot.channel_send(
                guild,
                "audit",
                "Error al intentar publicar en canal {} post {}: No tengo permiso para enviar mensajes".format(
                    channel.mention, account
                ),
            )
            return

        log.info(f"Started task {account}", extra={"guild": guild.name})

        # Wait until oclock to run post
        await self.wait_until_oclock()

        # Loop execution
        while True:
            next_task = datetime.now() + timedelta(seconds=interval * 60)

            if service == "twitter":
                embed = self.bot.twitter.get_latest_image_not_repeated(
                    guild, account, "twitter"
                )

            if service == "reddit":
                embed = await self.bot.reddit.get_hot_pic_not_repeated(
                    guild, account, "reddit", visibility
                )
                
            if service =="mastodon":
                instance=account.split("@")[1]
                account = account.split("@")[0]
                embed=self.bot.mastodon.get_latest_image_not_repeated(guild, account, instance)
            if embed:
                try:
                    await channel.send(embed=embed)
                except Exception as error:
                    log.error(
                        f"Task of account {account}({service}): {error}",
                        extra={"guild": guild.name},
                    )
            new_interval = next_task - datetime.now()
            await asyncio.sleep(new_interval.seconds)

    @tasks.loop(hours=1)
    async def update_users(self):
        """Updates the users database"""
        async for guild in self.bot.fetch_guilds():
            members = await guild.fetch_members().flatten()
            
            # Add new users
            for member in members:
                entry_in_database=self.bot.db.exists_user(member)
                if not entry_in_database and not member.bot:
                    # Add to database
                    try:
                        self.bot.db.insert_user(member)
                    except Exception as error:
                        log.error(
                            "Error creating user: {}".format(error),
                            extra={"guild": guild.name},
                        )
                        
    @tasks.loop(hours=1)
    async def joined_date(self):
        """Checks if today someone joined the server and posts a message in general"""

        now = datetime.now()
        if now.hour != 10:
            return
        now = datetime(now.year, now.month, now.day)

        for guild in self.bot.guilds:
            
            if not self.bot.db.exists_channel_of_type(guild, "general"):
                continue

            members = self.bot.db.get_users_with_joined_day_today(guild)

            for member in members:
                member_id = int(member[0])
                joined_date = member[3]

                member = await guild.fetch_member(member_id)
                years = now.year - int(joined_date.year)

                if years == 0:
                    return

                await self.bot.channel_send(
                    guild,
                    "general",
                    "Felicidades {}, hoy cumples {} años en el server".format(
                        member.mention, years
                    ),
                )

    @tasks.loop(hours=1)
    async def birthday(self):
        """Checks if today is somebody's birthday"""

        now = datetime.now()
        if now.hour != 0:
            return

        for guild in self.bot.guilds:
            
            
            if not self.bot.db.exists_channel_of_type(guild, "general"):
                continue

            members = self.bot.db.get_users(guild)
            for member in members:
                member_id = member[0]
                birthday=member[4]
                if birthday==None:
                    continue
                
                if birthday.day == now.day and birthday.month == now.month:

                    member = await guild.fetch_member(member_id)

                    await self.bot.channel_send(
                        guild,
                        "general",
                        f"Hoy es el cumple de {member.mention}, Felicidades!",
                    )

    #@joined_date.before_loop
    @free_games.before_loop
    @sync_commands.before_loop
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
    bot.add_cog(Tasks(bot))
