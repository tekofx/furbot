import random
import textwrap
import time
from PIL import ImageFont, ImageDraw
import hikari
from functions import (
    create_meme,
    get_user,
    delete_files,
    convert_pic,
    get_hot_subreddit_image,
    meme_path,
    meme_templates_path,
    count_files_in_dir,
    memes_history_txt,
    exists_string_in_file,
    write_in_file,
    count_lines_in_file,
    reddit_memes_history_txt,
)
import os
import logging
from cowpy import cow
import unicodedata
import requests
from PIL import Image
import lightbulb
from time import sleep


class Memes(lightbulb.Plugin):
    def __init__(self, bot: lightbulb.Bot):
        super().__init__(name="Memes")
        self.bot = bot

    @lightbulb.command()
    async def addmeme(self, ctx: lightbulb.Context, meme_name: str):
        """Añade un meme al bot"""
        meme_extension = "." + ctx.attachments[0].url.split(".")[-1]
        count = 1

        # TODO: Check raise error with hikari
        # If meme_name is user
        # if "@" in meme_extension:
        #    logging.error("Argument provided is a user")
        #    raise commands.CommandError("argument_is_user")

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
            for x in os.listdir(meme_path):
                aux2 = x.split(" (", 1)
                if "jpg" in aux2[1] and aux2[0] == meme_name:
                    count = count + 1

        if meme_extension == ".mp4":
            for x in os.listdir(meme_path):
                aux2 = x.split(" (", 1)
                if "mp4" in x and aux2[0] == meme_name:
                    count = count + 1

        count = str(count)

        meme_name = meme_name + " (" + count + ")"

        meme_name = meme_name.replace(" ", "_")
        meme_url = ctx.attachments[0].url

        r = requests.get(meme_url, allow_redirects=True)
        open(meme_path + meme_name + meme_extension, "wb").write(r.content)

        if meme_extension == ".png":
            im = Image.open(meme_path + meme_name + meme_extension)
            rgb_im = im.convert("RGB")
            meme_extension = ".jpg"
            rgb_im.save(meme_path + meme_name + meme_extension)
            os.remove(meme_path + meme_name + ".png")

        old = meme_path + meme_name + meme_extension
        newname = meme_name.replace("_", " ")
        new = meme_path + newname + meme_extension
        os.rename(old, new)
        logging.info("Meme " + newname + " added by" + str(ctx.author))
        await ctx.respond("Meme " + newname + " añadido")

    @lightbulb.command()
    async def meme(self, ctx: lightbulb.Context, name: str = None, tipo: str = None):
        """Meme random de los nuestros

        Uso:
            fur meme-->Meme random
            fur meme <nombre>-->Meme random de <nombre>
        """

        # If all memes have been sent, delete history
        try:
            if count_files_in_dir(meme_path) <= 30 + count_lines_in_file(
                memes_history_txt
            ):
                open(memes_history_txt, "w").close()
        except FileNotFoundError:
            logging.error("Error:  memes_history_txt could not be readed")
            return 0

        if name is None:
            output = random.choice(os.listdir(meme_path))
            while exists_string_in_file(memes_history_txt, output):
                output = random.choice(os.listdir(meme_path))

            write_in_file(memes_history_txt, output + "\n")
            await ctx.respond(attachment=meme_path + output)

        else:
            uwu = []
            for filenames in os.listdir(meme_path):
                if name.lower() in filenames.lower():
                    uwu.append(filenames)
            # check if exists a meme with the filters
            if len(uwu) == 0:
                await ctx.respond("No hay memes con " + name)
                return
            if (tipo == "video" and not any(".mp4" in s for s in uwu)) or (
                tipo == "imagen" and not any(".jpg" in s for s in uwu)
            ):
                await ctx.respond("No hay memes de " + tipo + " que sean de " + name)
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

                # Check if there are any memes with the name

            await ctx.respond(attachment=meme_path + output)
        logging.info("Meme " + output + " sent")

    @lightbulb.command(name="countmemes")
    async def count_memes(self, ctx: lightbulb.Context):
        """Número de memes añadidos al bot"""
        await ctx.respond(count_files_in_dir(meme_path))

    @lightbulb.command()
    async def horny(self, ctx: lightbulb.Context, user: hikari.Member = None):
        """Mucho horny

        Uso: fur horny "@<usuario>
        """
        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        # Create meme
        create_meme(("horny", "01"), avatarUrl, 300, (0, 0, 410, 180), True)

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def patada(self, ctx: lightbulb.Context, user: hikari.Member = None):
        """Te vas a comer mi pie

        Uso: fur patada "@<usuario>
        """
        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        # Create meme
        create_meme(
            ("patada", "01", "01"), avatarUrl, 110, (0, 0, 198, 229, 348, 915), True
        )

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def shef(self, ctx: lightbulb.Context, user: hikari.Member = None):
        """shef"""
        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        create_meme(("shef", "01"), avatarUrl, 120, (0, 0, 280, 87), True)

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def quote(
        self, ctx: lightbulb.Context, quote: str, title: str, user: hikari.Member = None
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

        r = requests.get(userName.avatar_url, allow_redirects=True)
        open(meme_templates_path + "01.webp", "wb").write(r.content)

        convert_pic(meme_templates_path + "01.webp", "01", avatarSize)

        # Open images
        txtPic = Image.new("RGBA", (620, 500))
        pic = Image.open(meme_templates_path + "quote.png").convert("RGBA")
        avatar = Image.open(meme_templates_path + "01" + ".png").convert("L")

        # Set up fonts
        fontQuote = ImageFont.truetype(meme_templates_path + "Sofia.ttf", txtSize)
        fontTitle = ImageFont.truetype(meme_templates_path + "Calibri.ttf", txtSize - 5)
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
        pic.save(meme_templates_path + "output.png", "PNG")

        await ctx.respond(attachment=meme_templates_path + "output.png")
        sleep(10)
        await ctx._message.delete()

        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def impostor(self, ctx: lightbulb.Context, user: hikari.Member = None):
        """Quién es el impostor?"""
        avatarUrl = get_user(ctx, user).avatar_url

        create_meme(("impostor", "01"), avatarUrl, 205, (0, 0, 323, 175), True)

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def stonks(self, ctx: lightbulb.Context, user: hikari.Member = None):
        """Stonks"""
        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        create_meme(("stonks", "01"), avatarUrl, 236, (0, 0, 63, 25), True)

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def jojo(self, ctx: lightbulb.Context, user: hikari.Member):
        """Za warudo"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        r = requests.get(ctx.author.avatar_url, allow_redirects=True)
        open(meme_templates_path + "02.webp", "wb").write(r.content)

        convert_pic(meme_templates_path + "02.webp", "02", 65)

        create_meme(
            ("jojo", "01", "02"), avatarUrl, 65, (0, 0, 162, 19, 469, 130), True
        )

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png", "02.png", "02.webp"))

    @lightbulb.command()
    async def cute(self, ctx: lightbulb.Context, user: hikari.Member = None):
        """You are cute"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        create_meme(("cute", "01"), avatarUrl, 387, (0, 0, 210, 75), True)

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def suicidio(self, ctx: lightbulb.Context):
        """Es hora del suisidio"""

        # Get user avatar
        avatarUrl = ctx.author.avatar_url

        create_meme(("suicidio", "01"), avatarUrl, 54, (0, 0, 172, 182), True)

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def coding(self, ctx: lightbulb.Context, user: hikari.Member = None):
        """Programa como un pro hacker"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        create_meme(("coding", "01"), avatarUrl, 167, (0, 0, 218, 137), True)

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def unsee(self, ctx: lightbulb.Context, user: hikari.Member = None):
        """No por favor"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        create_meme(("unsee", "01"), avatarUrl, 108, (0, 0, 256, 112), True)

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def palomitas(self, ctx: lightbulb.Context, user: hikari.Member = None):
        """Este drama está interesante"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        create_meme(("palomitas", "01"), avatarUrl, 125, (0, 0, 278, 67), True)

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def quien(
        self, ctx: lightbulb.Context, text1: str, text2: str, user: hikari.Member = None
    ):
        """Quien ha sido?"""
        Y = 20
        Y_aux = 10

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        create_meme(("quien", "01"), avatarUrl, 130, (0, 0, 210, 570), True)
        txtPic = Image.new("RGBA", (200, 200))
        img = Image.open(meme_templates_path + "output" + ".png").convert("RGBA")
        draw = ImageDraw.Draw(txtPic)
        font = ImageFont.truetype(meme_templates_path + "Calibri.ttf", 24)

        lines = textwrap.wrap(text1, width=18)
        for line in lines:
            draw.text(((0, Y)), line, font=font, fill=(0, 0, 0, 255))
            Y = Y + 25

        draw.text(((170, 170)), text2, font=font, fill=(0, 0, 0, 255))
        img.paste(txtPic, (180, 10), txtPic)
        img.save(meme_templates_path + "output2.png", "PNG")

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        time.sleep(1)
        delete_files(("01.webp", "output.png", "01.png", "output2.png"))

    @lightbulb.command()
    async def cojones(self, ctx: lightbulb.Context, text: str, user: hikari.Member):
        """Si, los cojones"""

        # Get user avatar
        avatarUrl = user.avatar_url

        # Download author avatar
        r = requests.get(ctx.author.avatar_url, allow_redirects=True)
        open(meme_templates_path + "02.webp", "wb").write(r.content)

        convert_pic(meme_templates_path + "02.webp", "02", 146)

        create_meme(
            ("cojones", "01", "02"), avatarUrl, 175, (0, 0, 185, 431, 218, 6), True
        )

        # Add text to image
        img = Image.open(meme_templates_path + "output" + ".png").convert("RGBA")
        txtPic = Image.new("RGBA", (600, 300))
        draw = ImageDraw.Draw(txtPic)
        font = ImageFont.truetype(meme_templates_path + "Calibri.ttf", 45)

        draw.text(((10, 10)), text, font=font, fill=(0, 0, 0, 255))
        img.paste(txtPic, (720, 560), txtPic)

        img.save(meme_templates_path + "output2.png", "PNG")

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(
            ("01.webp", "output.png", "01.png", "02.png", "02.webp", "output2.png")
        )

    @lightbulb.command()
    async def palanca(self, ctx: lightbulb.Context, user: hikari.Member):
        """Tira de la palanca Cronk"""

        # Get author avatar url
        author_avatar_url = ctx.author.avatar_url

        # Download second avatar
        r = requests.get(user.avatar_url, allow_redirects=True)
        open(meme_templates_path + "02.webp", "wb").write(r.content)

        convert_pic(meme_templates_path + "02.webp", "02", 57)

        create_meme(
            ("palanca", "01", "02"),
            author_avatar_url,
            62,
            (0, 0, 240, 79, 137, 176),
            True,
        )

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png", "02.png", "02.webp"))

    @lightbulb.command()
    async def tren(self, ctx: lightbulb.Context, user: hikari.Member):
        """Atropella gente con un tren"""

        # Get author avatar url
        author_avatar_url = ctx.author.avatar_url

        r = requests.get(user.avatar_url, allow_redirects=True)
        open(meme_templates_path + "02.webp", "wb").write(r.content)

        convert_pic(meme_templates_path + "02.webp", "02", 133)

        create_meme(
            ("tren", "01", "02"),
            author_avatar_url,
            212,
            (0, 0, 422, 148, 110, 275),
            True,
        )

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png", "02.png", "02.webp"))

    @lightbulb.command()
    async def dankmeme(self, ctx: lightbulb.Context):
        """Top memes de r/dankmemes"""
        message = await ctx.respond("buscando dankmeme")
        await ctx.respond(
            get_hot_subreddit_image("dankmemes", 100, reddit_memes_history_txt, None)
        )
        await message.delete()

    @lightbulb.command()
    async def cowsay(self, ctx: lightbulb.Context, text: str, character: str = None):
        """Una vaca dice cosas

        Uso:
           fur cowsay <texto>: Vaca dice <texto>
           fur cowsay <texto> <personaje>: <personaje> dice <texto>

           Characters:
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

        await ctx.respond(output)

    @lightbulb.command()
    async def slap(self, ctx: lightbulb.Context, user: hikari.Member = None):
        """slap"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        create_meme(("slap", "01"), avatarUrl, 160, (0, 0, 120, 88), True)

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def reviento(self, ctx: lightbulb.Context, user: hikari.Member = None):
        """a que me reviento"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        create_meme(("reviento", "01"), avatarUrl, 78, (0, 0, 315, 80), True)

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def radiopatio(self, ctx: lightbulb.Context, user: hikari.Member):
        """Es hora del cotilleo"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        create_meme(("radiopatio", "01"), avatarUrl, 88, (0, 0, 188, 45), True)

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def omni(self, ctx: lightbulb.Context, user: hikari.Member = None):
        """Omniman"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        create_meme(("omni", "01"), avatarUrl, 470, (0, 0, 210, 388), True)

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def mierda(self, ctx: lightbulb.Context, user: hikari.Member = None):
        """Menudo montón de mierda"""

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar_url

        create_meme(("mierda", "01"), avatarUrl, 270, (0, 0, 476, 161), True)

        # Send meme
        await ctx.respond(attachment=meme_templates_path + "output.png")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @lightbulb.command()
    async def coche(
        self,
        ctx: lightbulb.Context,
        text1: str,
        text2: str,
        text3: str,
        user: hikari.Member,
    ):
        """Fuera de mi coche

        Uso:
            fur coche "Texto1" "Texto2" "Texto3" @usuario

        Ejemplo:
            fur coche "Gala eres rich?" "Si, tengo 5 alexas" "Fuera de mi coche" @Gala

        """

        # Get images
        r = requests.get(ctx.author.avatar_url, allow_redirects=True)
        open(meme_templates_path + "01.webp", "wb").write(r.content)
        r = requests.get(user.avatar_url, allow_redirects=True)
        open(meme_templates_path + "02.webp", "wb").write(r.content)

        # Convert images
        convert_pic(meme_templates_path + "01.webp", "01", 205)  # author
        convert_pic(meme_templates_path + "02.webp", "02", 205)  # user
        convert_pic(meme_templates_path + "02.webp", "03", 120)  # user

        # Open new image
        width, height = (
            Image.open(meme_templates_path + "coche.png").convert("RGBA").size
        )
        output = Image.new("RGBA", (width, height))  # Create picture

        # Open other images
        meme = Image.open(meme_templates_path + "coche.png").convert("RGBA")
        author_image = Image.open(meme_templates_path + "01.png").convert("RGBA")
        user_image = Image.open(meme_templates_path + "02.png").convert("RGBA")
        user_image2 = Image.open(meme_templates_path + "03.png").convert("RGBA")

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
        font = ImageFont.truetype(meme_templates_path + "Calibri.ttf", 40)
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
        output.save(meme_templates_path + "output.png", "PNG")

        await ctx.respond(attachment=meme_templates_path + "output.png")

        delete_files(("01.webp", "02.webp", "01.png", "02.png", "03.png", "output.png"))

    @lightbulb.command()
    async def sus(self, ctx: lightbulb.Context, user: hikari.Member = None):
        """Its kinda sus"""
        string = """. 　　　。　　　　•　 　ﾟ　　。 　　.

            　　　.　　　 　　.　　　　　。　　 。　. 　

            .　　 。　　　　　 ඞ 。 . 　　 • 　　　　•.                                     .

            　　ﾟ　　 {} 　 。　.

            　　'　　　  　 　　。                                          .
            。
            　　ﾟ　　　.　　　. ,　　　　.　 ."""
        impostor = " era el impostor"
        no_impostor = " no era el impostor"
        selecccion = random.choice(impostor, no_impostor)

        if user is None:
            string = string.format(ctx.author.username + selecccion)
        else:
            string = string.format(user.name + selecccion)

        await ctx.respond(string)


def load(bot: lightbulb.Bot):
    bot.add_plugin(Memes(bot))

def unload(bot:lightbulb.Bot):
    bot.remove_plugin("Memes")