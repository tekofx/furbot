import os
import setproctitle
from dotenv import load_dotenv
from utils.bot import Bot
import sys
import logging
import colorama

log = logging.getLogger("main")


if os.name != "nt":
    import uvloop

    uvloop.install()


# Set workdir
path = os.path.dirname(os.path.abspath(__file__))
working_dir = os.path.dirname(path)
os.chdir(working_dir)

# Set process name
setproctitle.setproctitle("furbot")
del os.environ["DISCORD_TOKEN"]
del os.environ["VILLAFURRENSE"]
del os.environ["GENERAL_CHANNEL"]
del os.environ["MEMES_CHANNEL"]
del os.environ["AUDIT_CHANNEL"]


if "-t" in sys.argv:
    print(colorama.Fore.MAGENTA + "Executing in TEST mode")
    load_dotenv("src/utils/tests.env")
else:
    print(colorama.Fore.MAGENTA + "Executing in NORMAL mode")

    load_dotenv("src/utils/.env")

token = os.getenv("DISCORD_TOKEN")
bot = Bot(token)
bot.run()
