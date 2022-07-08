import logging
import coloredlogs


def get_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)
    return logger


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self):
        super().__init__()
        self.fmt = f"{self.blue}%(asctime)s {self.reset} {self.yellow}%(levelname)s{self.reset} {self.red}%(name)s{self.reset} %(message)s"
        self.FORMATS = {
            logging.DEBUG: self.fmt + self.reset,
            logging.INFO: self.fmt + self.reset,
            logging.WARNING: self.fmt + self.reset,
            logging.ERROR: self.fmt + self.reset,
            logging.CRITICAL: self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
