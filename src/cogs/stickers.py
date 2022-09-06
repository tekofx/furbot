from pathlib import Path
import nextcord
from nextcord.ext import commands
import requests
from utils.data import get_server_path
from utils.functions import convert_pic
import os
from utils.bot import Bot
from utils import logger
from nextcord import Interaction

log = logger.getLogger(__name__)

stickers_subpath = "stickers/"

local_guild = os.getenv("LOCAL_GUILD")


class stickers(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(
        guild_ids=[local_guild],
        name="sticker",
    )
    async def sticker(self, interaction: Interaction):
        pass

    @sticker.subcommand(
        name="add",
        description="Añade un sticker",
    )
    async def sticker_add(
        self, interaction: Interaction, nombre: str, image: nextcord.Attachment
    ):
        stickers_path = get_server_path(interaction.guild) + stickers_subpath

        # Checks if a picture is correct
        sticker_extension = image.filename.split(".")[-1]
        if check_sticker(interaction.guild, nombre, sticker_extension) == 0:
            await interaction.send(
                "Error: Ya existe un sticker con el nombre {}".format(nombre)
            )
            return

        if sticker_extension == "jpg":
            sticker_fileName = nombre + ".jpg"
        else:
            sticker_fileName = nombre + ".png"

        stickerUrl = image.url

        r = requests.get(stickerUrl, allow_redirects=True)
        open(stickers_path + sticker_fileName, "wb").write(r.content)

        convert_pic(stickers_path + sticker_fileName, nombre)

        if sticker_extension == "jpg":
            os.remove(stickers_path + sticker_fileName)
        await interaction.send("Sticker " + nombre + " añadido")

    @sticker.subcommand(
        name="list",
        description="Lista de los stickers añadidos",
    )
    async def sticker_list(self, interaction: Interaction):
        stickers_path = get_server_path(interaction.guild) + stickers_subpath

        output = os.listdir(stickers_path)
        output.sort()
        output[:] = [s.replace(".png", "") for s in output]
        output = ", ".join(output)
        await interaction.send(output)

    @sticker.subcommand(
        name="use",
        description="Usar un sticker",
    )
    async def sticker_use(
        self,
        interaction: Interaction,
        sticker: str,
    ):
        """Usar un sticker

        Uso:
            fur s <nombre_sticker>
        """
        stickers_path = get_server_path(interaction.guild) + stickers_subpath

        if Path(stickers_path + sticker + ".png").is_file():
            stickerName = stickers_path
            stickerName += sticker
            stickerName += ".png"
            await interaction.send(file=nextcord.File(stickerName))
            log.info(
                "Sticker " + sticker + " sent", extra={"guild": interaction.guild.id}
            )
        else:
            await interaction.send("No existe el sticker " + sticker)

            if sticker in self.bot.all_commands:
                await interaction.send(
                    "Igual quieres usar el comando `{}`".format(sticker)
                )


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
