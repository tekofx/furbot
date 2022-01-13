import logging
import nextcord
from nextcord.ext import commands
from utils.functions import get_random_line_of_file
from utils.bot import Bot
from utils.data import resources_path
from utils.database import create_connection, create_sentence, get_random_sentence

log = logging.getLogger(__name__)

animos_txt = resources_path + "animos.txt"
insults_txt = resources_path + "insults.txt"


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
            con = create_connection(str(ctx.guild.id))
            output = get_random_sentence(con, "insult")
            if user is None:
                await ctx.reply(content=output)
            else:
                await ctx.send(content=user.mention + " " + output)
        except Exception:
            log.error("Error: {}".format(Exception))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addinsult(self, ctx: commands.Context, *insults: str):
        """[ADMIN] Añade insulto

        Uso:
            fur addinsulto <insulto>
            fur addinsulto <insulto1> <insulto2>...

        Ejemplo:
            fur addinsulto "feo" "horrible"
        """
        try:
            con = create_connection(str(ctx.guild.id))

            for insult in insults:
                create_sentence(con, ["insult", insult])
            await ctx.reply("Insulto/s añadido/s")
        except Exception as error:
            log.error("Error: {}".format(error))

    @commands.command()
    async def animo(self, ctx: commands.Context, user: nextcord.Member = None):
        """Anima a la gente"""
        try:
            con = create_connection(str(ctx.guild.id))
            output = get_random_sentence(con, "animo")
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
            con = create_connection(str(ctx.guild.id))

            for animo in animos:
                create_sentence(con, ["animo", animo])
            await ctx.reply("Animo/s añadido/s")
        except Exception as error:
            log.error("Error: {}".format(error))


def setup(bot: commands.Bot):
    bot.add_cog(roast(bot))
