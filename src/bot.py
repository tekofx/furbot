from hikari import intents
import lightbulb
import hikari
from importlib import import_module
from pathlib import Path
import os
from dotenv import load_dotenv
from functions import yaml_f
import setproctitle


class Bot(lightbulb.Bot):
    def __init__(self, discord_token: str) -> None:

        super().__init__(
            prefix=["fur ", "Fur ", "FUR "],
            token=discord_token,
            intents=hikari.Intents.GUILD_MEMBERS
            | hikari.Intents.GUILDS
            | hikari.Intents.GUILD_MESSAGES,
        )

    async def on_starting(self, event: hikari.StartingEvent):
        pass

    async def on_started(self, event: hikari.StartedEvent):
        commands = Path("./src/slash_commands").glob("*.py")
        plugins = Path("./src/plugins").glob("*.py")

        """ for c in commands:
            mod = import_module(f"slash_commands.{c.stem}")
            mod.load(self) """

        for c in plugins:
            mod = import_module(f"plugins.{c.stem}")
            mod.load(self)

        # Set activity
        activity = hikari.Activity(name=yaml_f.get_activity())
        await self.update_presence(activity=activity)

    def run(self):
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)

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

# Run bot
bot = Bot(token)
bot.run()
