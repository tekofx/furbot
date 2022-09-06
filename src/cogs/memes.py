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
import unicodedata
import requests
from PIL import Image
from utils.bot import Bot
from utils.data import get_server_path, meme_resources_path
from utils import logger
from nextcord import Interaction, SlashOption

log = logger.getLogger(__name__)
test_guild = 0


class memes(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="meme",
    )
    async def meme(self, interaction: Interaction):
        pass

    @meme.subcommand(
        name="add",
    )
    async def meme_add(
        self, interaction: Interaction, meme: nextcord.Attachment, nombre: str
    ):
        """Añade un meme al bot

        Args:
            meme (nextcord.Attachment): meme
            nombre (str): nombre del meme
        """
        memes_path = get_server_path(interaction.guild) + "/memes/"

        meme_extension = "." + meme.filename.split(".")[-1]
        meme_extension = meme_extension[-4:]
        count = 1

        # Remove "
        nombre = nombre.replace('"', "")

        # Remove accents
        nombre = unicodedata.normalize("NFD", nombre)
        nombre = nombre.encode("ascii", "ignore")
        nombre = nombre.decode("utf-8")

        # Capitalize all names
        nombre = nombre.lower()
        nombre = nombre.title()

        # split into a list
        names = nombre.split()

        # Order names in case they are not in order
        names = sorted(names)
        nombre = " ".join(names)

        # Count the number to add to the name
        if meme_extension == ".png" or meme_extension == ".jpg":
            for x in os.listdir(memes_path):
                aux2 = x.split(" (", 1)
                if "jpg" in aux2[1] and aux2[0] == nombre:
                    count = count + 1

        if meme_extension == ".mp4":
            for x in os.listdir(memes_path):
                aux2 = x.split(" (", 1)
                if "mp4" in x and aux2[0] == nombre:
                    count = count + 1

        count = str(count)

        nombre = nombre + " (" + count + ")"

        nombre = nombre.replace(" ", "_")
        meme_url = meme.url

        r = requests.get(meme_url, allow_redirects=True)
        open(memes_path + nombre + meme_extension, "wb").write(r.content)

        if meme_extension == ".png":
            im = Image.open(memes_path + nombre + meme_extension)
            rgb_im = im.convert("RGB")
            meme_extension = ".jpg"
            rgb_im.save(memes_path + nombre + meme_extension)
            os.remove(memes_path + nombre + ".png")

        old = memes_path + nombre + meme_extension
        newname = nombre.replace("_", " ")
        new = memes_path + newname + meme_extension
        os.rename(old, new)
        log.info(
            "Meme " + newname + " added by " + str(interaction.user),
            extra={"guild": interaction.guild.id},
        )
        await interaction.send("Meme " + newname + " añadido")

    @meme.subcommand(
        name="send",
    )
    async def meme_send(
        self,
        interaction: Interaction,
        name: str = None,
    ):
        """Envia un meme

        Args:
            name (str, optional): Nombre del meme. Defaults to None.
        """

        # If all memes have been sent, delete history
        memes_path = get_server_path(interaction.guild) + "/memes/"

        if name is None:
            output = random.choice(os.listdir(memes_path))
            async with interaction.channel.typing():
                await interaction.send(file=nextcord.File(memes_path + output))

        else:
            uwu = []
            for filenames in os.listdir(memes_path):
                if name.lower() in filenames.lower():
                    uwu.append(filenames)
            # check if exists a meme with the filters
            if len(uwu) == 0:
                await interaction.send("No hay memes con " + name)
                return

            output = random.choice(uwu)

            async with interaction.typing():
                await interaction.send(file=nextcord.File(memes_path + output))
        log.info("Meme " + output + " sent", extra={"guild": interaction.guild.id})

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="horny",
    )
    async def horny(self, interaction: Interaction, user: nextcord.Member = None):
        """Mucho horny"""

        avatar_info = [
            {
                "url": get_user(interaction, user).avatar.url,
                "size": 300,
                "x": 410,
                "y": 180,
            }
        ]

        # Create meme
        meme = create_meme("horny", avatar_info)

        # Send meme
        await interaction.send(file=nextcord.File(meme, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="patada",
    )
    async def patada(self, interaction: Interaction, user: nextcord.Member = None):
        """Te vas a comer mi pie"""

        # Create meme
        avatar_info = [
            {
                "url": get_user(interaction, user).avatar.url,
                "size": 110,
                "x": 198,
                "y": 229,
            },
            {
                "url": get_user(interaction, user).avatar.url,
                "size": 85,
                "x": 348,
                "y": 915,
            },
        ]
        meme = create_meme("patada", avatar_info)

        # Send meme
        await interaction.send(file=nextcord.File(meme, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="quote",
    )
    async def quote(
        self,
        interaction: Interaction,
        quote: str,
        titulo: str,
        user: nextcord.Member = None,
    ):
        """Crear una quote

        Args:
            quote (str): Frase graciosa. Para poner saltos de línea escribir /
            titulo (str): Titulo de la quote
            user (nextcord.Member, optional): Usuario de la quote.
        """
        # Variables

        userName = get_user(interaction, user)
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
        lines = textwrap.wrap(titulo, width=lineWidth)
        if len(lines) > 1:
            textY += 15
            for line in lines:
                width, height = fontTitle.getsize(line)
                d.text(((textX), textY), line, font=fontTitle, fill=None)
                cont += 0.4
                textY += height + 5
        else:
            d.text(((textX) + 5, textY + 30), titulo, font=fontTitle, fill=None)

        # Paste in meme picture
        pic.paste(avatar, (avatarX, avatarY), avatar)
        pic.paste(txtPic, (textOffsetX, int(220 - 20 * cont)), txtPic)

        # Save picture
        bytes_io = io.BytesIO()
        pic.save(bytes_io, "PNG")
        bytes_io.seek(0)

        await interaction.send(file=nextcord.File(bytes_io, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="stonks",
    )
    async def stonks(self, interaction: Interaction, usuario: nextcord.Member = None):
        """Stonks"""

        avatar_info = [
            {
                "url": get_user(interaction, usuario).avatar.url,
                "size": 236,
                "x": 63,
                "y": 25,
            }
        ]

        meme = create_meme("stonks", avatar_info)

        # Send meme
        await interaction.send(file=nextcord.File(meme, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="jojo",
    )
    async def jojo(self, interaction: Interaction, usuario: nextcord.Member):
        """Za warudo"""

        avatar_info = [
            {
                "url": get_user(interaction, usuario).avatar.url,
                "size": 65,
                "x": 162,
                "y": 19,
            },
            {
                "url": interaction.user.avatar.url,
                "size": 65,
                "x": 469,
                "y": 130,
            },
        ]

        meme = create_meme("jojo", avatar_info)

        # Send meme
        await interaction.send(file=nextcord.File(meme, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="cute",
    )
    async def cute(self, interaction: Interaction, usuario: nextcord.Member = None):
        """You are cute"""

        avatar_info = [
            {
                "url": get_user(interaction, usuario).avatar.url,
                "size": 387,
                "x": 210,
                "y": 75,
            }
        ]
        meme = create_meme("cute", avatar_info)

        # Send meme
        await interaction.send(file=nextcord.File(meme, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="suicidio",
    )
    async def suicidio(self, interaction: Interaction):
        """Es hora del suisidio"""

        avatar_info = [
            {
                "url": interaction.user.avatar.url,
                "size": 54,
                "x": 172,
                "y": 182,
            }
        ]

        meme = create_meme("suicidio", avatar_info)

        # Send meme
        await interaction.send(file=nextcord.File(meme, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="coding",
    )
    async def coding(self, interaction: Interaction, usuario: nextcord.Member = None):
        """Programa como un pro hacker"""

        avatar_info = [
            {
                "url": get_user(interaction, usuario).avatar.url,
                "size": 167,
                "x": 218,
                "y": 137,
            }
        ]

        meme = create_meme("coding", avatar_info)

        # Send meme
        await interaction.send(file=nextcord.File(meme, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="unsee",
    )
    async def unsee(self, interaction: Interaction, usuario: nextcord.Member = None):
        """No por favor"""

        avatar_info = [
            {
                "url": get_user(interaction, usuario).avatar.url,
                "size": 108,
                "x": 256,
                "y": 112,
            }
        ]

        meme = create_meme("unsee", avatar_info)

        # Send meme
        await interaction.send(file=nextcord.File(meme, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="palomitas",
    )
    async def palomitas(self, interaction: Interaction):
        """Este drama está interesante"""

        avatar_info = [
            {
                "url": interaction.user.avatar.url,
                "size": 125,
                "x": 278,
                "y": 67,
            }
        ]

        meme = create_meme("palomitas", avatar_info)

        # Send meme
        await interaction.send(file=nextcord.File(meme, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="quien",
    )
    async def quien(
        self,
        interaction: Interaction,
        pregunta: str,
        respuesta: str = SlashOption(name="respuesta", choices={"Si", "No"}),
        usuario: nextcord.Member = None,
    ):
        """Meme de quien es quien

        Args:
            pregunta (str): Pregunta de quien es quien
            respuesta (str): Respuesta de si/no
            usuario (nextcord.Member, optional): Usuario
        """

        Y = 20

        avatar_info = [
            {
                "url": get_user(interaction, usuario).avatar.url,
                "size": 130,
                "x": 210,
                "y": 570,
            }
        ]

        meme = create_meme("quien", avatar_info)
        txtPic = Image.new("RGBA", (200, 200))
        img = Image.open(meme).convert("RGBA")
        draw = ImageDraw.Draw(txtPic)
        font = ImageFont.truetype(meme_resources_path + "Calibri.ttf", 24)

        lines = textwrap.wrap(pregunta, width=18)
        for line in lines:
            draw.text(((0, Y)), line, font=font, fill=(0, 0, 0, 255))
            Y = Y + 25

        draw.text(((170, 170)), respuesta, font=font, fill=(0, 0, 0, 255))
        img.paste(txtPic, (180, 10), txtPic)

        # Save
        bytes_io = io.BytesIO()
        img.save(bytes_io, "PNG")
        bytes_io.seek(0)

        # Send meme
        await interaction.send(file=nextcord.File(bytes_io, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="palanca",
    )
    async def palanca(self, interaction: Interaction, usuario: nextcord.Member):
        """Tira de la palanca Cronk"""

        avatar_info = [
            {
                "url": interaction.user.avatar.url,
                "size": 62,
                "x": 240,
                "y": 79,
            },
            {
                "url": usuario.avatar.url,
                "size": 55,
                "x": 137,
                "y": 177,
            },
        ]

        meme = create_meme("palanca", avatar_info)

        # Send meme
        await interaction.send(file=nextcord.File(meme, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="tren",
    )
    async def tren(self, interaction: Interaction, user: nextcord.Member):
        """Atropella gente con un tren"""

        avatar_info = [
            {
                "url": interaction.user.avatar.url,
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
        await interaction.send(file=nextcord.File(meme, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="slap",
    )
    async def slap(self, interaction: Interaction, usuario: nextcord.Member = None):
        """slap"""

        avatar_info = [
            {
                "url": get_user(interaction, usuario).avatar.url,
                "size": 160,
                "x": 120,
                "y": 88,
            }
        ]

        meme = create_meme("slap", avatar_info)

        # Send meme
        await interaction.send(file=nextcord.File(meme, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="reviento",
    )
    async def reviento(self, interaction: Interaction):
        """a que me reviento"""

        avatar_info = [
            {
                "url": interaction.user.avatar.url,
                "size": 78,
                "x": 315,
                "y": 80,
            }
        ]

        meme = create_meme("reviento", avatar_info)

        # Send meme
        await interaction.send(file=nextcord.File(meme, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="radiopatio",
    )
    async def radiopatio(
        self, interaction: Interaction, usuario: nextcord.Member = None
    ):
        """Es hora del cotilleo"""

        avatar_info = [
            {
                "url": get_user(interaction, usuario).avatar.url,
                "size": 88,
                "x": 188,
                "y": 45,
            }
        ]

        meme = create_meme("radiopatio", avatar_info)

        # Send meme
        await interaction.send(file=nextcord.File(meme, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="coche",
    )
    async def coche(
        self,
        interaction: Interaction,
        texto1: str,
        texto2: str,
        texto3: str,
        usuario: nextcord.Member,
    ):
        """Fuera de mi coche"""

        avatar_info = [
            {
                "url": interaction.user.avatar.url,
                "size": 205,
                "x": 171,
                "y": 0,
            },
            {
                "url": interaction.user.avatar.url,
                "size": 205,
                "x": 170,
                "y": 616,
            },
            {
                "url": usuario.avatar.url,
                "size": 205,
                "x": 603,
                "y": 10,
            },
            {
                "url": usuario.avatar.url,
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
        lines1 = textwrap.wrap(texto1, width=25)
        for line in lines1:
            draw.text(((10, Y)), line, font=font, fill=(255, 255, 255, 255))
            Y = Y + 40

        Y = 8
        txtPic2 = Image.new("RGBA", (320, 220))
        draw = ImageDraw.Draw(txtPic2)
        lines2 = textwrap.wrap(texto2, width=19)
        for line in lines2:
            draw.text(((10, Y)), line, font=font, fill=(255, 255, 255, 255))
            Y = Y + 40

        Y = 8
        txtPic3 = Image.new("RGBA", (540, 120))
        draw = ImageDraw.Draw(txtPic3)
        lines3 = textwrap.wrap(texto3, width=30)
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

        await interaction.send(file=nextcord.File(bytes_io, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="skeletor",
    )
    async def skeletor(self, interaction: Interaction, texto1: str, texto2: str):
        """Datos perturbadores de Skeletor"""

        meme_width = 994
        meme_hegiht = 680
        txtPic1 = Image.new("RGBA", (meme_width, meme_hegiht))
        pic = Image.open(meme_resources_path + "skeletor.png").convert("RGBA")
        font = ImageFont.truetype(meme_resources_path + "impact.ttf", 60)
        d = ImageDraw.Draw(txtPic1)

        # Write text1
        lines = textwrap.wrap(texto1.upper(), width=35)
        textY = 0
        for line in lines:
            width, height = font.getsize(line)

            d.text(((meme_width - width) / 2, textY), line, font=font, fill=None)
            textY += height

        lines = textwrap.wrap(texto2.upper(), width=35)
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

        await interaction.send(file=nextcord.File(bytes_io, "output.png"))

    @nextcord.slash_command(
        guild_ids=[test_guild],
        name="huracan",
    )
    async def huracan(
        self,
        interaction: Interaction,
        usuario1: nextcord.Member,
        usuario2: nextcord.Member,
        usuario3: nextcord.Member,
    ):
        """Jaja huracán"""

        avatar_info = [
            {
                "url": usuario1.avatar.url,
                "size": 265,
                "x": 683,
                "y": 473,
            },
            {
                "url": usuario2.avatar.url,
                "size": 230,
                "x": 420,
                "y": 630,
            },
            {
                "url": usuario3.avatar.url,
                "size": 170,
                "x": 650,
                "y": 870,
            },
        ]
        meme = create_meme("huracan", avatar_info)

        # Send meme
        await interaction.send(file=nextcord.File(meme, "output.png"))


def create_meme(meme_picture: str, avatars_info: list) -> io.BytesIO:
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
