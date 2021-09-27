import lightbulb
import hikari
from importlib import import_module
from pathlib import Path
import os
from dotenv import load_dotenv


class Bot(lightbulb.Bot):
    def __init__(self, discord_token: str) -> None:

        super().__init__(
            prefix="-",
            token=discord_token,
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

    def run(self):
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)

        super().run()


if os.name != "nt":
    import uvloop

    uvloop.install()

load_dotenv()
token = os.getenv("DISCORD_TOKEN_HIKARI")
bot = Bot(token)

bot.run()
