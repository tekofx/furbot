import io
from ntpath import join
import nextcord
from nextcord.ext import commands
from pyrae import dle
import requests
from utils.database import get_roles_by_type
from utils.bot import Bot
from PIL import Image, ImageOps, ImageFont, ImageDraw


class utilities(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def ping(self, context):
        await context.channel.send("Pim pam trucu trucu")

    @commands.command()
    async def carnet(self, context: commands.Context, user: nextcord.Member = None):
        if not user:
            user = context.author

        name = user.name
        joined_date = user.joined_at
        joined_date = (
            str(joined_date.day)
            + "-"
            + str(joined_date.month)
            + "-"
            + str(joined_date.year)
        )
        roles = user.roles
        color = user.colour

        # Get avatar and make it round
        avatar = user.avatar.url
        avatar = io.BytesIO(requests.get(avatar).content)
        avatar = Image.open(avatar).convert("RGBA").resize((80, 80))
        mask = Image.open("data/resources/mask.png").convert("L")
        avatar = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        avatar.putalpha(mask)

        # Create canvas
        canvas = Image.new("RGB", (400, 200), color="white")
        canvas.paste(avatar, (20, 20), avatar)

        # Create text image
        txt_pic = Image.new("RGBA", (200, 100))
        font = ImageFont.truetype("data/resources/calibri.ttf", size=20)
        draw = ImageDraw.Draw(txt_pic)

        # Draw text
        draw.text((10, 20), name, "black", font=font)
        draw.text((10, 40), joined_date, "black", font=font)

        canvas.paste(txt_pic, (150, 20), txt_pic)

        # Send
        bytes_io = io.BytesIO()
        canvas.save(bytes_io, "PNG")
        bytes_io.seek(0)
        await context.send(file=nextcord.File(bytes_io, "output.png"))

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


def setup(bot: commands.Bot):
    bot.add_cog(utilities(bot))
