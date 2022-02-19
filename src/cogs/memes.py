from http import server
import io
from turtle import width
import nextcord
from nextcord.ext import commands
import random
import textwrap
import time
import PIL
from PIL import ImageFont, ImageDraw
from utils.functions import (
    get_user,
    delete_files,
    convert_pic,
)
import os
import logging
from cowpy import cow
import unicodedata
import requests
from PIL import Image
from utils.bot import Bot
from utils.data import get_server_path, meme_resources_path, server_path

log = logging.getLogger(__name__)


class memes(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def addmeme(self, ctx: commands.Context, meme_name: str):
        """Añade un meme al bot

        Uso:
            fur meme <nombres personas en el meme>

        """
        memes_path = get_server_path(ctx.guild) + "/memes/"

        meme_extension = "." + ctx.message.attachments[0].filename
        meme_extension = meme_extension[-4:]
        count = 1

        # Remove "
        meme_name = meme_name.replace('"', "")

        # Remove accents
        meme_name = unicodedata.normalize("NFD", meme_name)
        meme_name = meme_name.encode("ascii", "ignore")
        meme_name = meme_name.decode("utf-8")

        # Capitalize all names
        meme_name = meme_name.lower()
        meme_name = meme_name.title()

        # split into a list
        names = meme_name.split()

        # Order names in case they are not in order
        names = sorted(names)
        meme_name = " ".join(names)

        # Count the number to add to the name
        if meme_extension == ".png" or meme_extension == ".jpg":
            for x in os.listdir(memes_path):
                aux2 = x.split(" (", 1)
                if "jpg" in aux2[1] and aux2[0] == meme_name:
                    count = count + 1

        if meme_extension == ".mp4":
            for x in os.listdir(memes_path):
                aux2 = x.split(" (", 1)
                if "mp4" in x and aux2[0] == meme_name:
                    count = count + 1

        count = str(count)

        meme_name = meme_name + " (" + count + ")"

        meme_name = meme_name.replace(" ", "_")
        meme_url = ctx.message.attachments[0].url

        r = requests.get(meme_url, allow_redirects=True)
        open(memes_path + meme_name + meme_extension, "wb").write(r.content)

        if meme_extension == ".png":
            im = Image.open(memes_path + meme_name + meme_extension)
            rgb_im = im.convert("RGB")
            meme_extension = ".jpg"
            rgb_im.save(memes_path + meme_name + meme_extension)
            os.remove(memes_path + meme_name + ".png")

        old = memes_path + meme_name + meme_extension
        newname = meme_name.replace("_", " ")
        new = memes_path + newname + meme_extension
        os.rename(old, new)
        logging.info("Meme " + newname + " added by" + str(ctx.author))
        await ctx.send("Meme " + newname + " añadido")

    @commands.command()
    async def meme(self, ctx: commands.Context, name: str = None, tipo: str = None):
        """Meme random de los nuestros"""

        # If all memes have been sent, delete history
        memes_path = get_server_path(ctx.guild) + "/memes/"

        if name is None:
            output = random.choice(os.listdir(memes_path))

            await ctx.send(file=nextcord.File(memes_path + output))

        else:
            uwu = []
            for filenames in os.listdir(memes_path):
                if name.lower() in filenames.lower():
                    uwu.append(filenames)
            # check if exists a meme with the filters
            if len(uwu) == 0:
                await ctx.send("No hay memes con " + name)
                return
            if (tipo == "video" and not any(".mp4" in s for s in uwu)) or (
                tipo == "imagen" and not any(".jpg" in s for s in uwu)
            ):
                await ctx.send("No hay memes de " + tipo + " que sean de " + name)
                return

            if tipo is not None:
                if tipo == "video":
                    output = "0"
                    while ".mp4" not in output:

                        output = random.choice(uwu)
                if tipo == "imagen":
                    output = "0"
                    while ".jpg" not in output:
                        output = random.choice(uwu)

            else:
                output = random.choice(uwu)

            await ctx.send(file=nextcord.File(memes_path + output))
        logging.info("Meme " + output + " sent")

    @commands.command()
    async def count_memes(self, ctx: commands.Context):
        """Número de memes añadidos al bot"""
        memes_path = get_server_path(ctx.guild) + "/memes/"
        await ctx.send(len(os.listdir(memes_path)))

    @commands.command()
    async def horny(self, ctx: commands.Context, user: nextcord.Member = None):
        """Mucho horny"""
        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        avatar_info = [
            {
                "url": avatarUrl,
                "size": 300,
                "x": 410,
                "y": 180,
            }
        ]

        # Create meme
        meme = create_meme("horny", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))
        # Delete user avatar and output
        # delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def patada(self, ctx: commands.Context, user: nextcord.Member = None):
        """Te vas a comer mi pie"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        # Create meme
        meme = create_meme(
            ("patada", "01", "01"), avatarUrl, 110, (0, 0, 198, 229, 348, 915), True
        )

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def shef(self, ctx: commands.Context, user: nextcord.Member = None):
        """shef"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        meme = create_meme(("shef", "01"), avatarUrl, 120, (0, 0, 280, 87), True)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def quote(
        self,
        ctx: commands.Context,
        quote: str,
        title: str,
        user: nextcord.Member = None,
    ):
        """Crea una quote en imagen

        Uso: fur quote "<quote>" "<titulo>" <@usuario para poner foto>

        - Si el quote tiene " reemplazar por '
        Ejemplo: fur quote "Gala: 'Ala Teko que racista'" "Gala, antiracistas" @Gala

        - Si se quiere poner algo tipo:
            Gala:"Hola que ase"
            Enana:"He reparido"
        se tiene que poner una / entre las dos lineas.
        Ejemplo: fur quote "Gala:'Hola que ase'/Enana:'He reparido' "Gala, antiracistas" @Gala
        """
        # Variables

        userName = get_user(ctx, user)
        avatarSize = 300
        txtSize = 40
        textX = 10
        textY = 10
        textOffsetX = 420
        textOffsetY = 200
        avatarX = 50
        avatarY = 150
        lineWidth = 31

        # Change ' with " because the command needs "" to get the quote and the title
        if "'" not in quote:
            quote = quote.replace("'", '"')
        quote = '"' + quote + '"'

        r = requests.get(userName.avatar.url, allow_redirects=True)
        bytes_io = io.BytesIO(r.content)

        converted_pic = convert_pic(bytes_io, avatarSize)

        # Open images
        txtPic = Image.new("RGBA", (620, 500))
        pic = Image.open(meme_resources_path + "quote.png").convert("RGBA")
        avatar = Image.open(converted_pic).convert("L")

        # Set up fonts
        fontQuote = ImageFont.truetype(meme_resources_path + "Sofia.ttf", txtSize)
        fontTitle = ImageFont.truetype(meme_resources_path + "Calibri.ttf", txtSize - 5)
        d = ImageDraw.Draw(txtPic)

        # Write quote
        cont = 0
        if "/" in quote:  # quote with line break
            lines = quote.split("/")
            for line in lines:
                width, height = fontQuote.getsize(line)

                if len(line) > lineWidth:
                    lines2 = textwrap.wrap(line, width=lineWidth)
                    for line in lines2:
                        width, height = fontQuote.getsize(line)
                        d.text((textX, textY), line, font=fontQuote, fill=None)
                        textY += height
                        cont += 1

                else:
                    d.text((textX, textY), line, font=fontQuote, fill=None)
                    textY += height
                    cont += 1

        else:  # quote without line break
            lines = textwrap.wrap(quote, width=lineWidth)
            if lines[-1] == '"':  # If last line is only a "
                lines[-2] = lines[-2] + '"'  # Put " in line before
                lines.pop(-1)  # Remove line with "

            firstLine = True

            for line in lines:
                width, height = fontQuote.getsize(line)
                if firstLine is True:  # put the first line furthest to the left
                    d.text(((textX - 10), textY), line, font=fontQuote, fill=None)
                    firstLine = False
                else:
                    d.text(((textX), textY), line, font=fontQuote, fill=None)
                cont += 1
                textY += height

        # Write title
        firstLine = True
        lines = textwrap.wrap(title, width=lineWidth)
        if len(lines) > 1:
            textY += 15
            for line in lines:
                width, height = fontTitle.getsize(line)
                d.text(((textX), textY), line, font=fontTitle, fill=None)
                cont += 0.4
                textY += height + 5
        else:
            d.text(((textX) + 5, textY + 30), title, font=fontTitle, fill=None)

        # Paste in meme picture
        pic.paste(avatar, (avatarX, avatarY), avatar)
        pic.paste(txtPic, (textOffsetX, int(220 - 20 * cont)), txtPic)

        # Save picture
        bytes_io = io.BytesIO()
        pic.save(bytes_io, "PNG")
        bytes_io.seek(0)

        await ctx.send(file=nextcord.File(bytes_io, "output.png"))

        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def impostor(self, ctx: commands.Context, user: nextcord.Member = None):
        """Quién es el impostor?"""

        avatarUrl = get_user(ctx, user).avatar.url

        meme = create_meme(("impostor", "01"), avatarUrl, 205, (0, 0, 323, 175), True)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def stonks(self, ctx: commands.Context, user: nextcord.Member = None):
        """Stonks"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        meme = create_meme(("stonks", "01"), avatarUrl, 236, (0, 0, 63, 25), True)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def jojo(self, ctx: commands.Context, user: nextcord.Member):
        """Za warudo"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        r = requests.get(ctx.author.avatar.url, allow_redirects=True)
        open(meme_resources_path + "02.webp", "wb").write(r.content)

        convert_pic(meme_resources_path + "02.webp", "02", 65)

        meme = create_meme(
            ("jojo", "01", "02"), avatarUrl, 65, (0, 0, 162, 19, 469, 130), True
        )

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png", "02.png", "02.webp"))

    @commands.command()
    async def cute(self, ctx: commands.Context, user: nextcord.Member = None):
        """You are cute"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        meme = create_meme(("cute", "01"), avatarUrl, 387, (0, 0, 210, 75), True)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def suicidio(self, ctx: commands.Context):
        """Es hora del suisidio"""

        # Get user avatar
        avatarUrl = ctx.author.avatar.url

        meme = create_meme(("suicidio", "01"), avatarUrl, 54, (0, 0, 172, 182), True)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def coding(self, ctx: commands.Context, user: nextcord.Member = None):
        """Programa como un pro hacker"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        meme = create_meme(("coding", "01"), avatarUrl, 167, (0, 0, 218, 137), True)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def unsee(self, ctx: commands.Context, user: nextcord.Member = None):
        """No por favor"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        meme = create_meme(("unsee", "01"), avatarUrl, 108, (0, 0, 256, 112), True)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def palomitas(self, ctx: commands.Context, user: nextcord.Member = None):
        """Este drama está interesante"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        meme = create_meme(("palomitas", "01"), avatarUrl, 125, (0, 0, 278, 67), True)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def quien(
        self,
        ctx: commands.Context,
        text1: str,
        text2: str,
        user: nextcord.Member = None,
    ):
        """Quien ha sido?

        Uso:
            fur quien <texto1> <texto2> @<usuario>

        Ejemplo:
            fur quien "Le gustan los chilenos?" "Si" @Thedax
        """

        Y = 20
        Y_aux = 10

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        meme = create_meme(("quien", "01"), avatarUrl, 130, (0, 0, 210, 570), True)
        txtPic = Image.new("RGBA", (200, 200))
        img = Image.open(meme_resources_path + "output" + ".png").convert("RGBA")
        draw = ImageDraw.Draw(txtPic)
        font = ImageFont.truetype(meme_resources_path + "Calibri.ttf", 24)

        lines = textwrap.wrap(text1, width=18)
        for line in lines:
            draw.text(((0, Y)), line, font=font, fill=(0, 0, 0, 255))
            Y = Y + 25

        draw.text(((170, 170)), text2, font=font, fill=(0, 0, 0, 255))
        img.paste(txtPic, (180, 10), txtPic)

        # Save
        bytes_io = io.BytesIO()
        img.save(bytes_io, "PNG")
        bytes_io.seek(0)

        # Send meme
        await ctx.send(file=nextcord.File(bytes_io, "output.png"))

        # Delete user avatar and output
        time.sleep(1)
        delete_files(("01.webp", "output.png", "01.png", "output2.png"))

    @commands.command()
    async def cojones(self, ctx: commands.Context, text: str, user: nextcord.Member):
        """Si, los cojones

        Uso:
            fur cojones <texto> @<usuario>
        """

        # Get user avatar
        avatarUrl = user.avatar.url

        # Download author avatar
        r = requests.get(ctx.author.avatar.url, allow_redirects=True)
        open(meme_resources_path + "02.webp", "wb").write(r.content)

        convert_pic(meme_resources_path + "02.webp", "02", 146)

        create_meme(
            ("cojones", "01", "02"), avatarUrl, 175, (0, 0, 185, 431, 218, 6), True
        )

        # Add text to image
        img = Image.open(meme_resources_path + "output" + ".png").convert("RGBA")
        txtPic = Image.new("RGBA", (600, 300))
        draw = ImageDraw.Draw(txtPic)
        font = ImageFont.truetype(meme_resources_path + "Calibri.ttf", 45)

        draw.text(((10, 10)), text, font=font, fill=(0, 0, 0, 255))
        img.paste(txtPic, (720, 560), txtPic)

        img.save(meme_resources_path + "output2.png", "PNG")

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(
            ("01.webp", "output.png", "01.png", "02.png", "02.webp", "output2.png")
        )

    @commands.command()
    async def palanca(self, ctx: commands.Context, user: nextcord.Member):
        """Tira de la palanca Cronk"""

        # Get author avatar url
        author_avatar_url = ctx.author.avatar.url

        # Download second avatar
        r = requests.get(user.avatar.url, allow_redirects=True)
        open(meme_resources_path + "02.webp", "wb").write(r.content)

        convert_pic(meme_resources_path + "02.webp", "02", 57)

        create_meme(
            ("palanca", "01", "02"),
            author_avatar_url,
            62,
            (0, 0, 240, 79, 137, 176),
            True,
        )

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png", "02.png", "02.webp"))

    @commands.command()
    async def tren(self, ctx: commands.Context, user: nextcord.Member):
        """Atropella gente con un tren"""

        # Get author avatar url
        author_avatar_url = ctx.author.avatar.url

        r = requests.get(user.avatar.url, allow_redirects=True)
        open(meme_resources_path + "02.webp", "wb").write(r.content)

        convert_pic(meme_resources_path + "02.webp", "02", 133)

        create_meme(
            ("tren", "01", "02"),
            author_avatar_url,
            212,
            (0, 0, 422, 148, 110, 275),
            True,
        )

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png", "02.png", "02.webp"))

    @commands.command()
    async def cowsay(self, ctx: commands.Context, text: str, character: str = None):
        """Una vaca dice cosas

        Uso:
           fur cowsay <texto>
           fur cowsay <texto> <personaje>

           Personajes:
           beavis budfrogs bunny cheese cower daemon dragonandcow eyes flamingsheep ghostbusters
           hellokitty kiss kitty koala kosh lukekoala
           mechandcow meow milk moofasa moose mutilated ren satanic sheep skeleton small
           squirrel stegosaurus stimpy supermilker surgery threeeyes
           turkey turtle tux udder vader vaderkoala www
        """

        if character is None:
            cow_cls = cow.get_cow("default")
        else:
            cow_cls = cow.get_cow(character)
        cheese = cow_cls()
        msg = cheese.milk(text)
        output = "```"
        output += msg
        output += "```"

        await ctx.send(output)

    @commands.command()
    async def slap(self, ctx: commands.Context, user: nextcord.Member = None):
        """slap"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        meme = create_meme(("slap", "01"), avatarUrl, 160, (0, 0, 120, 88), True)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def reviento(self, ctx: commands.Context, user: nextcord.Member = None):
        """a que me reviento"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        meme = create_meme(("reviento", "01"), avatarUrl, 78, (0, 0, 315, 80), True)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def radiopatio(self, ctx: commands.Context, user: nextcord.Member):
        """Es hora del cotilleo"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        meme = create_meme(("radiopatio", "01"), avatarUrl, 88, (0, 0, 188, 45), True)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def omni(self, ctx: commands.Context, user: nextcord.Member = None):
        """Omniman"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        meme = create_meme(("omni", "01"), avatarUrl, 470, (0, 0, 210, 388), True)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def mierda(self, ctx: commands.Context, user: nextcord.Member = None):
        """Menudo montón de mierda"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        meme = create_meme(("mierda", "01"), avatarUrl, 270, (0, 0, 476, 161), True)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def coche(
        self,
        ctx: commands.Context,
        text1: str,
        text2: str,
        text3: str,
        user: nextcord.Member,
    ):
        """Fuera de mi coche

        Uso:
            fur coche <Texto1> <Texto2> <Texto3> @<usuario>

        Ejemplo:
            fur coche "Eres de madrid?" "Si" "Fuera de mi coche" @Frank

        """

        # Get images
        r = requests.get(ctx.author.avatar.url, allow_redirects=True)
        open(meme_resources_path + "01.webp", "wb").write(r.content)
        r = requests.get(user.avatar.url, allow_redirects=True)
        open(meme_resources_path + "02.webp", "wb").write(r.content)

        # Convert images
        convert_pic(meme_resources_path + "01.webp", "01", 205)  # author
        convert_pic(meme_resources_path + "02.webp", "02", 205)  # user
        convert_pic(meme_resources_path + "02.webp", "03", 120)  # user

        # Open new image
        width, height = (
            Image.open(meme_resources_path + "coche.png").convert("RGBA").size
        )
        output = Image.new("RGBA", (width, height))  # Create picture

        # Open other images
        meme = Image.open(meme_resources_path + "coche.png").convert("RGBA")
        author_image = Image.open(meme_resources_path + "01.png").convert("RGBA")
        user_image = Image.open(meme_resources_path + "02.png").convert("RGBA")
        user_image2 = Image.open(meme_resources_path + "03.png").convert("RGBA")

        # Paste images
        output.paste(author_image, (171, 0), author_image)
        output.paste(author_image, (170, 616), author_image)
        output.paste(user_image, (603, 10), user_image)
        output.paste(user_image2, (766, 741), user_image2)
        output.paste(meme, (0, 0), meme)

        # Write text
        Y = 15

        txtPic1 = Image.new("RGBA", (450, 230))
        draw = ImageDraw.Draw(txtPic1)
        font = ImageFont.truetype(meme_resources_path + "Calibri.ttf", 40)
        lines1 = textwrap.wrap(text1, width=25)
        for line in lines1:
            draw.text(((10, Y)), line, font=font, fill=(255, 255, 255, 255))
            Y = Y + 40

        Y = 8
        txtPic2 = Image.new("RGBA", (320, 220))
        draw = ImageDraw.Draw(txtPic2)
        lines2 = textwrap.wrap(text2, width=19)
        for line in lines2:
            draw.text(((10, Y)), line, font=font, fill=(255, 255, 255, 255))
            Y = Y + 40

        Y = 8
        txtPic3 = Image.new("RGBA", (540, 120))
        draw = ImageDraw.Draw(txtPic3)
        lines3 = textwrap.wrap(text3, width=30)
        for line in lines3:
            draw.text(((10, Y)), line, font=font, fill=(255, 255, 255, 255))
            Y = Y + 40

        output.paste(txtPic1, (18, 249), txtPic1)
        output.paste(txtPic2, (550, 260), txtPic2)
        output.paste(txtPic3, (188, 888), txtPic3)

        # Save image
        output.save(meme_resources_path + "output.png", "PNG")

        await ctx.send(file=nextcord.File(meme, "output.png"))

        delete_files(("01.webp", "02.webp", "01.png", "02.png", "03.png", "output.png"))

    @commands.command()
    async def skeletor(self, ctx: commands.Context, text1: str, text2: str):
        """Datos perturbadores de Skeletor

        Uso:
            fur skeletor <text1> <text2>
        """

        meme_width = 994
        meme_hegiht = 680
        txtPic1 = Image.new("RGBA", (meme_width, meme_hegiht))
        pic = Image.open(meme_resources_path + "skeletor.png").convert("RGBA")
        font = ImageFont.truetype(meme_resources_path + "impact.ttf", 60)
        d = ImageDraw.Draw(txtPic1)

        # Write text1
        lines = textwrap.wrap(text1.upper(), width=35)
        textY = 0
        for line in lines:
            width, height = font.getsize(line)

            d.text(((meme_width - width) / 2, textY), line, font=font, fill=None)
            textY += height

        lines = textwrap.wrap(text2.upper(), width=35)
        textY = 520
        for line in lines:
            width, height = font.getsize(line)

            d.text(((meme_width - width) / 2, textY), line, font=font, fill=None)
            textY += height

        pic.paste(txtPic1, (10, 440), txtPic1)

        pic.save(meme_resources_path + "output.png", "PNG")

        await ctx.send(file=nextcord.File(meme, "output.png"))
        os.remove(meme_resources_path + "output.png")

    @commands.command()
    async def undertale(
        self, ctx: commands.Context, texto: str, usuario: nextcord.Member = None
    ):
        """Bajo cuento"""

        # Get user
        avatar_url = get_user(ctx, usuario).avatar.url

        # Get image
        character_image_size = 200
        r = requests.get(avatar_url, allow_redirects=True)
        open(meme_resources_path + "01.webp", "wb").write(r.content)
        convert_pic(meme_resources_path + "01.webp", "01", 200)

        # Open resources
        image = Image.open(meme_resources_path + "dialogue_box.png")
        font = ImageFont.truetype(
            meme_resources_path + "Determination-Sans.otf", size=60
        )
        txtPic1 = Image.new("RGBA", (800, 270))
        draw = ImageDraw.Draw(txtPic1)

        # Convert character picture
        sprite = Image.open(meme_resources_path + "01.png").convert("L")
        wpercent = character_image_size / float(sprite.size[0])
        hsize = int((float(sprite.size[1]) * float(wpercent)))
        sprite = sprite.resize((character_image_size, hsize), Image.ANTIALIAS)
        image.paste(sprite, (70, 90))

        # Add text
        lines = textwrap.wrap(texto, width=25)
        Y = 20
        for line in lines:
            width, height = font.getsize(line)
            draw.text(((10, Y)), line, font=font, fill=(255, 255, 255, 255))
            Y = Y + height

        image.paste(txtPic1, (350, 50), txtPic1)
        image.save(meme_resources_path + "output.png", "PNG")
        await ctx.send(file=nextcord.File(meme, "output.png"))
        delete_files(("output.png", "01.png", "01.webp"))

    @commands.command()
    async def huracan(
        self,
        ctx: commands.Context,
        user1: nextcord.Member,
        user2: nextcord.Member,
        user3: nextcord.Member,
    ):
        """Jaja huracán

        Uso:
            fur huracan <usuario1> <usuario2> <usuario3>
        """

        # Get user avatars
        r = requests.get(user1.avatar.url, allow_redirects=True)
        open(meme_resources_path + "01.webp", "wb").write(r.content)
        r = requests.get(user2.avatar.url, allow_redirects=True)
        open(meme_resources_path + "02.webp", "wb").write(r.content)
        r = requests.get(user3.avatar.url, allow_redirects=True)
        open(meme_resources_path + "03.webp", "wb").write(r.content)

        # Convert avatars
        convert_pic(meme_resources_path + "01.webp", "01", 265)
        convert_pic(meme_resources_path + "02.webp", "02", 230)
        convert_pic(meme_resources_path + "03.webp", "03", 170)

        # Open meme image
        meme = Image.open(meme_resources_path + "huracan" + ".png").convert("RGBA")

        # Get width and height
        width, height = meme.size

        # Create base image
        output = Image.new("RGBA", (width, height))

        # Paste images
        img1 = Image.open(meme_resources_path + "01" + ".png").convert("RGBA")
        output.paste(img1, (683, 473), img1)
        img2 = Image.open(meme_resources_path + "02" + ".png").convert("RGBA")
        output.paste(img2, (420, 630), img2)
        img3 = Image.open(meme_resources_path + "03" + ".png").convert("RGBA")
        output.paste(img3, (650, 870), img3)

        # Paste meme image
        output.paste(meme, (0, 0), meme)
        output.save(meme_resources_path + "output.png", "PNG")

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

        # Delete user avatar and output
        delete_files(
            (
                "01.webp",
                "02.webp",
                "03.webp",
                "output.png",
                "01.png",
                "02.png",
                "03.png",
            )
        )


def create_meme(meme_picture: str, avatars_info: list[dict]) -> io.BytesIO:
    """Crea un meme

    Args:
        meme_picture (str): name of the meme picture
        avatars_info (list): containgin a dictionary with the avatars info.
            The keys of each avatar are: url, size, x, y

    Returns:
        io.BytesIO: the meme image
    """

    # Open meme canvas
    meme = Image.open(meme_resources_path + meme_picture + ".png").convert("RGBA")

    # Get canvas size
    width, height = meme.size

    # Create canvas
    canvas = Image.new("RGBA", (width, height))

    # Paste avatars
    for avatar in avatars_info:
        url = avatar["url"]
        size = avatar["size"]
        x = avatar["x"]
        y = avatar["y"]
        avatar = (
            Image.open(io.BytesIO(requests.get(url).content))
            .convert("RGBA")
            .resize((size, size))
        )
        canvas.paste(avatar, (x, y), avatar)

    # Paste meme into canvas
    canvas.paste(meme, (0, 0), meme)

    bytes_io = io.BytesIO()

    canvas.save(bytes_io, "PNG")
    bytes_io.seek(0)

    return bytes_io


def setup(bot: commands.Bot):
    bot.add_cog(memes(bot))
