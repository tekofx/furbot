import os
import setproctitle
from dotenv import load_dotenv
import sys
from core.bot import Bot
from core import logger

# Set logs
log = logger.getLogger("main")

# Set workdir
path = os.path.dirname(os.path.abspath(__file__))
working_dir = os.path.dirname(path)
os.chdir(working_dir)

# Set process name
setproctitle.setproctitle("furbot")


if "-t" in sys.argv:
    log.info("Executing in TEST mode")
    load_dotenv("dev.env")
else:
    log.info("Executing in NORMAL mode")


bot = Bot(os.environ["DISCORD_TOKEN"])
bot.run()
