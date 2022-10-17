import logging


def getLogger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)
    return logger


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
    RESET = "\x1b[0m"

    def __init__(self):
        super().__init__()
        self.fmt = (
            f"{self.GREEN}%(asctime)s{self.RESET} {self.PURPLE}%(name)s{self.RESET} "
        )
        self.fmt_guild = (
            f"{self.GREEN}%(asctime)s{self.RESET} {self.PURPLE}%(name)s{self.RESET} "
        )

        self.FORMATS = {
            logging.DEBUG: self.fmt
            + f"{self.BLUE}%(levelname)s{self.RESET} %(message)s",
            logging.INFO: self.fmt
            + f"{self.BLUE}%(levelname)s{self.RESET} %(message)s",
            logging.WARNING: self.fmt
            + f"{self.YELLOW }%(levelname)s{self.RESET} %(message)s",
            logging.ERROR: self.fmt
            + f"{self.LIGHT_RED}%(levelname)s{self.RESET} %(message)s",
            logging.CRITICAL: self.fmt
            + f"{self.RED}%(levelname)s{self.RESET} %(message)s",
        }
        self.FORMATS_GUILD = {
            logging.DEBUG: self.fmt_guild
            + f"{self.BLUE}%(levelname)s{self.RESET} {self.YELLOW}%(guild)s{self.RESET} %(message)s",
            logging.INFO: self.fmt_guild
            + f"{self.BLUE}%(levelname)s{self.RESET} {self.YELLOW}%(guild)s{self.RESET} %(message)s",
            logging.WARNING: self.fmt_guild
            + f"{self.YELLOW}%(levelname)s{self.RESET} {self.YELLOW}%(guild)s{self.RESET} %(message)s",
            logging.ERROR: self.fmt_guild
            + f"{self.LIGHT_RED}%(levelname)s{self.RESET} {self.YELLOW}%(guild)s{self.RESET} %(message)s",
            logging.CRITICAL: self.fmt_guild
            + f"{self.RED}%(levelname)s{self.RESET} {self.YELLOW}%(guild)s{self.RESET} %(message)s",
        }

    def format(self, record):
        if "guild" in record.__dict__:
            log_fmt = self.FORMATS_GUILD.get(record.levelno)
        else:
            log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
