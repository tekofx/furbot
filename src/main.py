import os
import setproctitle
from dotenv import load_dotenv
import sys
import coloredlogs, logging, colorama
from utils.bot import Bot

coloredlogs.install()
log = logging.getLogger(__name__)
log.setLevel("INFO")

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
    "LOBBY_CHANNEL",
    "REDDIT_CLIENT_ID",
    "REDDIT_CLIENT_SECRET",
    "REDDIT_USER_AGENT",
    "TWITTER_CONSUMER_KEY",
    "TWITTER_CONSUMER_SECRET",
    "TWITTER_ACCESS_TOKEN",
    "TWITTER_ACCESS_TOKEN_SECRET",
]
print('a')

# Check for folders
folders = [
    "databases/",
    "files/memes/",
    "files/resources/data/",
    "files/resources/memes/",
    "files/resources/utilities/",
    "files/stickers",
]
for folder in folders:
    if not os.path.isdir(folder):
        log.warning("Folder {} not exists, creating it".format(folder))
        os.mkdir(folder)
    else:
        log.info("Folder {} exists".format(folder))

# Check for files
files = [
    "files/resources/data/insults.txt",
    "files/resources/data/reddit_memes_history.txt",
    "files/resources/data/animos.txt",
    "files/resources/data/memes_history.txt",
    "files/resources/data/jojos.txt",
]
for file in files:
    if not os.path.isfile(file):
        log.warning("file {} not exists, creating it".format(file))
        fp = open(file, "x")
        fp.close()

# Remove previous env variables from environment
# and check if any missing env variable

for var in env_vars:
    if var in os.environ:
        del os.environ[var]
    else:
        try:
            os.getenv(var)
        except:
            log.error(
                "Error: Missing environmental variable {} in .env file".format(var)
            )
            sys.exit()
print(os.environ)
print(os.path.isfile("env/furbot.env"))

if "-t" in sys.argv:
    print(colorama.Fore.MAGENTA + "Executing in TEST mode")
    load_dotenv("env/furbot.env")
else:
    print(colorama.Fore.MAGENTA + "Executing in NORMAL mode")

    load_dotenv("env/furbot.env")

token = os.getenv("DISCORD_TOKEN")
bot = Bot(token)
bot.run()
