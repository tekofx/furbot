import asyncio
import logging
import requests
import nextcord
from nextcord.ext import commands, tasks
from datetime import date, datetime, timedelta
import random
from utils.database import (
    check_entry_in_database,
    check_record_in_database,
    create_record,
    create_user,
    exists_channel,
    get_joined_dates,
    remove_records_from_a_date,
)
from utils.bot import Bot

log = logging.getLogger(__name__)


class tasks(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        # Start tasks
        self.meme.start()
        self.update_users.start()
        self.discord_status.start()
        # self.remove_records_from_previous_day.start()
        self.new_github_release.start()
        self.free_games.start()
        self.joined_date.start()
        log.info("Waiting for tasks to start")

    @tasks.loop(hours=2)
    async def free_games(self):
        r = requests.get("https://www.gamerpower.com/api/giveaways?type=game")

        for guild in self.bot.guilds:
            if not exists_channel(guild, "games"):
                continue

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

    @tasks.loop(hours=1)
    async def new_github_release(self):
        "Checks if there is a new release on github and sends a message to the channel"
        r = requests.request(
            "GET", "https://api.github.com/repos/tekofx/furbot/releases"
        )
        r = r.json()
        for guild in self.bot.guilds:
            if not exists_channel(guild, "bot_news"):
                continue

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
            var = datetime(
                date.today().year, date.today().month, date.today().day
            ) - timedelta(days=3)
            remove_records_from_a_date(guild, var, ["meme"])

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
        subreddits = ["dankmemes", "LMDShow", "SpanishMeme", "MemesESP", "orslokx"]
        subreddit = subreddits[num]

        memes = await self.bot.reddit.get_hot_subreddit_submissions_with_media(
            subreddit, 100, 1
        )

        for guild in self.bot.guilds:
            if not exists_channel(guild, "memes"):
                continue
            try:
                for x in memes:
                    if not check_record_in_database(guild, x.url):
                        meme = x
                        create_record(guild, ["meme", meme.url])
                        break

                # If contains video
                if meme.media:
                    print(meme.media)
                    print(type(meme.media))
                    print(meme.media["reddit_video"]["fallback_url"])
                    # download video

                    await self.bot.channel_send(
                        guild, "memes", meme.media["reddit_video"]["fallback_url"]
                    )

                else:
                    await self.bot.channel_send(guild, "memes", meme.url)

                # await self.bot.channel_send(guild, "memes", meme.url)
                log.info("Sent meme from {}".format(subreddit))

            except (Exception) as error:
                log.error("Error sending meme to {}: {}".format(guild.name, error))

    @tasks.loop(hours=1)
    async def joined_date(self):
        """Checks if today is somebody's birthday"""

        now = datetime.now()
        if now.hour != 8:
            return
        now = datetime(now.year, now.month, now.day)

        for guild in self.bot.guilds:

            if not exists_channel(guild, "general"):
                continue
            dates = get_joined_dates(guild)
            for user_id, date in dates:
                now_str = str(now).split(" ")[0][5:]
                if date[5:] == now_str:
                    user = await guild.fetch_member(user_id)
                    years = int(now.year) - int(date[:4])

                    await self.bot.channel_send(
                        guild,
                        "general",
                        "Hoy hace {} años que se unió {}".format(years, user.mention),
                    )

    @tasks.loop(minutes=5)
    async def discord_status(self):
        r = requests.get("https://discordstatus.com/api/v2/summary.json")
        data = r.json()

        for guild in self.bot.guilds:

            if not exists_channel(guild, "audit"):
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
    # @meme.before_loop
    @joined_date.before_loop
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
