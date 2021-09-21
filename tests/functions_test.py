import requests
from PIL import Image
import pytest
from src.functions import (
    convert_pic,
    exists_string_in_file,
    get_color_code,
    get_user,
    meme_templates_path,
)
import discord
import os


def test_get_user_avatar():
    pass


def test_convert_pic():
    image_size = 200
    r = requests.get(
        "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.r8ZOm4wGSzX-uC0khYq7zgHaEK%26pid%3DApi&f=1",
        allow_redirects=True,
    )

    open("tests/image.jpeg", "wb").write(r.content)

    convert_pic("tests/image.jpeg", "picture", 200)

    image = Image.open(meme_templates_path + "picture.png")

    assert image_size == image.size[0]
    os.remove(meme_templates_path + "picture.png")
    os.remove("tests/image.jpeg")


def test_get_user_none():
    user = None
    context = discord.ext.commands.context.Context
    context.author = 719623435607643137

    assert get_user(context, user) == 719623435607643137


def test_get_user_not_none():
    user = 719623435607643137
    context = discord.ext.commands.context.Context
    context.author = 123456789607643137

    assert get_user(context, user) == 719623435607643137


def test_create_meme():
    pass


def test_get_user_ranks():
    pass


def test_get_user_roles():
    pass


def test_get_user_species():
    pass


def test_get_user_color():

    pass


def test_get_color_code():
    assert get_color_code("rojo") == [197, 10, 12]
    assert get_color_code("verde") == [15, 199, 29]
    assert get_color_code("morado") == [114, 18, 172]


def test_get_reddit_image():
    pass


def test_get_hot_subreddit_image():
    pass


def test_exists_string_in_file_true():
    file = "tests/file1.txt"
    string = "dafadsfasd545454"
    assert exists_string_in_file(file, string) == True


def test_exists_string_in_file_false():
    file = "tests/file1.txt"
    string = "d"
    assert exists_string_in_file(file, string) == False
