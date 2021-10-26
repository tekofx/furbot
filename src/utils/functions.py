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

    def get_ranks(self):
        """Get ranks names

        Returns:
            list: list of ranks names
        """
        content = self.get_content_yaml()
        output = []
        for x, y in content["ranks"].items():
            output.append(x)

        return output

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

    def get_colors(self):
        """Get colors names

        Returns:
            list: containing color names
        """
        content = self.get_content_yaml()
        output = []
        for key, value in content["colors"].items():
            output.append(key)
        return output

    def get_color_code(self, color: str):
        """Gets color code of a color

        Args:
            color (str): color name

        Returns:
            list: contains RGB values
        """
        content = self.get_content_yaml()

        for key, value in content["colors"].items():
            if key == color:
                output = value.split(" ")
                # Delete \n from last element
                output = [s.replace("\n", "") for s in output]

                # Convert all elements into int
                output = list(map(int, output))
                return output

    def get_species(self):
        """Gets species

        Returns:
            list: contains species names
        """
        content = self.get_content_yaml()
        output = []
        for x in content["species"]:
            output.append(x)

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

    def get_cumpleaños(self):
        """Gets birthdays from YAML file

        Returns:
            list: containing 3 lists
                - user names
                - user ids
                - dates
        """
        content = self.get_content_yaml()
        output = []
        user_names = []
        dates = []
        user_ids = []
        for entry in content["birthdays"].items():
            user_names.append(entry[0])
            for key, value in entry[1].items():
                dates.append(key)
                user_ids.append(value)
        output.append(user_names)
        output.append(user_ids)
        output.append(dates)
        return output

    def set_user_list(self, data: dict):
        """Set user list of Villafurrense server

        Args:
            data (dict): dict containing usernames and user ids
        """

        with open(self.yaml_file, "r") as yml:
            content = yaml.safe_load(yml)
            del content["user_list"]
            data = {"user_list": data}
            content.update(data)
        with open(self.yaml_file, "w") as f:
            yaml.dump(content, f, allow_unicode=True)

    def add_birthday(self, user_id: int, user_name: str, date: str):
        """Adds a birthday to the yaml_file
        Args:
            user_id(int): user id
            user_name (str): user name
            date (str): birthday with format dd-mm
        """
        date = date.split("-")
        day = date[0]
        month = date[1]
        if len(day) == 1:
            day = "0" + day
        if len(month) == 1:
            month = "0" + month

        date = month + "-" + day
        with open(self.yaml_file, "r") as yml:
            content = yaml.safe_load(yml)
            aux = content["birthdays"]
            data = {user_name: {date: user_id}}
            aux.update(data)

        with open(self.yaml_file, "w") as f:
            yaml.dump(content, f, allow_unicode=True)

    def add_species(self, specie_name: str, specie_id: int):
        """Adds an specie to yaml_file

        Args:
            specie_name (str): name of specie
            specie_id (int): id of specie role
        """
        with open(self.yaml_file, "r") as yml:
            content = yaml.safe_load(yml)
            aux = content["species"]
            data = {str(specie_name): int(specie_id)}
            aux.update(data)
        with open(self.yaml_file, "w") as f:
            yaml.dump(content, f, allow_unicode=True)

    def add_rank(self, rank_name: str, rank_id: int):
        # TODO: Implement
        pass

    def remove_species(self, specie_name: str, specie_id: int):
        # TODO: Implement
        pass

    def remove_rank(self, rank_name: str, rank_id: int):
        # TODO: Implement
        pass


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


