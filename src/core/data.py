import os
from core import logger
import nextcord
import json


log = logger.getLogger(__name__)

data_path = "data/"
server_path = data_path + "servers/{guild_id} - {guild_name}/"

# Resources
resources_path = data_path + "resources/"
meme_resources_path = resources_path + "memes/"
config_json = resources_path + "config.json"


class Data:
    def __init__(self, guild: nextcord.Guild) -> None:
        self.guild = guild

        self.server_path = server_path.format(guild_name=guild.name, guild_id=guild.id)

        # Info folders
        self.temp_path = self.server_path + "temp/"
        self.stickers_path = self.server_path + "stickers/"
        self.memes_path = self.server_path + "memes/"

        # Paths
        self._folders = [
            data_path,
            self.server_path,
            self.temp_path,
            self.stickers_path,
            self.memes_path,
        ]

        # Datafiles
        self._files = [config_json]

    @property
    def files(self) -> list:
        """Returns a list containing all files

        Returns:
            list
        """
        return self._files

    @property
    def folders(self) -> list:
        """Returns a list containing all folders

        Returns:
            list
        """
        return self._folders

    def setup_folders(self) -> None:
        """Creates needed folders if they not exists"""
        for folder in self._folders:
            if not os.path.isdir(folder):
                log.warning("Folder {} not exists, creating it".format(folder))
                os.makedirs(folder)
                log.warning("Folder {} created".format(folder))
            else:
                log.info("Folder {} exists".format(folder))

    def setup_files(self) -> None:
        """Creates needed files if they not exists"""
        for file in self._files:

            if not os.path.isfile(file):
                log.warning("file {} not exists, creating it".format(file))
                fp = open(file, "x")
                fp.close()
                if file == config_json:
                    dictionary = {"activity": "online"}

                with open(config_json, "w") as outfile:
                    json.dump(dictionary, outfile)

        # Create a JSON file with server info
        if not os.path.isfile(self.server_path + "server.json"):
            var = {
                "name": self.guild.name,
                "id": self.guild.id,
                "created_at": str(self.guild.created_at),
                "owner": {
                    "name": self.guild.owner.name,
                    "id": self.guild.owner.id,
                },
            }

            with open(self.server_path + "server.json", "w") as f:
                f.write(json.dumps(var))


def get_server_path(guild: nextcord.Guild) -> str:
    """Returns the server path

    Returns:
        str
    """
    return server_path.format(guild_name=guild.name, guild_id=guild.id)


def get_config() -> dict:
    """Gets info from config file

    Returns:
        dict: all config values
    """

    with open(config_json) as f:
        data = json.load(f)

    return data


def get_activity() -> str:
    """Gets activity from config

    Returns:
        str: activity
    """

    activity = ""

    with open(config_json) as f:
        data = json.load(f)
        activity = data["activity"]

    return activity
