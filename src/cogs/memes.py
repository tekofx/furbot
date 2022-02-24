import io
import nextcord
from nextcord.ext import commands
import random
import textwrap
from PIL import ImageFont, ImageDraw
from utils.functions import (
    get_user,
)
import os
import logging
from cowpy import cow
import unicodedata
import requests
from PIL import Image
from utils.bot import Bot
from utils.data import get_server_path, meme_resources_path

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

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 300,
                "x": 410,
                "y": 180,
            }
        ]

        # Create meme
        meme = create_meme("horny", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

    @commands.command()
    async def patada(self, ctx: commands.Context, user: nextcord.Member = None):
        """Te vas a comer mi pie"""

        # Create meme
        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 110,
                "x": 198,
                "y": 229,
            },
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 85,
                "x": 348,
                "y": 915,
            },
        ]
        meme = create_meme("patada", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

    @commands.command()
    async def shef(self, ctx: commands.Context, user: nextcord.Member = None):
        """shef"""

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 120,
                "x": 280,
                "y": 87,
            }
        ]

        meme = create_meme("shef", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

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

        # Open images
        txtPic = Image.new("RGBA", (620, 500))
        pic = Image.open(meme_resources_path + "quote.png").convert("RGBA")
        avatar = (
            Image.open(io.BytesIO(requests.get(userName.avatar.url).content))
            .convert("L")
            .resize((avatarSize, avatarSize))
        )

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

    @commands.command()
    async def impostor(self, ctx: commands.Context, user: nextcord.Member = None):
        """Quién es el impostor?"""

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 205,
                "x": 323,
                "y": 175,
            }
        ]
        meme = create_meme("impostor", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

    @commands.command()
    async def stonks(self, ctx: commands.Context, user: nextcord.Member = None):
        """Stonks"""

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 236,
                "x": 63,
                "y": 25,
            }
        ]

        meme = create_meme("stonks", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

    @commands.command()
    async def jojo(self, ctx: commands.Context, user: nextcord.Member):
        """Za warudo"""

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 65,
                "x": 162,
                "y": 19,
            },
            {
                "url": ctx.author.avatar.url,
                "size": 65,
                "x": 469,
                "y": 130,
            },
        ]

        meme = create_meme("jojo", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

    @commands.command()
    async def cute(self, ctx: commands.Context, user: nextcord.Member = None):
        """You are cute"""

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 387,
                "x": 210,
                "y": 75,
            }
        ]
        meme = create_meme("cute", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

    @commands.command()
    async def suicidio(self, ctx: commands.Context):
        """Es hora del suisidio"""

        avatar_info = [
            {
                "url": ctx.author.avatar.url,
                "size": 54,
                "x": 172,
                "y": 182,
            }
        ]

        meme = create_meme("suicidio", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

    @commands.command()
    async def coding(self, ctx: commands.Context, user: nextcord.Member = None):
        """Programa como un pro hacker"""

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 167,
                "x": 218,
                "y": 137,
            }
        ]

        meme = create_meme("coding", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

    @commands.command()
    async def unsee(self, ctx: commands.Context, user: nextcord.Member = None):
        """No por favor"""

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 108,
                "x": 256,
                "y": 112,
            }
        ]

        meme = create_meme("unsee", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

    @commands.command()
    async def palomitas(self, ctx: commands.Context, user: nextcord.Member = None):
        """Este drama está interesante"""

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 125,
                "x": 278,
                "y": 67,
            }
        ]

        meme = create_meme("palomitas", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

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

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 130,
                "x": 210,
                "y": 570,
            }
        ]

        # Get user avatar
        avatarUrl = get_user(ctx, user).avatar.url

        meme = create_meme("quien", avatar_info)
        txtPic = Image.new("RGBA", (200, 200))
        img = Image.open(meme).convert("RGBA")
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

    @commands.command()
    async def palanca(self, ctx: commands.Context, user: nextcord.Member):
        """Tira de la palanca Cronk"""

        avatar_info = [
            {
                "url": ctx.author.avatar.url,
                "size": 62,
                "x": 240,
                "y": 79,
            },
            {
                "url": user.avatar.url,
                "size": 55,
                "x": 137,
                "y": 177,
            },
        ]

        meme = create_meme("palanca", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

    @commands.command()
    async def tren(self, ctx: commands.Context, user: nextcord.Member):
        """Atropella gente con un tren"""

        avatar_info = [
            {
                "url": ctx.author.avatar.url,
                "size": 212,
                "x": 422,
                "y": 148,
            },
            {
                "url": user.avatar.url,
                "size": 133,
                "x": 110,
                "y": 275,
            },
        ]

        meme = create_meme("tren", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

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

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 160,
                "x": 120,
                "y": 88,
            }
        ]

        meme = create_meme("slap", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

    @commands.command()
    async def reviento(self, ctx: commands.Context, user: nextcord.Member = None):
        """a que me reviento"""

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 78,
                "x": 315,
                "y": 80,
            }
        ]

        meme = create_meme("reviento", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

    @commands.command()
    async def radiopatio(self, ctx: commands.Context, user: nextcord.Member = None):
        """Es hora del cotilleo"""

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 88,
                "x": 188,
                "y": 45,
            }
        ]

        meme = create_meme("radiopatio", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

    @commands.command()
    async def omni(self, ctx: commands.Context, user: nextcord.Member = None):
        """Omniman"""

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 470,
                "x": 210,
                "y": 388,
            }
        ]

        meme = create_meme("omni", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

    @commands.command()
    async def mierda(self, ctx: commands.Context, user: nextcord.Member = None):
        """Menudo montón de mierda"""

        avatar_info = [
            {
                "url": get_user(ctx, user).avatar.url,
                "size": 270,
                "x": 476,
                "y": 161,
            }
        ]

        meme = create_meme("mierda", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))

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

        avatar_info = [
            {
                "url": ctx.author.avatar.url,
                "size": 205,
                "x": 171,
                "y": 0,
            },
            {
                "url": ctx.author.avatar.url,
                "size": 205,
                "x": 170,
                "y": 616,
            },
            {
                "url": user.avatar.url,
                "size": 205,
                "x": 603,
                "y": 10,
            },
            {
                "url": user.avatar.url,
                "size": 120,
                "x": 766,
                "y": 741,
            },
        ]

        meme = create_meme("coche", avatar_info)
        meme = Image.open(meme).convert("RGBA")

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

        meme.paste(txtPic1, (18, 249), txtPic1)
        meme.paste(txtPic2, (550, 260), txtPic2)
        meme.paste(txtPic3, (188, 888), txtPic3)

        # Save image
        bytes_io = io.BytesIO()
        meme.save(bytes_io, "PNG")
        bytes_io.seek(0)

        await ctx.send(file=nextcord.File(bytes_io, "output.png"))

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

        # Save image
        bytes_io = io.BytesIO()
        pic.save(bytes_io, "PNG")
        bytes_io.seek(0)

        await ctx.send(file=nextcord.File(bytes_io, "output.png"))

    @commands.command()
    async def undertale(
        self, ctx: commands.Context, texto: str, usuario: nextcord.Member = None
    ):
        """Bajo cuento"""

        avatar_info = [
            {
                "url": get_user(ctx, usuario).avatar.url,
                "size": 160,
                "x": 120,
                "y": 88,
            }
        ]
        character_image_size = 200

        # Get user
        avatar_url = get_user(ctx, usuario).avatar.url

        sprite = (
            Image.open(io.BytesIO(requests.get(avatar_url).content))
            .convert("L")
            .resize((character_image_size, character_image_size))
        )

        # Open resources
        image = Image.open(meme_resources_path + "dialogue_box.png")
        font = ImageFont.truetype(
            meme_resources_path + "Determination-Sans.otf", size=60
        )
        txtPic1 = Image.new("RGBA", (800, 270))
        draw = ImageDraw.Draw(txtPic1)

        # Convert character picture
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

        # Send image
        bytes_io = io.BytesIO()
        image.save(bytes_io, "PNG")
        bytes_io.seek(0)

        await ctx.send(file=nextcord.File(bytes_io, "output.png"))

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

        avatar_info = [
            {
                "url": user1.avatar.url,
                "size": 265,
                "x": 683,
                "y": 473,
            },
            {
                "url": user2.avatar.url,
                "size": 230,
                "x": 420,
                "y": 630,
            },
            {
                "url": user3.avatar.url,
                "size": 170,
                "x": 650,
                "y": 870,
            },
        ]
        meme = create_meme("huracan", avatar_info)

        # Send meme
        await ctx.send(file=nextcord.File(meme, "output.png"))


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
