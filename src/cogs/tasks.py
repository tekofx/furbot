import asyncio
import logging
import requests
import nextcord
from nextcord.errors import Forbidden
from nextcord.ext import commands, tasks
from datetime import date, datetime, timedelta
import random
from utils.database import (
    check_entry_in_database,
    check_record_in_database,
    create_connection,
    create_record,
    create_user,
    get_birthdays,
    remove_records_from_a_date,
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
        self.discord_status.start()
        self.remove_records_from_previous_day.start()
        self.new_github_release.start()

    @tasks.loop(minutes=5)
    async def new_github_release(self):
        "Checks if there is a new release on github and sends a message to the channel"
        r = requests.request(
            "GET", "https://api.github.com/repos/tekofx/furbot/releases"
        )
        r = r.json()
        for guild in self.bot.guilds:
            if not check_record_in_database(guild, r[0]["url"]):
                create_record(guild, ["github", r[0]["url"]])
                version = r[0]["tag_name"]
                release_changelog = r[0]["body"]
                url = r[0]["html_url"]
                embed = nextcord.Embed(
                    title="Nueva versión " + version, description=url
                )
                embed.set_thumbnail(
                    url="https://raw.githubusercontent.com/tekofx/furbot/main/assets/furbot_logo.png"
                )
                release_changelog = release_changelog.replace("\r", "")
                release_changelog = release_changelog.split("#")
                for i in release_changelog:
                    if i != "":
                        i = i.splitlines()
                        var = "\n".join(i[1:])
                        embed.add_field(name=i[0], value=var, inline=False)

                await self.bot.channel_send(guild, "bot_news", "a", embed)

    @tasks.loop(hours=30)
    async def remove_records_from_previous_day(self):
        """Removes records from 2 days ago"""
        for guild in self.bot.guilds:
            remove_records_from_a_date(guild, date.today(), "github")
        log.info("Removed records from 2 days ago")

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
                        create_user(guild, [member.id, member.name, member.joined_at])
                    except Exception as error:
                        log.error("Error creating user on join: {}".format(error))
                    else:
                        log.info(
                            "Created user {} with id {}".format(member.name, member.id)
                        )

    @tasks.loop(hours=1)
    async def meme(self):
        """Sends a random meme"""

        num = random.randint(0, 2)
        subreddits = ["dankmemes", "furry_irl", "SpanishMeme"]
        subreddit = subreddits[num]

        memes = await self.bot.reddit.get_hot_subreddit_images(subreddit, 100, 1)

        for guild in self.bot.guilds:
            try:
                for x in memes:
                    if not check_record_in_database(guild, x):
                        meme = x
                        create_record(guild, ["meme", meme])
                        break

                await self.bot.channel_send(guild, "memes", meme)
                log.info("Sent meme from {}".format(subreddit))

            except (Exception) as error:
                log.error("Error sending meme to {}: {}".format(guild.name, error))

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

                for guild in self.bot.guilds:
                    birthdays = get_birthdays(guild)
                    for user_id, birthday in birthdays:
                        if birthday != None and today in birthday:
                            member = await self.bot.fetch_user(user_id)
                            await self.bot.channel_send(
                                guild,
                                "general",
                                "Es el cumple de "
                                + member.mention
                                + ". Felicidades!!!!!!!!!",
                            )

                            log.info("Sent birthday message of " + member.display_name)

            except (Exception, Forbidden) as error:
                if isinstance(error, nextcord.Forbidden):
                    log.error("Forbidden error on task birthday: {}".format(error))
                    await self.bot.channel_send(
                        guild,
                        "general",
                        "Error: El bot no tiene permiso para enviar mensajes",
                    )
                else:
                    log.error("Unknown error on task birthday: {}".format(error))
                    await self.bot.channel_send(
                        guild, "general", "Error desconocido, contacta al creador"
                    )

    @tasks.loop(minutes=5)
    async def discord_status(self):
        r = requests.get("https://discordstatus.com/api/v2/summary.json")
        data = r.json()

        for guild in self.bot.guilds:

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

    @discord_status.before_loop
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
