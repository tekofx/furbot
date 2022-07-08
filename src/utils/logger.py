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

    grey = "\x1b[38;21m"
    green = "\033[32m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self):
        super().__init__()
        self.fmt = f"{self.green}%(asctime)s{self.reset} {self.blue}%(levelname)s{self.reset} {self.red}%(name)s{self.reset} %(message)s"
        self.fmt_guild = f"{self.green}%(asctime)s{self.reset} {self.blue}%(levelname)s{self.reset} {self.red}%(name)s{self.reset} {self.yellow}%(guild)s{self.reset} %(message)s"

        self.FORMATS = {
            logging.DEBUG: self.fmt + self.reset,
            logging.INFO: self.fmt + self.reset,
            logging.WARNING: self.fmt + self.reset,
            logging.ERROR: self.fmt + self.reset,
            logging.CRITICAL: self.fmt + self.reset,
        }
        self.FORMATS_GUILD = {
            logging.DEBUG: self.fmt_guild + self.reset,
            logging.INFO: self.fmt_guild + self.reset,
            logging.WARNING: self.fmt_guild + self.reset,
            logging.ERROR: self.fmt_guild + self.reset,
            logging.CRITICAL: self.fmt_guild + self.reset,
        }

    def format(self, record):
        if "guild" in record.__dict__:
            log_fmt = self.FORMATS_GUILD.get(record.levelno)
        else:
            log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
