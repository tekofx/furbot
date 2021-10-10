from hikari import Intents
import lightbulb
import hikari
from importlib import import_module
from pathlib import Path
import os
from dotenv import load_dotenv
from functions import yaml_f
import setproctitle
import logging


log = logging.getLogger(__name__)


class Bot(lightbulb.Bot):
    def __init__(self, discord_token: str) -> None:

        super().__init__(
            prefix=["fur", "Fur", "FUR"],
            token=discord_token,
            intents=Intents.GUILD_MEMBERS | Intents.GUILDS | Intents.GUILD_MESSAGES,
        )

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
        pass

    async def on_starting(self, event: hikari.StartingEvent):
        # Load commands
        commands = Path("./src/slash_commands").glob("*.py")
        for c in commands:
            mod = import_module(f"slash_commands.{c.stem}")
            mod.load(self)
            log.info(f"Loaded slash commands from {c.stem}")

    async def on_started(self, event: hikari.StartedEvent):
        # Load plugins
        plugins = Path("./src/plugins").glob("*.py")
        for c in plugins:

            mod = import_module(f"plugins.{c.stem}")
            mod.load(self)
            log.info(f"Loaded plugin {c.stem}")

        # Set activity
        activity = hikari.Activity(name=yaml_f.get_activity())
        await self.update_presence(activity=activity)
        log.info("Set activity to: " + activity.name)

    async def on_command_invoked(self, event: lightbulb.events.CommandInvocationEvent):
        user = event.context.author.username
        log.info(user + " used command " + event.command.name)

    def run(self):
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(
            hikari.GuildMessageCreateEvent, self.on_new_guild_message
        )
        self.event_manager.subscribe(
            lightbulb.events.CommandInvocationEvent, self.on_command_invoked
        )

        super().run()


if os.name != "nt":
    import uvloop

    uvloop.install()

# Get .env
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

# Set workdir
path = os.path.dirname(os.path.abspath(__file__))
working_dir = os.path.dirname(path)
os.chdir(working_dir)

# Set process name
setproctitle.setproctitle("furbot")

bot = Bot(token)
bot.run()
