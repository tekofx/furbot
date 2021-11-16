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

        times_joined = yaml_f.get_times_joined(int(event.member.id))
        log.info("User {} joined VF".format(event.member.username))

        if not event.member.is_bot:

            # If user not in user list add it
            if times_joined == 0:
                log.info(
                    "User {} not exists in user list".format(event.member.username)
                )
                user_data = {
                    "name": event.member.username,
                    "times_joined": 1,
                    "joined_date": event.member.joined_at,
                }
                yaml_f.add_user_to_user_list(int(event.member.id), user_data)
                log.info("User {} added to list".format(event.member.username))
                message = "Se ha unido el usuario {}. Veces que se ha unido: {}".format(
                    event.member.username, str(times_joined + 1)
                )

            elif times_joined < MAX_JOINED_TIMES:
                # increase
                yaml_f.increase_joined_times(event.member)
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

    async def send_DM_to_owners(self, message):
        for owner in self.owners:
            await owner.send(message)

    async def tasks_listener(self, event):
        log.error("Error in tasks, restarting them")
        self.remove_plugin("Tasks")
        log.info("Removed tasks plugin")
        try:
            log.info("Restarting scheduler")
            self.scheduler.shutdown()
            self.scheduler.start()

        except Exception as error:
            message = "Error while restarting scheduler: {}".format(error)
            log.error(message)
            await self.send_DM_to_owners(message)

        try:
            log.info("Loading tasks plugin")
            tasks.load(self)
        except Exception as error:
            message = "Error while loading tasks plugin: {}".format(error)
            log.error(message)
            await self.send_DM_to_owners(message)

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

        # Get channels
        log.info("Fetching needed channels")
        self.general_channel = await self.rest.fetch_channel(
            os.getenv("GENERAL_CHANNEL")
        )
        log.info("Loaded general channel")
        self.memes_channel = await self.rest.fetch_channel(os.getenv("MEMES_CHANNEL"))
        log.info("Loaded memes channel")
        self.audit_channel = await self.rest.fetch_channel(os.getenv("AUDIT_CHANNEL"))
        log.info("Loaded audit channel\n")

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


def build_logger(name=__name__, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    file_handler = logging.FileHandler("bot.log", mode="a")
    file_handler.setLevel(level)

    formatter = logging.Formatter(
        fmt="{levelname} - {asctime} in {name}:\n{message}",
        datefmt="%b %d %H:%M:%S",
        style="{",
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
