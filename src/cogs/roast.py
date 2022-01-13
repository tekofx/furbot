import logging
import nextcord
from nextcord.ext import commands
from utils.bot import Bot
from utils.database import create_connection, create_sentence, get_random_sentence

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
        """Insulta gente 7w7"""

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
        con = create_connection(str(ctx.guild.id))

        for insult in insults:
            try:
                create_sentence(con, ["insult", insult])
            except Exception as error:
                log.error("Error adding insult: {}".format(error))
                await ctx.reply(
                    "Error añadiendo insulto {}: insulto ya existente".format(insult)
                )
            else:
                log.info("Added insult {}".format(insult))
                await ctx.reply("Insulto añadido")

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
        con = create_connection(str(ctx.guild.id))

        for animo in animos:
            try:
                create_sentence(con, ["animo", animo])
            except Exception as error:
                log.error("Error adding anim: {}".format(error))
                await ctx.reply(
                    "Error añadiendo animo {}: animo ya existente".format(animo)
                )
            else:
                log.info("Added animo {}".format(animo))
                await ctx.reply("Animo añadido")


def setup(bot: commands.Bot):
    bot.add_cog(roast(bot))
