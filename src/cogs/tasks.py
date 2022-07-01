import asyncio
import logging
import requests
import nextcord
from nextcord.ext import commands, tasks
from datetime import datetime, timedelta
import random
from utils.database import (
    check_entry_in_database,
    check_record_in_database,
    create_record,
    create_user,
    exists_channel_of_type,
    remove_records_2_days,
    get_posts,
    get_records_of_type,
    remove_record,
    get_users_with_joined_date_today,
)
from utils.bot import Bot


log = logging.getLogger(__name__)


class tasks(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        # Start tasks
        self.post.start()
        self.update_users.start()
        self.discord_status.start()
        self.remove_records_from_previous_day.start()
        self.ordure_bizarre.start()
        self.free_games.start()
        self.joined_date.start()

    def remove_games(self, guild: nextcord.Guild, games: list):
        ids = [i["id"] for i in games]
        records = get_records_of_type(guild, "game")
        records = [int(i[1]) for i in records]

        for record in records:
            if record not in ids:
                remove_record(guild, record)

    @tasks.loop(hours=2)
    async def free_games(self):
        r = requests.get("https://www.gamerpower.com/api/giveaways?type=game")

        for guild in self.bot.guilds:
            if not exists_channel_of_type(guild, "games"):
                continue

            # Remove games records that are not sent by the api
            self.remove_games(guild, r.json())

            for x in r.json():
                if not check_record_in_database(guild, x["id"]):
                    create_record(guild, ["game", x["id"]])
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

    @tasks.loop(hours=48)
    async def remove_records_from_previous_day(self):
        """Removes records from 2 days ago"""
        for guild in self.bot.guilds:
            remove_records_2_days(guild, ("post", "incident", "animal"))

    @tasks.loop(hours=1)
    async def post(self):
        """Posts a random post from an account/s"""
        for guild in self.bot.guilds:
            posts = get_posts(guild)
            for post in posts:
                channel_id = post[0]
                nsfw = post[1]
                account = post[2]
                post_id = post[3]
                if nsfw == "nsfw":
                    nsfw = True
                else:
                    nsfw = False
                try:
                    channel = await self.bot.fetch_channel(channel_id)
                except nextcord.errors.Forbidden:
                    log.error(f"{guild.name} - {channel_id} is not accesible")
                    await self.bot.channel_send(
                        guild,
                        "audit",
                        "Error al intentar publicar en canal el post id={}: No tengo acceso al canal".format(
                            post_id
                        ),
                    )
                    return

                if not channel.permissions_for(guild.me).send_messages:
                    log.error(
                        f"{guild.name} - {channel.name} doesn't have permission to send messages in "
                    )
                    await self.bot.channel_send(
                        guild,
                        "audit",
                        "Error al intentar publicar en canal {} post id={}: No tengo permiso para enviar mensajes".format(
                            channel.mention, post_id
                        ),
                    )
                    return

                if " " in account:  # Multiple accounts
                    accounts = account.split(" ")
                    account = random.choice(accounts)

                if "twitter" in account:
                    twitter_account = account.replace("twitter@", "")
                    embed = self.bot.twitter.get_latest_image_not_repeated(
                        guild, twitter_account, "post"
                    )

                else:
                    reddit_account = account.replace("reddit@", "")
                    embed = await self.bot.reddit.get_hot_pic_not_repeated(
                        guild, reddit_account, "post", nsfw
                    )

                try:
                    await channel.send(embed=embed)
                except Exception as error:
                    log.error(
                        f"Could not send post from {account} in {guild.name}: {error}"
                    )
                    continue

    @tasks.loop(hours=6)
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
                        log.error("Error creating user on join: {}".format(error))
                    else:
                        log.info(
                            "Created user {} with id {}".format(member.name, member.id)
                        )

    @tasks.loop(minutes=10)
    async def ordure_bizarre(self):
        post = self.bot.twitter.get_latest_image("ordurebizarree")
        for guild in self.bot.guilds:
            if not exists_channel_of_type(guild, "ordure"):
                continue

            if not check_record_in_database(guild, post):
                create_record(guild, ["meme", post])
                await self.bot.channel_send(guild, channel_type="ordure", msg=post)

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

    @tasks.loop(minutes=5)
    async def discord_status(self):
        r = requests.get("https://discordstatus.com/api/v2/summary.json")
        data = r.json()

        for guild in self.bot.guilds:

            if not exists_channel_of_type(guild, "audit"):
                continue

            for incident in data["incidents"]:

                incident_id = incident["id"]
                incident_name = incident["name"]
                incident_status = incident["status"]
                incident_impact = incident["impact"]

                if incident_impact == "Minor":
                    color = nextcord.Color.yellow()
                elif incident_impact == "Major":
                    color = nextcord.Color.orange()
                elif incident_impact == "Critical":
                    color = nextcord.Color.red()
                else:
                    color = nextcord.Color.green()

                embed = nextcord.Embed(title="Discord Status", color=color)
                embed.add_field(name="Incidencia", value=incident_name)
                embed.add_field(name="Estado", value=incident_status)
                embed.add_field(name="ID", value=incident_id)
                embed.add_field(name="Impacto", value=incident_impact)

                # Inform about a new incident
                if not check_record_in_database(guild, incident_id):
                    create_record(guild, ["incident", incident_id])
                    await self.bot.channel_send(guild, "audit", "a", embed)

                # Inform about an incident update

                for update in incident["incident_updates"]:

                    update_id = update["id"]
                    update_body = update["body"]
                    update_status = update["status"]
                    update_embed = nextcord.Embed(
                        title="Actualización incidencia",
                        color=nextcord.Color.dark_grey(),
                    )
                    update_embed.add_field(name="ID", value=update_id, inline=False)
                    update_embed.add_field(
                        name="Actualización", value=update_body, inline=False
                    )
                    update_embed.add_field(
                        name="Estado", value=update_status, inline=False
                    )
                    if not check_record_in_database(guild, update_id):
                        create_record(guild, ["incident", update_id])
                        await self.bot.channel_send(guild, "audit", "a", update_embed)

    @free_games.before_loop
    @discord_status.before_loop
    @joined_date.before_loop
    @post.before_loop
    async def prep(self):
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