def create_meme(
    pictures: list, avatar_url: str, avatar_size: int, position: list, invert: bool
):
    """Crea un meme

    Args:
        pictures (list): lista de imagenes, siendo pictures[0] el meme y el resto avatares
        avatar_url (str): url del avatar a añadir al meme
        avatar_size (int): tamañao al que convertir el avatar de webp a png
        position (list): posiciones en las que colocar las imagenes, siendo position[0] y position[1] la x,y del meme
        invert (bool): Si es True usa el meme como canvas, en caso contrario, usa el avatar
    """

    r = requests.get(avatar_url, allow_redirects=True)
    open(meme_templates_path + "01.webp", "wb").write(r.content)

    # Convert avatar
    convert_pic(meme_templates_path + "01.webp", "01", avatar_size)

    if not invert:  # burn
        canvas = pictures[1]
        width, height = (
            Image.open(meme_templates_path + canvas + ".png").convert("RGBA").size
        )
    else:  # cringe
        canvas = pictures[0]
        width, height = (
            Image.open(meme_templates_path + canvas + ".png").convert("RGBA").size
        )

    output = Image.new("RGBA", (width, height))  # Create picture
    meme = Image.open(meme_templates_path + pictures[0] + ".png").convert(
        "RGBA"
    )  # Open meme picture

    # Add avatar pictures
    i = 2
    for x in pictures[1:]:
        img = Image.open(meme_templates_path + x + ".png").convert("RGBA")
        output.paste(img, (position[i], position[i + 1]), img)
        i += 2

    # Add meme picture
    output.paste(meme, (position[0], position[1]), meme)

    # Save final meme
    output.save(meme_templates_path + "output.png", "PNG")


############################# Carnet functions ##############################
def get_user_ranks(user: hikari.Member):
    """Get ranks from a user

    Args:
        user (hikari.User): user to search for roles

    Returns:
        str: String containing all ranks
    """
    server_ranks = yaml_f.get_ranks()
    output = []
    roles = user.get_roles()

    for role in roles:
        if str(role.name) in server_ranks:
            output.append(role.name)
    if output:
        b = ", ".join(output)
    else:
        return "Admin"
    return str(b)


def get_user_roles(user: hikari.Member):
    """Get user roles that are not ranks

    Args:
        user (hikari.User): user to search for roles

    Returns:
        str: String containing roles
    """
    server_ranks = yaml_f.get_ranks()
    mention = []
    roles = user.get_roles()

    for role in roles:
        if (
            role.name != "@everyone"
            and str(role.name) not in server_ranks
            and separator not in str(role)
        ):
            mention.append(role.name)

    b = ", ".join(mention)
    return str(b)


def get_user_species(user: hikari.Member):
    """Get user roles that are species

    Args:
        user (hikari.User): user to search for roles

    Returns:
        str: String containing roles
    """
    server_species = yaml_f.get_species()
    mention = []
    roles = user.get_roles()
    for role in roles:
        if str(role.name) in server_species:
            mention.append(role.name)

    b = ", ".join(mention)
    return b


def get_user_color(user: hikari.Member):
    """Get user role that is a color

    Args:
        user (hikari.User): user to search for color

    Returns:
        str: String with color
    """
    server_colors = yaml_f.get_colors()
    output = "blanco"
    roles = user.get_roles()
    for role in roles:
        if str(role.name) in server_colors:
            output = role.name
            break

    return str(output)


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


# TODO: cambiar argumentos a solo el path del archivo
def exists_file(file: str, directory: str):
    """Checks if exists a file with a given name

    Args:
        file (str): name of the file
        directory (str): folder to search for file

    Returns:
        [Bool]: true if exists, false if not
    """
    output = False
    files = os.listdir(directory)
    if file in files:
        output = True
    return output


# TODO: cambiar argumentos a solo el path del archivo
def exists_substring_in_file(substring: str, directory: str):
    output = False
    files = os.listdir(directory)
    for file in files:
        if substring in file:
            output = True
    return output


def get_files_in_directory(directory: str):
    """Get a list of files in a directory

    Args:
        directory (str): directory to search

    Returns:
        [list]: list of files in dir
    """
    return os.listdir(directory)


def get_files_in_directory_with_substring(substring: str, directory: str):
    """Get a string with files in a directory that contain a substring in its name

    Args:
        directory (str): directory to search

    Returns:
        [files]: list of files in dir
    """
    output = ""
    files = os.listdir(directory)
    for file in files:
        if substring in file:
            output += str(file[:-4]) + ", "
    output = output[:-2]
    return output


def write_in_file(file: str, string: str):
    """Writes text in a file

    Args:
        file (str): file to write
        string (str): string to write
    """
    f = open(file, "a")
    f.write(string)
    f.close()


def delete_content_in_file(file: str):
    """Deletes contents of a file

    Args:
        file (str): File to delete contents
    """
    open(file, "w").close()


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


############################ YAML #########################
