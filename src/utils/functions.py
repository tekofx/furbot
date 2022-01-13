# Contains all functions that are not commands
from PIL import Image
import os
import logging
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands
import praw
import random
import requests
import yaml
from utils.data import resources_path, meme_resources_path


def get_user_avatar(url: str, name: str):
    """Downloads the avatar of a user

    Args:
        user (hikari.User): user to download avatar from
        name (str): user to download avatar from
    """

    r = requests.get(url, allow_redirects=True)

    open(meme_resources_path + name, "wb").write(r.content)

    logging.info("Saved avatar with url " + url + " in " + meme_resources_path)


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

    img.save(meme_resources_path + imgName + ".png")


def get_user(ctx: commands.Context, user: nextcord.Member = None) -> nextcord.Member:
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
        if os.path.isfile(meme_resources_path + x):
            os.remove(meme_resources_path + x)
    logging.info("Removed dependencies")
