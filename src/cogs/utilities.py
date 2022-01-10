import nextcord
from nextcord.ext import commands
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import qrcode
from pyrae import dle
import requests
from utils.functions import (
    convert_pic,
    meme_templates_path,
    delete_files,
)

from utils.database import (
    create_connection,
    get_birthday,
    get_colors,
    get_ranks,
    get_species,
)
from utils.bot import Bot


class utilities(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def ping(self, context):
        await context.channel.send("Pim pam trucu trucu")

    # TODO
    @commands.command()
    async def carnet(self, ctx: commands.Context, user: nextcord.Member, design: str):
        # Get user info
        usr = user
        name = usr.display_name
        species = get_user_species(usr)
        rank = get_user_ranks(usr)
        roles = get_user_roles(usr)
        color = get_user_color_code(usr)

        """ if int(usr.id) == magnet_id:
            date = "24-01-2021"
        elif int(usr.id) == angel_id:
            date = "17-03-2020"
        else: """
        date = str(usr.created_at)
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
            await ctx.respond(attachment=meme_templates_path + "output.png")
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
            output = Image.new("RGB", (1100, 1700), color)
            output.paste(carnet_design, (0, 0), carnet_design)

            # Save carnet
            output.save(meme_templates_path + "output.png", "PNG")
            await ctx.respond(attachment=meme_templates_path + "output.png")

        delete_files(("01.webp", "output.png", "01.png"))

    @commands.command()
    async def rae(self, ctx: commands.Context, palabra: str):
        """Obtiene una definición de la RAE

        Uso:
            fur rae <palabra>
        """

        tmp = await ctx.send("Buscando en la RAE")

        output = str(dle.search_by_word(palabra))

        if "«Diccionario de la lengua española»" in output:
            await tmp.edit(content="Termino no encontrado")
        else:
            await tmp.edit(content=output)

    @commands.command()
    async def cumple(self, ctx: commands.Context, user: nextcord.Member):
        """Obtiene el cumpleaños de un usuario

        Uso:
            fur cumple @<usuario>
        """
        con = create_connection(str(ctx.guild.id))

        output = "No existe el cumpleaños de " + user.display_name
        birthday = get_birthday(con, user.id).split("-")
        day = birthday[2]
        month = birthday[1]
        birthday = str(day) + "-" + str(month)

        output = "El cumpleaños de {user} es el {cumple}".format(
            user=user.display_name, cumple=birthday
        )
        await ctx.send(output)


def setup(bot: commands.Bot):
    bot.add_cog(utilities(bot))


def get_user_species(user: nextcord.Member):
    """Get user roles that are species

    Args:
        user (nextcord.Member): user to search for roles

    Returns:
        str: String containing roles
    """
    con = create_connection(user.guild.id)
    server_species = get_species(con)
    mention = []
    roles = user.roles
    for role in roles:
        if role.id in server_species:
            mention.append(role.name)

    b = ", ".join(mention)
    return b


def get_user_roles(user: nextcord.Member):
    """Get user roles that are not ranks

    Args:
        user (nextcord.Member): user to search for roles

    Returns:
        str: String containing roles
    """
    con = create_connection(user.guild.id)

    server_ranks = get_ranks(con)
    mention = []
    roles = user.roles

    for role in roles:
        if role.id in server_ranks:
            mention.append(role.name)

    b = ", ".join(mention)
    return str(b)


def get_user_ranks(user: nextcord.Member):
    """Get ranks from a user

    Args:
        user (nextcord.User): user to search for roles

    Returns:
        str: String containing all ranks
    """
    con = create_connection(user.guild.id)
    server_ranks = get_ranks(con)
    output = []
    roles = user.roles

    for role in roles:
        if role.id in server_ranks:
            output.append(role.name)
    if output:
        b = ", ".join(output)
    else:
        return "Admin"
    return str(b)


def get_user_color_code(user: nextcord.Member):
    """Get user roles that are not ranks

    Args:
        user (nextcord.User): user to search for roles

    Returns:
        str: String containing roles
    """
    con = create_connection(user.guild_id)

    server_colors = get_colors(con)
    roles = user.roles

    for role in roles:
        if role.id in server_colors:
            return role.colour.value
