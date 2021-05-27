import discord
from discord.ext import commands
import os
from PIL import Image
from discord.ext.commands.core import command
from cogs.functions import *
from pathlib import Path
import logging


class stickers(commands.Cog):
    """Discord es una kk y no tiene stickers pero yo si :)"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addsticker")
    async def add_sticker(self, context, arg1):
        """Añade un sticker

        Uso: seleccionar una imagen y en el cuadro de "añadir comentario"
        poner fur add <nombre_sticker>
        """

        if not context.message.attachments:
            logging.error("Image not provided")
            await context.channel.send("Falta el sticker a añadir")

        else:
            # Checks if a picture is correct
            sticker_extension = context.message.attachments[0].url.split(".")[-1]
            if check_sticker(arg1, sticker_extension) == 0:
                logging.error("Name already in use")
                await context.channel.send("El nombre de sticker ya existe")
                return

            if sticker_extension == "jpg":
                sticker_fileName = arg1 + ".jpg"
            else:
                sticker_fileName = arg1 + ".png"

            stickerUrl = context.message.attachments[0].url
            var = "wget -O %s%s %s" % (stickersPath, sticker_fileName, stickerUrl)
            stickerPath = "%s%s" % (stickersPath, sticker_fileName)
            os.system(var)
            convert_pic(stickerPath, arg1)

            if sticker_extension == "jpg":
                var2 = "rm " + stickerPath
                os.system(var2)
            await context.channel.send("Sticker " + arg1 + " añadido")

    @commands.command()
    async def list(self, context):
        """Nombre de los stickers añadidos"""
        output = os.listdir(stickersPath)
        output.sort()
        output[:] = [s.replace(".png", "") for s in output]
        output = ", ".join(output)
        await context.channel.send(output)

    @commands.command(name="s")
    async def use_sticker(self, context, sticker):
        """Usar un sticker

        Uso: fur s <nombre_sticker>
        """
        if Path(stickersPath + sticker + ".png").is_file():
            stickerName = stickersPath
            stickerName += sticker
            stickerName += ".png"
            await context.channel.send(file=discord.File(stickerName))
            logging.info("Sticker " + sticker + " sent")
        else:

            await context.channel.send("No existe el sticker " + sticker)

            # If sticker is confused with meme
            for command in self.bot.commands:
                if sticker == command.name:
                    await context.send("Igual quisiste usar el comando `fur "+sticker +'`')
                    break
            
            # If command fur list is wrong used
            if sticker == "list":
                await context.channel.send("Prueba con `fur list`")
            logging.error("Sticker " + sticker + " does not exist")

    @commands.command(name="rm")
    @commands.check(is_admin)
    async def remove_sticker(self, context, sticker):
        """[ADMIN] Borra un sticker"""
        os.system("rm " + stickersPath + sticker + ".png")
        logging.info("Sticker " + sticker + " deleted")
        await context.channel.send("Sticker " + sticker + " eliminado")

    @commands.command(name="edit")
    @commands.check(is_admin)
    async def edit_sticker(self, context, sticker_before, sticker_after):
        """[ADMIN] Cambia nombre a un sticker"""
        os.system(
            "mv "
            + stickersPath
            + sticker_before
            + ".png "
            + stickersPath
            + sticker_after
            + ".png"
        )
        logging.info("Sticker " + sticker_before + " edited")
        await context.channel.send(
            "Cambiado nombre del sticker " + sticker_before + " a " + sticker_after
        )


# Resize and image and save it as png
def convert_pic(picture: str, stickerName: str):
    """Converts a picture to a sticker

    Args:
        picture (str): [picture to convert]
        stickerName (str): [name of the sticker to be created]
    """

    img = Image.open(picture)
    wpercent = stickerSize / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((stickerSize, hsize), Image.ANTIALIAS)
    img.save(stickersPath + stickerName + ".png")


def check_sticker(stickerName: str, stickerExtension: str):
    """checks if a sticker already exists and if file extension is correct

    Args:
        stickerName ([String]): [Name of sticker to add]
        stickerExtension ([String]): [Extension of sticker to add]

    Returns:
        [0]: [name used by other sticker]
        [1]: [if file extension is correct, must be jpg or png]
    """
    str = os.listdir(stickersPath)
    str[:] = [s.replace(".png", "") for s in str]
    str[:] = [s.replace("'", "") for s in str]
    if stickerName in str:
        return 0
    if stickerExtension in ["jpg", "png"]:
        return 1


def setup(bot):
    bot.add_cog(stickers(bot))
