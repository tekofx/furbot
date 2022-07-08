import os
import setproctitle
from dotenv import load_dotenv
import sys
from utils.bot import Bot
from utils import logger

# Set logs
log = logger.getLogger("main")

# Set workdir
path = os.path.dirname(os.path.abspath(__file__))
working_dir = os.path.dirname(path)
os.chdir(working_dir)

# Set process name
setproctitle.setproctitle("furbot")

# Env variables
env_vars = [
    "DISCORD_TOKEN",
    "VILLAFURRENSE",
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
        try:
            os.getenv(var)
        except Exception as error:
            log.error(
                "Error: Missing environmental variable {} in .env file".format(var)
            )
            sys.exit()


if "-t" in sys.argv:
    log.info("Executing in TEST mode")
    load_dotenv("env/tests.env")
else:
    log.info("Executing in NORMAL mode")

    load_dotenv("env/furbot.env")

token = os.getenv("DISCORD_TOKEN")
bot = Bot(token)
bot.run()
