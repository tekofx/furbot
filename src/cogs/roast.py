import logging
import nextcord
from nextcord.ext import commands
from utils.functions import get_random_line_of_file, magnet_id, insults_txt, animos_txt
from utils.bot import Bot

log = logging.getLogger(__name__)


class roast(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def tecute(self, ctx: commands.Context):
        """Teko cute"""
        if ctx.author.id is magnet_id:
            await ctx.send("Teko cute")
        else:
            await ctx.send("Teko NO cute")

    @commands.command()
    async def teodio(self, ctx: commands.Context, user: nextcord.Member = None):
        """Muestra tu odio al bot"""
        await ctx.reply(content="Yo te odio mas pedazo de basura")

    @commands.command()
    async def insult(self, ctx: commands.Context, user: nextcord.Member = None):
        """Insulta gente 7w7

        Genera un insulto aleatorio
        """

        try:
            output = get_random_line_of_file(insults_txt)
            if user is None:
                await ctx.reply(content=output)
            else:
                await ctx.send(content=user.mention + " " + output)
        except Exception:
            log.error("Error: {}".format(Exception))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addinsult(self, ctx, *insults: str):
        """[ADMIN] Añade insulto

        Uso:
            fur addinsulto <insulto>
            fur addinsulto <insulto1> <insulto2>...

        Ejemplo:
            fur addinsulto "feo" "horrible"
        """
        try:
            f = open(insults_txt, "a")
            for insult in insults:
                insult = insult.replace('"', "")
                f.write(insult + "\n")
            f.close()
            await ctx.reply("Insulto/s añadido/s")
        except Exception:
            log.error("Error: {}".format(Exception))

    @commands.command()
    async def animo(self, ctx: commands.Context, user: nextcord.Member = None):
        """Anima a la gente"""
        try:
            output = get_random_line_of_file(animos_txt)
            if user is None:
                await ctx.reply(content=output)
            else:
                await ctx.send(content=user.mention + " " + output)
        except Exception:
            log.error("Error: {}".format(Exception))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addanimo(self, ctx: commands.Context, *animos: str):
        """[ADMIN] Añade animos

        Uso:
            fur addanimo <animo>
            fur addanimo <animo1> <animo2>...

        Ejemplo:
            fur addanimo "guapo" "hermoso"
        """
        try:
            f = open(animos_txt, "a")
            for animo in animos:
                animo = animo.replace('"', "")
                f.write(animo + "\n")
            f.close()
            await ctx.send("animo/s añadido/s")
        except Exception:
            log.error("Error: {}".format(Exception))


def setup(bot: commands.Bot):
    bot.add_cog(roast(bot))
