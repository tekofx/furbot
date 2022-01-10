import nextcord
from nextcord.ext import commands
import random
from utils.bot import Bot


class fun(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def penis(self, ctx: commands.Context, user: nextcord.Member = None):
        """Buena tula

        Genera un pene de tamaño aleatorio.
        Uso:
            fur penis
            fur penis @<usuario>
        """

        num = random.randint(1, 15)
        output = "El pene de {}\n"
        if user is None:
            usuario = ctx.author.display_name
        else:
            usuario = user.display_name

        output += "8"
        for x in range(num):
            output += "="
        output += "D"
        await ctx.send(output.format(usuario))

    @commands.command()
    async def communist(self, ctx: commands.Context, user: nextcord.Member = None):
        """Serás un comunista bolivariano que apoya al Coletas?

        Uso:
            fur communist
            fur communist @<usuario>
        """

        num = random.randint(0, 100)
        output = "{} es {}% comunista"
        if user is None:
            usuario = ctx.author.display_name
        else:
            usuario = user.display_name
        await ctx.send(output.format(usuario, num))

    @commands.command()
    async def capitalist(self, ctx: commands.Context, user: nextcord.Member = None):
        """Serás capitalista y te convertirás en el nuevo lobo de Wall Street?

        Uso:
            fur capitalist
            fur capitalist @<usuario>
        """

        num = random.randint(0, 100)
        output = "{} es {}% capitalista"
        if user is None:
            usuario = ctx.author.display_name
        else:
            usuario = user.display_name
        await ctx.send(output.format(usuario, num))

    @commands.command()
    async def gay(self, ctx: commands.Context, user: nextcord.Member = None):
        """Maricon el ultimo

        Uso:
            fur gay
            fur gay @<usuario>
        """

        num = random.randint(0, 100)
        output = "{} es {}% gay"
        if user is None:
            usuario = ctx.author.display_name
        else:
            usuario = user.display_name

        await ctx.send(output.format(usuario, num))

    @commands.command(name="str8")
    async def straight(self, ctx: commands.Context, user: nextcord.Member = None):
        """Super str8 el ultimo

        Uso:
            fur str8
            fur str8 @<usuario>

        """

        num = random.randint(0, 100)
        output = "{} es {}% straight"
        if user is None:
            usuario = ctx.author.display_name
        else:
            usuario = user.display_name

        await ctx.send(output.format(usuario, num))


def setup(bot: commands.Bot):
    bot.add_cog(fun(bot))
