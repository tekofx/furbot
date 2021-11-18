# Contains all functions that are not commands
from PIL import Image
import os
import logging
from dotenv import load_dotenv
import praw
import random
import requests
import yaml
import lightbulb
import hikari


class yaml_functions:
    def __init__(self, yaml_file=None):
        if yaml_file is None:
            self.yaml_file = "files/resources/config.yaml"
        else:
            self.yaml_file = yaml_file

    def set_yaml_file(self, yaml_file: str):
        """Sets the yaml file

        Args:
            yaml_file (str): file
        """
        self.yaml_file = yaml_file

    def get_content_yaml(self):
        """Gets the content of yaml_file

        Returns:
            any: content of yaml_file
        """
        with open(self.yaml_file, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print("Error loading YAML: " + exc)

    def get_ranks_ids(self):
        """Get ranks ids

        Returns:
            list: list of ranks ids
        """
        content = self.get_content_yaml()
        output = []
        for x, y in content["ranks"].items():
            output.append(y)

        return output

    def get_activity(self):
        """Gets activity from yaml_file

        Returns:
            str: activity name
        """
        content = self.get_content_yaml()
        return content["activity"]

    def change_activity(self, activity: str):
        """Edits the activity of yaml_file

        Args:
            activity (str): name of the activity
        """
        with open(self.yaml_file, "r") as f:
            content = yaml.safe_load(f)
            content["activity"] = activity
        with open(self.yaml_file, "w") as f:
            yaml.dump(content, f, allow_unicode=True)


yaml_f = yaml_functions()

# .env data
load_dotenv()
magnet_id = int(os.getenv("MAGNET"))
angel_id = int(os.getenv("ANGEL"))


# Paths
stickers_path = "files/stickers/"
meme_templates_path = "files/resources/memes/"
meme_path = "files/memes/"
paths = [stickers_path, meme_path]

# Datafiles
insults_txt = "files/resources/data/insults.txt"
reddit_memes_history_txt = "files/resources/data/reddit_memes_history.txt"
animos_txt = "files/resources/data/animos.txt"
memes_history_txt = "files/resources/data/memes_history.txt"
jojos_txt = "files/resources/data/jojos.txt"
files = [
    insults_txt,
    reddit_memes_history_txt,
    animos_txt,
    memes_history_txt,
    jojos_txt,
]

stickerSize = 500

separator = "       "  # key word to distinguish separator roles

# Creation of reddit
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    check_for_async=False,
)


def setup_logs():
    """Set up the logs"""
    logging.basicConfig(
        filename="src/logs",
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    logging.info("\n\n\nStarted furbot")


def setup_directories():
    """Creates needed directories"""
    for path in paths:
        if not os.path.isdir(path):
            print("directory ", path, " not exists, creating it")

            os.mkdir(path)


def setup_files():
    """Creates needed directories"""
    for file in files:
        if not os.path.isfile(file):
            print("file ", file, " not exists, creating it")
            fp = open(file, "x")
            fp.close()


def get_user_avatar(url: str, name: str):
    """Downloads the avatar of a user

    Args:
        user (hikari.User): user to download avatar from
        name (str): user to download avatar from
    """

    r = requests.get(url, allow_redirects=True)

    open(meme_templates_path + name, "wb").write(r.content)

    logging.info("Saved avatar with url " + url + " in " + meme_templates_path)


def convert_pic(picture: str, imgName: str, imgSize: str = None):
    """Converts an image to PNG with a differents size

    Args:
        picture (str): picture to convert
        imgName (str): exported picture name
        imgSize (str): exported image size
    """
    img = Image.open(picture)

    if imgSize is not None:
        wpercent = imgSize / float(img.size[0])
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((imgSize, hsize), Image.ANTIALIAS)

    img.save(meme_templates_path + imgName + ".png")


def get_user(ctx: lightbulb.Context, user: hikari.User = None):
    """Gets user from a message

    Args:
        context (Message): Message to get an avatar
        user (hikari.User, optional): User of a message. Defaults to None.

    Returns:
        hikari.User: user
    """
    if user is None:
        output = ctx.author
    else:
        output = user

    return output


############################# Carnet functions ##############################


############################### Reddit functions ###############################
def get_hot_subreddit_image(
    sub_reddit: str,
    posts_limit: int,
    history_file: str,
    not_flair: str = None,
):
    """Get a hot subreddit post image

    Args:
        sub_reddit (str): subreddit to get the image from
        posts_limit (int): maxium number of posts to get
        history_file (str): file to save the posts that where
        not_flair (str): flair not present in post

    Returns:
        str: url of image
    """
    posts = reddit.subreddit(sub_reddit).hot(limit=posts_limit)
    try:
        for post in posts:
            if post.over_18 is False:  # Check if post is SFW

                if not_flair is None:

                    if post.url.endswith("jpg") and not exists_string_in_file(
                        history_file, post.url
                    ):
                        write_in_file(history_file, post.url + "\n")
                        return post.url
                else:
                    if (
                        (not post.link_flair_text or not_flair in post.link_flair_text)
                        and post.url.endswith("jpg")
                        and not exists_string_in_file(history_file, post.url)
                    ):
                        write_in_file(history_file, post.url + "\n")
                        return post.url

    except Exception as error:
        logging.error("Error in get_hot_subreddit_image: {}".format(error))
        return "Error: {}".format(error)


############################### Files functions ###############################
def exists_string_in_file(file_name: str, string: str):
    """Checks if string is contained as line in file_name

    Args:
        file_name (str): file to check
        string (str): string to search

    Returns:
        bool: True if string is in file_name, False if not
    """
    with open(file_name, "r") as file:
        for line in file:
            if string + "\n" == line:
                return True
    return False


def count_lines_in_file(file: str):
    """Counts lines of a file

    Args:
        file (str): file to count lines from

    Returns:
        int: number of lines
    """
    output = 0
    with open(file, "r") as f:
        for line in f:
            output += 1
    return output


def count_files_in_dir(directory: str):
    """Counts files in a directory

    Args:
        directory (str): directory to count files from

    Returns:
        int: number of files in directory
    """
    files = os.listdir(directory)  # dir is your directory path
    output = len(files)
    return output


def get_files_in_directory(directory: str):
    """Get a list of files in a directory

    Args:
        directory (str): directory to search

    Returns:
        [list]: list of files in dir
    """
    return os.listdir(directory)


def write_in_file(file: str, string: str):
    """Writes text in a file

    Args:
        file (str): file to write
        string (str): string to write
    """
    f = open(file, "a")
    f.write(string)
    f.close()


def get_random_line_of_file(file: str):
    """Gets random line of a file

    Args:
        file (str): file to get the line

    Returns:
        [str]: random line
    """
    with open(file) as f:
        lines = f.readlines()
    f.close()

    return random.choice(lines)


def delete_files(elements: list):
    """Delete files needed to create a meme

    Args:
        elements (list): files used in a meme
    """
    for x in elements:
        if os.path.isfile(meme_templates_path + x):
            os.remove(meme_templates_path + x)
    logging.info("Removed dependencies")
