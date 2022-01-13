import os
import logging

log = logging.getLogger(__name__)

data_path = "data/"
resources_path = data_path + "resources/"
meme_resources_path = resources_path + "memes/"
config_yaml = resources_path + "config.yaml"
databases_path = data_path + "databases/"
stickers_path = data_path + "stickers/"
memes_path = data_path + "memes/"


insults_txt = resources_path + "insults.txt"
reddit_memes_history_txt = resources_path + "reddit_memes_history.txt"
animos_txt = resources_path + "animos.txt"
memes_history_txt = resources_path + "memes_history.txt"
jojos_txt = resources_path + "jojos.txt"


class Data:
    def __init__(self) -> None:
        # Paths
        self._folders = [
            data_path,
            memes_path,
            stickers_path,
            databases_path,
            resources_path,
            meme_resources_path,
        ]

        # Datafiles
        self._files = [
            jojos_txt,
            animos_txt,
            insults_txt,
            memes_history_txt,
            reddit_memes_history_txt,
        ]

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
                os.mkdir(folder)
            else:
                log.info("Folder {} exists".format(folder))

    def setup_files(self) -> None:
        """Creates needed files if they not exists"""
        for file in self._files:
            if not os.path.isfile(file):
                log.warning("file {} not exists, creating it".format(file))
                fp = open(file, "x")
                fp.close()
