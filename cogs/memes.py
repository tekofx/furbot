import random
import textwrap
import time
import wget
from PIL import ImageFont, ImageDraw
from sympy import symbols, solve
from cogs.functions import *
import discord
import logging

meme_templates_path = "resources/memes/"
memePath = "memes/"


class memes(commands.Cog):
    """Memés"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addmeme(self, context, *, arg1):
        meme_extension = "." + context.message.attachments[0].url.split(".")[-1]
        count = 1

        # Remove "
        arg1 = arg1.replace('"', "")

        # Order names in case they are not in order
        names = arg1.split()
        names.sort()
        arg1 = " ".join(names)

        # Capitalize all names
        arg1.lower()
        arg1 = arg1.title()

        # Count the number to add to the name
        if meme_extension == ".png" or meme_extension == ".jpg":
            for x in os.listdir(memePath):
                aux2 = x.split(" (", 1)
                if "jpg" in aux2[1] and aux2[0] == arg1:
                    count = count + 1

        if meme_extension == ".mp4":
            for x in os.listdir(memePath):
                aux2 = x.split(" (", 1)
                if "mp4" in x and aux2[0] == arg1:
                    count = count + 1

        count = str(count)
        if count == "0":
            meme_name = arg1
        else:
            meme_name = arg1 + " (" + count + ")"

        meme_name = meme_name.replace(" ", "_")
        meme_url = context.message.attachments[0].url
        var = (
            "wget -O "
            + memePath
            + '"'
            + meme_name
            + '"'
            + meme_extension
            + " "
            + meme_url
        )
        os.system(var)

        if meme_extension == ".png":
            im = Image.open(memePath + meme_name + meme_extension)
            rgb_im = im.convert("RGB")
            meme_extension = ".jpg"
            rgb_im.save(memePath + meme_name + meme_extension)
            os.remove(memePath + meme_name + ".png")

        old = memePath + meme_name + meme_extension
        newname = meme_name.replace("_", " ")
        new = memePath + newname + meme_extension
        os.rename(old, new)
        logging.info("Meme " + newname + " added by" + str(context.author))
        await context.channel.send("Meme " + arg1 + " añadido")

    """
    type: can be video or image
    """

    @commands.command()
    async def meme(
        self,
        context,
        name: str = None,
        tipo: str = None,
        *,
        user: discord.Member = None,
    ):
        """Meme random de los nuestros
        Uso:
            fur meme-->Meme random
            fur meme <nombre>-->Meme random de <nombre>
        """
        if name == None:
            output = random.choice(os.listdir(memePath))
            await context.channel.send(file=discord.File(memePath + output))

        else:
            uwu = []
            for filenames in os.listdir(memePath):
                if name.lower() in filenames.lower():
                    uwu.append(filenames)
            # check if exists a meme with the filters
            if len(uwu) == 0:
                await context.channel.send("No hay memes con " + name)
                return
            if (tipo == "video" and not any(".mp4" in s for s in uwu)) or (
                tipo == "imagen" and not any(".jpg" in s for s in uwu)
            ):
                await context.channel.send(
                    "No hay memes de " + tipo + " que sean de " + name
                )
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
                        print(output)

            else:
                output = random.choice(uwu)

                # Check if there are any memes with the name

            await context.channel.send(file=discord.File(memePath + output))
        logging.info("Meme sent")

    @commands.command()
    async def trauma(self, context, *, user: discord.Member = None):

        """Oh no traumita

        Uso: fur trauma "@<usuario>
        """

        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        # Create meme
        create_meme(("trauma", "01"), avatarUrl, 670, (0, 0, 39, 400), True)

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def horny(self, context, *, user: discord.Member = None):
        """Mucho horny

        Uso: fur horny "@<usuario>
        """
        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        # Create meme
        create_meme(("horny", "01"), avatarUrl, 300, (0, 0, 410, 180), True)

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def patada(self, context, *, user: discord.Member = None):
        """Te vas a comer mi pie

        Uso: fur patada "@<usuario>
        """
        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        # Create meme
        create_meme(
            ("patada", "01", "01"), avatarUrl, 110, (0, 0, 198, 229, 348, 915), True
        )

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def cringe(self, context, *, user: discord.Member = None):
        """That's cringy as fuck

        Uso: fur cringe "@<usuario>
        """

        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        # Create meme
        create_meme(("cringe", "01"), avatarUrl, 170, (0, 0, 370, 20), True)

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def burn(self, context, *, user: discord.Member = None):
        """Quema a tus amigos :)

        Uso: fur burn "@<usuario>  ---> quema a un amigo
             fur burn              ---> quémate tu solo
        """
        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        # createMeme('01', '01','burn',avatar_url=avatarUrl, avatar_size=300, position=(0,0,0,0))
        create_meme(("burn", "01"), avatarUrl, 300, (0, 0, 0, 0), False)

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def shef(self, context, *, user: discord.Member = None):
        """shef"""
        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        # createMeme('01', '01','burn',avatar_url=avatarUrl, avatar_size=300, position=(0,0,0,0))
        create_meme(("shef", "01"), avatarUrl, 120, (0, 0, 280, 87), True)

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def quote(
        self, context, quote: str, title: str, *, user: discord.Member = None
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
        userName = get_user(context, user)
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

        var = "wget -O %s%s %s" % (meme_templates_path, "01.webp", userName.avatar_url)
        print(userName.avatar_url)
        os.system(var)

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

        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")
        time.sleep(1)
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def smash(self, context, *, user: discord.Member = None):
        """Has sido invitado a Smash :0"""
        avatarUrl = get_user(context, user).avatar_url
        var = "wget -O %s%s %s" % (meme_templates_path, "01.webp", avatarUrl)
        os.system(var)
        convert_pic(meme_templates_path + "01.webp", "01", 300)

        # variables
        name = str(get_user(context, user))[:-5]  # remove #1234
        txt = "Yiffs into the fight"

        nameX = 0
        txtX = 8
        imageLayerX = 400
        imageLayerY = -40
        avatarX = 50
        avatarY = 150
        shadowcolor = "black"
        nameColor = "white"
        txtColor = "orange"

        # Calculate name font size, nameY, txtY depending on name
        var = [
            150,
            150,
            150,
            150,
            150,
            150,
            130,
            130,
            120,
            120,
            120,
            110,
            110,
            110,
            110,
            110,
            100,
            100,
            90,
            90,
            90,
            90,
            90,
        ]  # var[4]=150 text size for a name with 4 chars
        x = symbols("x")
        expr = len(name) * x - var[len(name)]
        sol = solve(expr)
        txtSize = len(name) * sol[0]

        nameY = 150 - var[len(name)]
        txtY = nameY + var[len(name)]

        # Requiremnts
        output = Image.open(meme_templates_path + "smash" + ".png").convert("RGBA")
        avatar = Image.open(meme_templates_path + "01" + ".png").convert("RGBA")

        txtPic = Image.new("RGBA", (600, 300))
        nameFont = ImageFont.truetype(
            meme_templates_path + "Haettenschweiler-Regular.ttf", txtSize
        )
        txtFont = ImageFont.truetype(
            meme_templates_path + "Haettenschweiler-Regular.ttf", 70
        )
        d = ImageDraw.Draw(txtPic)

        ## Drop shadow name
        d.text((nameX + 8, nameY + 8), name, font=nameFont, fill=shadowcolor)

        # Drop shadow txt
        d.text((txtX + 5, txtY + 5), txt, font=txtFont, fill=shadowcolor)

        # Put text above drop shadows
        d.text((nameX, nameY), name, font=nameFont, fill=nameColor)
        d.text((txtX, txtY), txt, font=txtFont, fill=txtColor)

        # Rotate text and paste it in meme
        w = txtPic.rotate(10, expand=1)
        output.paste(w, (imageLayerX, imageLayerY), w)

        # Paste avatar
        output.paste(avatar, (avatarX, avatarY), avatar)

        # Save result
        output.save(meme_templates_path + "output.png")

        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def impostor(self, context, *, user: discord.Member = None):
        """Quién es el impostor?"""
        avatarUrl = get_user(context, user).avatar_url

        create_meme(("impostor", "01"), avatarUrl, 205, (0, 0, 323, 175), True)

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def stonks(self, context, *, user: discord.Member = None):
        """Stonks"""
        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        create_meme(("stonks", "01"), avatarUrl, 236, (0, 0, 63, 25), True)

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def jojo(self, context, *, user: discord.Member):
        """Za warudo"""

        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        var = "wget -O %s%s %s" % (
            meme_templates_path,
            "02.webp",
            context.author.avatar_url,
        )
        os.system(var)
        convert_pic(meme_templates_path + "02.webp", "02", 65)

        create_meme(
            ("jojo", "01", "02"), avatarUrl, 65, (0, 0, 162, 19, 469, 130), True
        )

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png", "02.png", "02.webp"))

    @commands.command()
    async def cute(self, context, *, user: discord.Member = None):
        """You are cute"""

        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        create_meme(("cute", "01"), avatarUrl, 387, (0, 0, 210, 75), True)

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def suicidio(self, context, *, user: discord.Member = None):
        """Es hora del suisidio"""

        # Get user avatar
        avatarUrl = context.author.avatar_url

        create_meme(("suicidio", "01"), avatarUrl, 54, (0, 0, 172, 182), True)

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def coding(self, context, *, user: discord.Member = None):

        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        create_meme(("coding", "01"), avatarUrl, 167, (0, 0, 218, 137), True)

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def unsee(self, context, *, user: discord.Member = None):
        """No por favor"""

        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        create_meme(("unsee", "01"), avatarUrl, 108, (0, 0, 256, 112), True)

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def palomitas(self, context, *, user: discord.Member = None):
        """Este drama está interesante"""

        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        create_meme(("palomitas", "01"), avatarUrl, 125, (0, 0, 278, 67), True)

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def quien(
        self, context, text1: str, text2: str, *, user: discord.Member = None
    ):
        """Este drama está interesante"""
        Y = 20
        Y_aux = 10

        # draw.text((x, y),"Sample Text",(r,g,b))
        # x, y is the top-left coordinate

        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        create_meme(("quien", "01"), avatarUrl, 130, (0, 0, 210, 570), True)
        txtPic = Image.new("RGBA", (200, 200))
        img = Image.open(meme_templates_path + "output" + ".png").convert("RGBA")
        draw = ImageDraw.Draw(txtPic)
        font = ImageFont.truetype(meme_templates_path + "Calibri.ttf", 24)
        """ draw.text(((170, 30)), text, font=font, fill=(0,0,0,255))
        print('f') """

        lines = textwrap.wrap(text1, width=18)
        for line in lines:
            draw.text(((0, Y)), line, font=font, fill=(0, 0, 0, 255))
            Y = Y + 25

        draw.text(((170, 170)), text2, font=font, fill=(0, 0, 0, 255))
        img.paste(txtPic, (180, 10), txtPic)
        img.save(meme_templates_path + "output2.png", "PNG")

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output2.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        time.sleep(1)
        delete_files(("01.webp", "output.png", "01.png", "output2.png"))

    @commands.command()
    async def cojones(self, context, *, user: discord.Member):
        """Si, los cojones"""

        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        var = "wget -O %s%s %s" % (
            meme_templates_path,
            "02.webp",
            context.author.avatar_url,
        )
        os.system(var)
        convert_pic(meme_templates_path + "02.webp", "02", 146)

        create_meme(
            ("cojones", "01", "02"), avatarUrl, 175, (0, 0, 185, 431, 218, 6), True
        )

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png", "02.png", "02.webp"))

    @commands.command()
    async def tehc(self, context, *, user: discord.Member = None):
        """Tehc"""

        # Get user avatar
        avatarUrl = get_user(context, user).avatar_url

        create_meme(("tehc", "01"), avatarUrl, 140, (0, 0, 237, 7), True)

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def palanca(self, context, *, user: discord.Member):
        """Tehc"""

        # Get author avatar url
        author_avatar_url = context.author.avatar_url

        # Get parameter user avatar
        parameter_user_avatar_url = user.avatar_url
        var = "wget -O %s%s %s" % (
            meme_templates_path,
            "02.webp",
            parameter_user_avatar_url,
        )
        os.system(var)
        convert_pic(meme_templates_path + "02.webp", "02", 57)

        create_meme(
            ("palanca", "01", "02"),
            author_avatar_url,
            62,
            (0, 0, 240, 79, 137, 176),
            True,
        )

        # Send meme
        await context.channel.send(
            file=discord.File(meme_templates_path + "output.png")
        )
        logging.info("Meme sent")

        # Delete user avatar and output
        delete_files(("01.webp", "output.png", "01.png", "02.png", "02.webp"))

    @commands.command()
    async def dankmeme(self, context):
        """Top memes de r/dankmemes"""
        message = await context.channel.send("buscando dankmeme")
        await context.channel.send(get_top_reddit_image("dankmemes", 10))
        await message.delete()


def setup(bot):
    bot.add_cog(memes(bot))
