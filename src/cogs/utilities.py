import logging
import discord
from discord.ext import commands
import asyncio
import random
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import qrcode
import datetime
from pyrae import dle
import requests
from functions import (
    get_user,
    get_user_species,
    get_user_color,
    get_user_ranks,
    get_user_roles,
    convert_pic,
    meme_templates_path,
    delete_files,
    yaml_f,
)
from functions import magnet_id, angel_id


class utilities(commands.Cog):
    """Utilidades varias"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, context):
        await context.channel.send("Pim pam trucu trucu")

    @commands.command()
    async def random(self, context, min_num: int = None, max_num: int = None):
        """Genera un número aleatorio

        Uso: fur random                 ---> Genera un numero entre 1 y 100
             fur random <min_num> <max_num>     ---> Genera un numero entre <min_num> y <max_num>
        """

        if min_num and max_num is not None:
            num = str(random.randint(min_num, max_num))
        else:
            num = str(random.randint(0, 100))
        tmp = await context.channel.send("Generando número aleatorio")

        await tmp.edit(content="Generando número aleatorio.")
        await asyncio.sleep(0.2)
        await tmp.edit(content="Generando número aleatorio..")
        await asyncio.sleep(0.2)
        await tmp.edit(content="Generando número aleatorio...")
        await asyncio.sleep(0.2)
        await tmp.edit(content="Generando número aleatorio....")
        await asyncio.sleep(0.2)
        await tmp.edit(content="Generando número aleatorio.....")
        await asyncio.sleep(0.2)
        await tmp.edit(content="Numero aletorio: " + num)

    @commands.command()
    async def carnet(self, context, *args):
        """Muestra tu carnet como miembro de Villa Furrense

        Uso:
            fur carnet: Muestra tu carnet por defecto
            fur carnet <diseño>: Muestra tu carnet con diseño <diseño>
            fur carnet <usuario> : Muestra carnet por defecto de <usuario>
            fur carnet <usuario> <diseño>: Muestra carnet con diseño <diseño> de <usuario>


        Diseños: 1,2
        """

        user = None
        design = None
        for arg in args:
            if "@" in arg:
                arg = int(arg.strip("<@!>"))
                user = await context.guild.fetch_member(int(arg))
            else:
                design = arg

        # Get user info
        usr = get_user(context, user)
        name = usr.display_name
        species = get_user_species(usr)
        rank = get_user_ranks(usr)
        roles = get_user_roles(usr)
        color = get_user_color(usr)
        color = yaml_f.get_color_code(color)
        if usr.id == magnet_id:
            date = "24-01-2021"
        elif usr.id == angel_id:
            date = "17-03-2020"
        else:
            date = str(usr.joined_at)
            date = date.split()
            date = date[0].split("-")
            date = date[2] + "-" + date[1] + "-" + date[0]

        # Create qr code
        qr_text = (
            "Nombre: "
            + name
            + "\n"
            + "Especie: "
            + species
            + "\n"
            + "Rango: "
            + rank
            + "\n"
            + "Fecha: "
            + date
        )
        img = qrcode.make(qr_text)
        img = img.resize((250, 250))

        # Get user avatar
        r = requests.get(usr.avatar_url, allow_redirects=True)
        open(meme_templates_path + "01.webp", "wb").write(r.content)

        convert_pic(meme_templates_path + "01.webp", "01", 1000)
        user_avatar = meme_templates_path + "01.png"
        avatar = Image.open(user_avatar)

        if design is None or design == "1":
            # Open carnet to draw
            output = Image.open("files/resources/utilities/carnet.png").convert("RGBA")
            draw = ImageDraw.Draw(output)
            font = ImageFont.truetype(meme_templates_path + "Calibri.ttf", 40)

            # Draw name
            draw.text(((425, 266)), name, font=font, fill=(0, 0, 0, 255))

            # Draw species
            draw.text(((425, 388)), species, font=font, fill=(0, 0, 0, 255))

            # Draw rank
            draw.text(((425, 518)), rank, font=font, fill=(0, 0, 0, 255))

            # Draw time in server
            draw.text(((425, 646)), date, font=font, fill=(0, 0, 0, 255))

            # Add avatar
            avatar = avatar.resize((300, 300))
            output.paste(avatar, (50, 250))

            # Add discord nitro badge
            if "Furrense Booster" in roles:
                booster = Image.open("files/resources/utilities/booster.png").convert(
                    "RGBA"
                )
                booster = booster.resize((140, 140))
                output.paste(booster, (1090, 530), booster)

            # Add qrcode
            output.paste(img, (1030, 250))

            # Save carnet
            output.save(meme_templates_path + "output.png", "PNG")
            await context.channel.send(
                file=discord.File(meme_templates_path + "output.png")
            )
        if design == "2":
            W = 1100

            # Open carnet design to draw
            carnet_design = Image.open("files/resources/utilities/carnet2.png").convert(
                "RGBA"
            )
            draw = ImageDraw.Draw(carnet_design)
            font = ImageFont.truetype(meme_templates_path + "Calibri.ttf", 60)
            font_bold = ImageFont.truetype(meme_templates_path + "Calibri_bold.ttf", 65)

            # Add avatar
            avatar = avatar.resize((400, 400))
            carnet_design.paste(avatar, (380, 150))

            # Draw name
            w, h = draw.textsize(name, font=font)
            size = W - w
            draw.text((size / 2, 576), name, font=font_bold, fill=(0, 0, 0, 255))

            # Draw rank
            w, h = draw.textsize(rank, font=font)
            size = W - w
            draw.text((size / 2, 670), rank, font=font, fill=(73, 73, 73, 255))

            # Draw species
            w, h = draw.textsize(species, font=font)
            size = W - w
            draw.text((size / 2, 765), species, font=font, fill=(0, 0, 0, 255))

            # Draw time in server
            w, h = draw.textsize(date, font=font)
            size = W - w
            draw.text((size / 2, 873), date, font=font, fill=(0, 0, 0, 255))

            # Add qrcode
            img = img.resize((460, 460))
            carnet_design.paste(img, (340, 980))

            # Add discord nitro badge
            if "Furrense Booster" in roles:
                booster = Image.open("files/resources/utilities/booster.png").convert(
                    "RGBA"
                )
                booster = booster.resize((140, 140))
                carnet_design.paste(booster, (10, 10), booster)

            # Add color to carnet
            output = Image.new("RGB", (1100, 1700), (color[0], color[1], color[2]))
            output.paste(carnet_design, (0, 0), carnet_design)

            # Save carnet
            output.save(meme_templates_path + "output.png", "PNG")
            await context.channel.send(
                file=discord.File(meme_templates_path + "output.png")
            )

        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def avatar(self, context, *, user: discord.Member = None):
        """Obtén la imagen de perfil de alguien"""

        avatar_url = get_user(context, user).avatar_url

        r = requests.get(avatar_url, allow_redirects=True)
        open(meme_templates_path + "01.webp", "wb").write(r.content)

        convert_pic(meme_templates_path + "01.webp", "01")
        await context.channel.send(file=discord.File(meme_templates_path + "01.png"))
        delete_files(("01.webp", "01.png"))

    @commands.command()
    async def rae(self, context, *, search: str):
        """Obtén la imagen de perfil de alguien"""
        tmp = await context.channel.send("Buscando en la RAE")

        output = str(dle.search_by_word(search))

        if "«Diccionario de la lengua española»" in output:
            await tmp.edit(content="Termino no encontrado")
        else:
            await tmp.edit(content=output)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def addcumple(self, context, birthday: str, user: discord.Member):
        """[Admin] Añade el cumpleaños de alguien al bot

        Uso:
            fur addcumple <dia>-<mes> @<usuario>

        Ejemplo:
            fur addcumple 16-1 @Teko
        """
        birthday = birthday.split("-")
        birthday = birthday[1] + "-" + birthday[0]
        day = int(birthday[0])
        month = int(birthday[1])
        datetime.datetime(2000, month, day)
        logging.info("Added birthday of " + user.name + ": " + birthday)
        await context.channel.send("Añadido cumpleaños de " + user.name)

    @commands.command()
    async def cumple(self, context, user: discord.Member):
        """Muestra cumpleaños de un usuario

        Uso:
            fur cumple @<usuario>

        Ejemplo:
            fur cumple @Teko
        """
        output = "No existe el cumpleaños de " + user.name
        data = yaml_f.get_cumpleaños()
        dates = data[0]
        user_ids = data[1]
        print(user_ids)
        for x in range(len(dates)):
            print(dates[x])
            if user_ids[x] == user.id:
                output = "El cumpleaños de {user} es el {cumple}".format(
                    user=user.name, cumple=dates[x]
                )
                break
        await context.channel.send(output)


def setup(bot):
    bot.add_cog(utilities(bot))
