# Contains all functions that are not commands
from PIL import Image
import os
import logging
import nextcord
from nextcord.ext import commands
import requests
from utils.data import meme_resources_path


def convert_pic(picture: str, img_name: str, img_size: str = None):
    """Converts an image to PNG with a differents size

    Args:
        picture (str): picture to convert
        img_name (str): exported picture name
        img_size (str): exported image size
    """
    img = Image.open(picture)

    if img_size is not None:
        wpercent = img_size / float(img.size[0])
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((img_size, hsize), Image.ANTIALIAS)

    img.save(meme_resources_path + img_name + ".png")


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


def delete_files(elements: list):
    """Delete files needed to create a meme

    Args:
        elements (list): files used in a meme
    """
    for x in elements:
        if os.path.isfile(meme_resources_path + x):
            os.remove(meme_resources_path + x)
    logging.info("Removed dependencies")
