from pathlib import Path
import nextcord
from nextcord.ext import commands
import requests
from utils.data import get_server_path
from utils.functions import convert_pic
import os
from utils.bot import Bot
from utils import logger

log = logger.getLogger(__name__)

stickers_subpath = "stickers/"


class stickers(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(name="addsticker")
    async def add_sticker(self, ctx: commands.Context, sticker_name: str):
        """Añade un sticker

        Uso:
            - seleccionar una imagen y en el cuadro de "añadir comentario" poner:
            fur add <nombre_sticker>
        """
        stickers_path = get_server_path(ctx.guild) + stickers_subpath
        # If not image provided
        if not ctx.message.attachments:
            await ctx.send("Error: No se ha añadido una imagen")
            return

        # Checks if a picture is correct
        sticker_extension = ctx.message.attachments[0].url.split(".")[-1]
        if check_sticker(ctx.guild, sticker_name, sticker_extension) == 0:
            await ctx.send(
                "Error: Ya existe un sticker con el nombre {}".format(sticker_name)
            )
            return

        if sticker_extension == "jpg":
            sticker_fileName = sticker_name + ".jpg"
        else:
            sticker_fileName = sticker_name + ".png"

        stickerUrl = ctx.message.attachments[0].url

        r = requests.get(stickerUrl, allow_redirects=True)
        open(stickers_path + sticker_fileName, "wb").write(r.content)

        convert_pic(stickers_path + sticker_fileName, sticker_name)

        if sticker_extension == "jpg":
            os.remove(stickers_path + sticker_fileName)
        await ctx.send("Sticker " + sticker_name + " añadido")

    @commands.command(name="list")
    async def list_stickers(self, ctx: commands.Context):
        """Lista de los stickers añadidos"""
        stickers_path = get_server_path(ctx.guild) + stickers_subpath

        output = os.listdir(stickers_path)
        output.sort()
        output[:] = [s.replace(".png", "") for s in output]
        output = ", ".join(output)
        await ctx.send(output)

    @commands.command("s")
    async def use_sticker(self, ctx: commands.Context, sticker):
        """Usar un sticker

        Uso:
            fur s <nombre_sticker>
        """
        stickers_path = get_server_path(ctx.guild) + stickers_subpath

        if Path(stickers_path + sticker + ".png").is_file():
            stickerName = stickers_path
            stickerName += sticker
            stickerName += ".png"
            await ctx.send(file=nextcord.File(stickerName))
            log.info("Sticker " + sticker + " sent", extra={"guild": ctx.guild.id})
        else:
            await ctx.send("No existe el sticker " + sticker)

            if sticker in self.bot.all_commands:
                await ctx.send("Igual quieres usar el comando `{}`".format(sticker))


def setup(bot: commands.Bot):
    bot.add_cog(stickers(bot))


def check_sticker(guild: nextcord.Guild, stickerName: str, stickerExtension: str):
    """checks if a sticker already exists and if file extension is correct

    Args:
        guild (nextcord.Guild): guild
        stickerName ([String]): [Name of sticker to add]
        stickerExtension ([String]): [Extension of sticker to add]

    Returns:
        [0]: [name used by other sticker]
        [1]: [if file extension is correct, must be jpg or png]
    """
    stickers_path = get_server_path(guild) + stickers_subpath

    string = os.listdir(stickers_path)
    string[:] = [s.replace(".png", "") for s in string]
    string[:] = [s.replace("'", "") for s in string]
    if stickerName in string:
        return 0
    if stickerExtension in ["jpg", "png"]:
        return 1
