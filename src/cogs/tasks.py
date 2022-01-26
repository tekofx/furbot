import asyncio
from cgitb import text
import logging
import requests
import discord
import nextcord
from nextcord.errors import Forbidden
from nextcord.ext import commands, tasks
from datetime import datetime, timedelta
import random
from utils.database import (
    check_entry_in_database,
    check_record_in_database,
    create_connection,
    create_record,
    create_user,
    get_birthdays,
)
from utils.bot import Bot

log = logging.getLogger(__name__)


class tasks(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        # Start tasks
        # self.meme.start()
        # self.birthday.start()
        # self.update_users.start()
        self.discord_status.start()

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

        num = random.randint(0, 1)
        if num == 0:
            subreddit = "dankmemes"

        else:
            subreddit = "furry_irl"

        """ else:
            subreddit = "SpanishMeme" """

        memes = await self.bot.reddit.get_hot_subreddit_images(subreddit, 100)

        for guild in self.bot.guilds:
            try:
                con = create_connection(str(guild.id))
                for x in memes:
                    if not check_record_in_database(con, x):
                        meme = x
                        create_record(con, ["meme", meme])
                        break

                await self.bot.channel_send(guild.id, "memes", meme)
                con.close()

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
                    con = create_connection(str(guild.id))
                    birthdays = get_birthdays(con)
                    for id, birthday in birthdays:
                        if birthday != None and today in birthday:
                            member = await self.bot.fetch_user(id)
                            await self.bot.channel_send(
                                guild.id,
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
                        guild.id,
                        "general",
                        "Error: El bot no tiene permiso para enviar mensajes",
                    )
                else:
                    log.error("Unknown error on task birthday: {}".format(error))
                    await self.bot.channel_send(
                        guild.id, "general", "Error desconocido, contacta al creador"
                    )

    @tasks.loop(minutes=5)
    async def discord_status(self):
        r = requests.get("https://discordstatus.com/api/v2/summary.json")
        data = r.json()

        for guild in self.bot.guilds:
            con = create_connection(str(guild.id))

            for incident in data["incidents"]:

                incident_id = incident["id"]
                incident_name = incident["name"]
                incident_status = incident["status"]
                embed = nextcord.Embed(title="Discord Status", color=0x00FF00)
                embed.description = "Hay un incidente en discord"
                embed.add_field(name="Incidente", value=incident_name)
                embed.add_field(name="Estado", value=incident_status)
                embed.add_field(name="ID", value=incident_id)

                # Inform about a new incident
                if not check_record_in_database(con, incident_id):
                    create_record(con, ["incident", incident_id])
                    await self.bot.channel_send(guild.id, "audit", "a", embed)

                # Inform about an incident update

                for update in incident["incident_updates"]:

                    update_id = update["id"]
                    update_body = update["body"]
                    update_status = update["status"]
                    update_embed = nextcord.Embed(
                        title="Actualización incidente", color=0x00FF00
                    )
                    update_embed.add_field(name="ID", value=update_id, inline=False)
                    update_embed.add_field(
                        name="Actualización", value=update_body, inline=False
                    )
                    update_embed.add_field(
                        name="Estado", value=update_status, inline=False
                    )
                    if not check_record_in_database(con, update_id):
                        create_record(con, ["incident", update_id])
                        await self.bot.channel_send(
                            guild.id, "audit", "a", update_embed
                        )

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
