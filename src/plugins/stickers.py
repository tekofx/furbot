import lightbulb
from functions import stickers_path, stickerSize
import requests
import os
from PIL import Image
from pathlib import Path
from hikari import permissions


class Stickers(lightbulb.Plugin):
    def __init__(self, bot: lightbulb.Bot):
        super().__init__(name="Stickers")
        self.bot = bot

    @lightbulb.command(name="addsticker")
    async def add_sticker(self, ctx: lightbulb.Context, sticker_name: str):
        """Añade un sticker

        Uso: seleccionar una imagen y en el cuadro de "añadir comentario"
        poner fur add <nombre_sticker>
        """

        # If not image provided
        if not ctx.attachments:
            await ctx.respond("Error: No se ha añadido una imagen")
            return

        # Checks if a picture is correct
        sticker_extension = ctx.attachments[0].url.split(".")[-1]
        if check_sticker(sticker_name, sticker_extension) == 0:
            await ctx.respond(
                "Error: Ya existe un sticker con el nombre {}".format(sticker_name)
            )
            return

        if sticker_extension == "jpg":
            sticker_fileName = sticker_name + ".jpg"
        else:
            sticker_fileName = sticker_name + ".png"

        stickerUrl = ctx.attachments[0].url

        r = requests.get(stickerUrl, allow_redirects=True)
        open(stickers_path + sticker_fileName, "wb").write(r.content)

        convert_pic(stickers_path + sticker_fileName, sticker_name)

        if sticker_extension == "jpg":
            os.remove(stickers_path + sticker_fileName)
        await ctx.respond("Sticker " + sticker_name + " añadido")

    @lightbulb.command()
    async def list(self, ctx: lightbulb.Context):
        """Nombre de los stickers añadidos"""
        output = os.listdir(stickers_path)
        output.sort()
        output[:] = [s.replace(".png", "") for s in output]
        output = ", ".join(output)
        await ctx.respond(output)

    @lightbulb.command(name="s")
    async def use_sticker(self, ctx: lightbulb.Context, sticker):
        """Usar un sticker

        Uso: fur s <nombre_sticker>
        """
        if Path(stickers_path + sticker + ".png").is_file():
            stickerName = stickers_path
            stickerName += sticker
            stickerName += ".png"
            await ctx.respond(attachment=stickerName)
            # logging.info("Sticker " + sticker + " sent")
        else:

            await ctx.respond("No existe el sticker " + sticker)

            # If sticker is confused with meme
            # for command in self.bot.commands:
            #    if sticker == command.name:
            #        raise commands.CommandError("confused_sticker_meme", sticker)
            #
            # if exists_substring_in_file(sticker, stickers_path):
            #    raise commands.CommandError("wrong_sticker_name", sticker)
            #
            ## If command fur list is wrong used
            # if sticker == "list":
            #    raise commands.CommandError("use_list_as_sticker")
            # logging.error("Sticker " + sticker + " does not exist")

    @lightbulb.check(
        lightbulb.has_guild_permissions(permissions.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command(name="rm")
    async def remove_sticker(self, ctx: lightbulb.Context, sticker):
        """[ADMIN] Borra un sticker"""
        os.remove(stickers_path + sticker + ".png")
        # logging.info("Sticker " + sticker + " deleted")
        await ctx.respond("Sticker " + sticker + " eliminado")

    @lightbulb.check(
        lightbulb.has_guild_permissions(permissions.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command(name="edit")
    async def edit_sticker(self, ctx: lightbulb.Context, sticker_before, sticker_after):
        """[ADMIN] Cambia nombre a un sticker"""
        old_name = stickers_path + sticker_before + ".png"
        new_name = stickers_path + sticker_after + ".png"
        os.rename(old_name, new_name)
        # logging.info("Sticker " + sticker_before + " edited")
        await ctx.respond(
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
    img.save(stickers_path + stickerName + ".png")


def check_sticker(stickerName: str, stickerExtension: str):
    """checks if a sticker already exists and if file extension is correct

    Args:
        stickerName ([String]): [Name of sticker to add]
        stickerExtension ([String]): [Extension of sticker to add]

    Returns:
        [0]: [name used by other sticker]
        [1]: [if file extension is correct, must be jpg or png]
    """
    string = os.listdir(stickers_path)
    string[:] = [s.replace(".png", "") for s in string]
    string[:] = [s.replace("'", "") for s in string]
    if stickerName in string:
        return 0
    if stickerExtension in ["jpg", "png"]:
        return 1


def load(bot: lightbulb.Bot):
    bot.add_plugin(Stickers(bot))


def unload(bot: lightbulb.Bot):
    bot.remove_plugin("Stickers")
