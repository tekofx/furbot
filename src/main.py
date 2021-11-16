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
env_vars = [
    "DISCORD_TOKEN",
    "VILLAFURRENSE",
    "GENERAL_CHANNEL",
    "MEMES_CHANNEL",
    "AUDIT_CHANNEL",
    "REDDIT_CLIENT_ID",
    "REDDIT_CLIENT_SECRET",
    "REDDIT_USER_AGENT",
    "TWITTER_CONSUMER_KEY",
    "TWITTER_CONSUMER_SECRET",
    "TWITTER_ACCESS_TOKEN",
    "TWITTER_ACCESS_TOKEN_SECRET",
]


# Remove previous env variables from environment
# and check if any missing env variable
for var in env_vars:
    if var in os.environ:
        del os.environ[var]
    else:
        log.error(
            colorama.Fore.RED
            + "Error: Missing environmental variable {} in .env file".format(var)
        )
        sys.exit()


if "-t" in sys.argv:
    print(colorama.Fore.MAGENTA + "Executing in TEST mode")
    load_dotenv("src/utils/tests.env")
else:
    print(colorama.Fore.MAGENTA + "Executing in NORMAL mode")

    load_dotenv("src/utils/.env")

token = os.getenv("DISCORD_TOKEN")
bot = Bot(token)
bot.run()
