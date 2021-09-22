import requests
from PIL import Image
import pytest
from src.functions import (
    convert_pic,
    count_files_in_dir,
    count_lines_in_file,
    delete_content_in_file,
    exists_file,
    exists_string_in_file,
    get_color_code,
    get_files_in_directory,
    get_files_in_directory_with_substring,
    get_random_line_of_file,
    get_user,
    meme_templates_path,
    write_in_file,
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
    file = "tests/dir/test_file2.txt"
    string = "falseasdf"
    assert exists_string_in_file(file, string) == True


def test_exists_string_in_file_false():
    file = "tests/dir/test_file2.txt"
    string = "x"
    assert exists_string_in_file(file, string) == False


def test_count_lines_in_file():
    assert count_lines_in_file("tests/dir/a") == 18


def test_count_files_in_dir():
    assert count_files_in_dir("tests/dir/") == 5


def test_exists_file_true():
    assert exists_file("a", "tests/dir/") == True


def test_exists_file_false():
    assert exists_file("c", "tests/dir/") == False


def test_get_files_in_directory():
    assert len(get_files_in_directory("tests/dir/")) == 5


def test_get_files_in_directory_with_substring():
    assert (
        get_files_in_directory_with_substring("e", "tests/dir/")
        == "test_file1, test_file2"
    )


# TODO
def test_write_in_file():
    file = "tests/dir/d"
    string1 = "hola mundo"
    string2 = " adios mundo"

    # Write first string
    write_in_file(file, string1)
    f = open(file, "r")

    # check first string
    assert f.readline() == string1
    f.close()

    # Write string2
    write_in_file(file, string2)
    f = open(file, "r")

    # Check string1 and string2
    assert f.readline() == string1 + string2
    f.close()

    # Delete contents of file
    open(file, "w").close()


def test_delete_content_in_file():
    string1 = "hola mundo"
    file = "tests/dir/d"
    write_in_file(file, string1)

    delete_content_in_file(file)

    f = open(file, "r")
    assert f.readline() == ""

    f.close()


def test_get_random_line_of_file():
    assert get_random_line_of_file("tests/dir/b") in [
        "a\n",
        "b\n",
        "c\n",
        "d\n",
        "e\n",
        "f\n",
    ]
