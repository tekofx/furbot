from hikari import Intents
import lightbulb
import hikari
from importlib import import_module
from pathlib import Path
import os
import logging
from utils.functions import yaml_f
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.events import EVENT_JOB_ERROR
import plugins.tasks as tasks
from utils.database import (
    create_connection,
    create_user,
    get_times_joined,
    set_times_joined,
    setup_database,
)

MAX_JOINED_TIMES = 3

log = logging.getLogger(__name__)


class Bot(lightbulb.Bot):
    def __init__(self, discord_token: str) -> None:
        super().__init__(
            prefix=["fur ", "Fur ", "FUR "],
            token=discord_token,
            logs=None,
            intents=Intents.GUILD_MEMBERS
            | Intents.GUILDS
            | Intents.GUILD_MESSAGES
            | Intents.GUILD_BANS
            | Intents.DM_MESSAGES,
        )
        self.scheduler = AsyncIOScheduler()

    async def on_new_guild_message(self, event: hikari.GuildMessageCreateEvent):
        if event.content and not event.message.author.is_bot:  # If message has text
            if "uwu" in event.content.lower():
                await event.message.respond("UwU")

            if "owo" in event.content.lower():
                await event.message.respond("OwO")

            if "7w7" in event.content.lower():
                await event.message.respond(":eyes:")

            if "vaca " in event.content.lower():
                await event.message.respond("Muu!")

            if "vacas" in event.content.lower():
                await event.message.respond("Muu muuu!")

    async def on_new_member(self, event: hikari.MemberCreateEvent):

        log.info("User {} joined VF".format(event.member.username))
        con = create_connection(event.guild_id)
        new_member = event.member
        times_joined = get_times_joined(con, new_member.id)

        if not event.member.is_bot:

            # If user not in user list add it
            if times_joined == 0:
                log.info(
                    "User {} not exists in user list".format(event.member.username)
                )
                user_data = [
                    new_member.id,
                    new_member.username,
                    new_member.joined_at,
                    1,
                ]
                create_user(con, user_data)
                log.info("User {} added to list".format(new_member.username))
                message = "Se ha unido el usuario {}. Veces que se ha unido: {}".format(
                    new_member.username, str(times_joined + 1)
                )

            elif times_joined < MAX_JOINED_TIMES:
                # increase
                set_times_joined(con, new_member.id, times_joined + 1)
                log.info(
                    "User {} already in list, increasing its joined times to {}".format(
                        event.member.username, times_joined + 1
                    )
                )
                message = "Se ha unido el usuario {}. Veces que se ha unido: {}".format(
                    event.member.username, str(times_joined + 1)
                )
            else:
                # Ban user
                user_name = event.member.username
                await event.member.ban(reason="Se unió y salió del server 3 veces")

                message = (
                    "Se ha baneado al usuario {} por unirse e irse {} veces".format(
                        user_name, str(MAX_JOINED_TIMES)
                    )
                )

                log.info(
                    "User {} banned due to exceading max times of joins".format(
                        event.member.username
                    )
                )

            await self.audit_channel.send(message)

    def tasks_listener(self, event):
        log.error("Error in tasks")

        try:
            log.info("Removing tasks")
            self.scheduler.remove_all_jobs(jobstore="default")

        except Exception as error:
            message = "Error while restarting scheduler: {}".format(error)
            log.error(message)

        try:
            log.info("Reloading tasks plugin")
            tasks.unload(self)
            tasks.load(self)
        except Exception as error:
            message = "Error while loading tasks plugin: {}".format(error)
            log.error(message)

        else:
            log.info("Loaded tasks plugin successfully")

    async def on_leave_member(self, event: hikari.MemberDeleteEvent):
        pass

    async def on_starting(self, event: hikari.StartingEvent):
        log.info("Starting event")

        # Fetch bot owners users
        await self.fetch_owner_ids()
        owners = []
        for owner_id in self.owner_ids:
            user = await self.rest.fetch_user(owner_id)
            owners.append(user)
        self.owners = owners

        # Load commands
        log.info("Loading slash commands")
        commands = Path("./src/slash_commands").glob("*.py")
        for c in commands:
            mod = import_module(f"slash_commands.{c.stem}")
            mod.load(self)
            log.info(f"Loaded slash commands from {c.stem}")

        # Get channels and server
        log.info("Fetching needed channels")
        self.general_channel = await self.rest.fetch_channel(
            os.getenv("GENERAL_CHANNEL")
        )
        log.info("Loaded general channel")
        self.memes_channel = await self.rest.fetch_channel(os.getenv("MEMES_CHANNEL"))
        log.info("Loaded memes channel")
        self.audit_channel = await self.rest.fetch_channel(os.getenv("AUDIT_CHANNEL"))
        log.info("Loaded audit channel\n")
        self.server = await self.rest.fetch_guild(os.getenv("VILLAFURRENSE"))

    async def on_started(self, event: hikari.StartedEvent):
        log.info("Started event")

        # Load plugins
        plugins = Path("./src/plugins").glob("*.py")
        for c in plugins:

            mod = import_module(f"plugins.{c.stem}")
            mod.load(self)
            log.info(f"Loaded plugin {c.stem}")

        # Start scheduler
        self.scheduler.start()
        self.scheduler.add_listener(self.tasks_listener, EVENT_JOB_ERROR)

        # Set activity
        activity = hikari.Activity(name=yaml_f.get_activity())
        await self.update_presence(activity=activity)
        log.info("Set activity to: " + activity.name)

        # Set database
        log.info("Database configured")
        guilds = self.rest.fetch_my_guilds().enumerate()
        async for num, guild in guilds:
            server = str(guild.id)
            con = setup_database(server)

    async def on_command_invoked(self, event: lightbulb.events.CommandInvocationEvent):
        user = event.context.author.username
        log.info(user + " used command " + event.command.name)

    async def on_stopping(self, event: hikari.StoppingEvent):
        log.info("Stopping bot")

        # Stop scheduler
        self.scheduler.shutdown()

    def run(self):
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(
            hikari.GuildMessageCreateEvent, self.on_new_guild_message
        )
        self.event_manager.subscribe(
            lightbulb.events.CommandInvocationEvent, self.on_command_invoked
        )
        self.event_manager.subscribe(hikari.MemberCreateEvent, self.on_new_member)
        self.event_manager.subscribe(hikari.MemberDeleteEvent, self.on_leave_member)

        super().run()
