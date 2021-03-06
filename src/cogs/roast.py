import nextcord
from nextcord.ext import commands
from utils.bot import Bot
from utils.database import create_sentence, get_random_sentence
from utils import logger

log = logger.getLogger(__name__)


class roast(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def teodio(self, ctx: commands.Context, user: nextcord.Member = None):
        """Muestra tu odio al bot"""
        await ctx.reply(content="Yo te odio mas pedazo de basura")

    @commands.command()
    async def insult(self, ctx: commands.Context, user: nextcord.Member = None):
        """Insulta gente 7w7"""

        try:
            output = get_random_sentence(ctx.guild, "insult")
            if user is None:
                await ctx.reply(content=output)
            else:
                await ctx.send(content=user.mention + " " + output)
        except Exception:
            log.error("Error: {}".format(Exception),extra={"guild": ctx.guild.id})

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
        for insult in insults:
            try:
                create_sentence(ctx.guild, ["insult", insult])
            except Exception as error:
                log.error("Error adding insult: {}".format(error),extra={"guild": ctx.guild.id})
                await ctx.reply(
                    "Error añadiendo insulto {}: insulto ya existente".format(insult)
                )
            else:
                log.info(
                    "Added insult {}".format(insult), extra={"guild": ctx.guild.id}
                )
                await ctx.reply("Insulto añadido")

    @commands.command()
    async def animo(self, ctx: commands.Context, user: nextcord.Member = None):
        """Anima a la gente"""
        try:
            output = get_random_sentence(ctx.guild, "animo")
            if user is None:
                await ctx.reply(content=output)
            else:
                await ctx.send(content=user.mention + " " + output)
        except Exception:
            log.error("Error: {}".format(Exception),extra={"guild": ctx.guild.id})

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

        for animo in animos:
            try:
                create_sentence(ctx.guild, ["animo", animo])
            except Exception as error:
                log.error("Error adding anim: {}".format(error),extra={"guild": ctx.guild.id})
                await ctx.reply(
                    "Error añadiendo animo {}: animo ya existente".format(animo)
                )
            else:
                log.info("Added animo {}".format(animo), extra={"guild": ctx.guild.id})
                await ctx.reply("Animo añadido")


def setup(bot: commands.Bot):
    bot.add_cog(roast(bot))
