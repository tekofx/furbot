# Contains all functions that are not commands
import discord
from PIL import Image
import os
import logging
from dotenv import load_dotenv
import praw
import random
from discord.ext import commands
import requests
import yaml


# .env data

load_dotenv()

yaml_file = "files/resources/config.yaml"

separator = "       "  # key word to distinguish separator roles


# Create bot
prefixes = ["fur ", "Fur ", "FUR "]
bot = commands.Bot(command_prefix=prefixes)

# Paths
stickers_path = "files/stickers/"
meme_templates_path = "files/resources/memes/"
meme_path = "files/memes/"
paths = [stickers_path, meme_path]

# Datafiles
insults_txt = "files/resources/data/insults.txt"
cumpleaños_txt = "files/resources/data/cumpleaños.txt"
reddit_memes_history_txt = "files/resources/data/reddit_memes_history.txt"
animos_txt = "files/resources/data/animos.txt"
memes_history_txt = "files/resources/data/memes_history.txt"
activity_txt = "files/resources/data/activity.txt"
jojos_txt = "files/resources/data/jojos.txt"
species_txt = "files/resources/data/species.txt"
colors_txt = "files/resources/data/colors.txt"
ranks_txt = "files/resources/data/ranks.txt"
files = [
    insults_txt,
    cumpleaños_txt,
    reddit_memes_history_txt,
    animos_txt,
    memes_history_txt,
    activity_txt,
    jojos_txt,
    species_txt,
    colors_txt,
    ranks_txt,
]

stickerSize = 500

# Creation of reddit
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
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
        user (discord.Member): user to download avatar from
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


def get_user(context, user: discord.Member = None):
    """Gets user from a message

    Args:
        context (Message): Message to get an avatar
        user (discord.Member, optional): User of a message. Defaults to None.

    Returns:
        discord.Member: user
    """
    if user is None:
        output = context.author
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
def get_user_ranks(user: discord.Member):
    """Get ranks from a user

    Args:
        user (discord.Member): user to search for roles

    Returns:
        str: String containing all ranks
    """
    server_ranks = get_ranks(yaml_file)
    print(server_ranks)
    output = []
    for role in user.roles:
        if str(role.name) in server_ranks:
            print("b")
            output.append(role.name)
    if output:
        b = ", ".join(output)
    else:
        return "Admin"
    return str(b)


def get_user_roles(user: discord.Member):
    """Get user roles that are not ranks

    Args:
        user (discord.Member): user to search for roles

    Returns:
        str: String containing roles
    """
    server_ranks = get_ranks(yaml_file)
    mention = []
    for role in user.roles:
        if (
            role.name != "@everyone"
            and str(role.name) not in server_ranks
            and separator not in str(role)
        ):
            mention.append(role.name)

    b = ", ".join(mention)
    return str(b)


def get_user_species(user: discord.Member):
    """Get user roles that are species

    Args:
        user (discord.Member): user to search for roles

    Returns:
        str: String containing roles
    """
    server_species = get_species(yaml_file)
    mention = []
    for role in user.roles:
        if str(role.name) in server_species:
            mention.append(role.name)

    b = ", ".join(mention)
    return b


def get_user_color(user: discord.Member):
    """Get user role that is a color

    Args:
        user (discord.Member): user to search for color

    Returns:
        str: String with color
    """
    output = "blanco"
    for role in user.roles:
        if exists_string_in_file(colors_txt, str(role.name)):
            output = role.name
            break

    return str(output)


############################### Reddit functions ###############################
def get_reddit_image(Subreddit: str, Flair: str, Filter: str):
    """Gets a random Reddit image

    Args:
        Subreddit (str): subreddit to get the photo from
        Flair (str): flair to filter by
        Filter (str): filter to search by

    Returns:
        str: url from a reddit image
    """
    try:
        var = True
        while var:
            if Flair is None:
                memes_submissions = reddit.subreddit(Subreddit).search(
                    Filter
                )  # Gets a random images from r/foxes with flair Pics!
            else:
                memes_submissions = reddit.subreddit(Subreddit).search(
                    "Flair:" + Flair
                )  # Gets a random images from r/foxes with flair Pics!
            post_to_pick = random.randint(1, 10)
            for i in range(0, post_to_pick):
                submission = next(x for x in memes_submissions if not x.stickied)
            if submission.url.endswith("jpg"):
                var = False
    except ConnectionError:
        logging.error("Error at getting images from reddit")

    return submission.url


def get_hot_subreddit_image(Subreddit: str, Limit: int, file_txt: str):
    """Get an image from a subreddit in hot

    Args:
        Subreddit (str): Subreddit to search for
        Limit (int): Limit to search in subreddit

    Returns:
        str: link to image
    """
    output = random.choice([x for x in reddit.subreddit(Subreddit).hot(limit=Limit)])
    try:
        while (
            exists_string_in_file(file_txt, output.url) and "v.reddit.it" not in output
        ):
            output = random.choice(
                [x for x in reddit.subreddit(Subreddit).hot(limit=Limit)]
            )

        write_in_file(file_txt, output.url + "\n")

        return output.url
    except FileNotFoundError:
        logging.error("Error at getting reddit_memes_history.txt")


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
def get_content_yaml(yaml_file: str):
    with open(yaml_file, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print("Error loading YAML: " + exc)


def get_ranks(yaml_file: str):
    content = get_content_yaml(yaml_file)
    output = []
    for x in content["ranks"]:
        output.append(x)

    return output


def get_activity(yaml_file: str):
    content = get_content_yaml(yaml_file)
    print(content["activity"])
    pass


def get_color_code(yaml_file: str, color: str):
    content = get_content_yaml(yaml_file)

    for key, value in content["colors"].items():
        if key == color:
            print(value)
            output = value.split(" ")
            # Delete \n from last element
            output = [s.replace("\n", "") for s in output]

            # Convert all elements into int
            output = list(map(int, output))
            print(output)
            return output


def get_species(yaml_file: str):
    content = get_content_yaml(yaml_file)
    output = []
    for x in content["species"]:
        output.append(x)

    return output
