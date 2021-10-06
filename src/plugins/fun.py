import lightbulb
from time import sleep
import hikari
import random


class Fun(lightbulb.Plugin):
    def __init__(self, bot: lightbulb.Bot):
        super().__init__(name="Fun")
        self.bot = bot

    @lightbulb.command()
    async def penis(self, context: lightbulb.Context, user: hikari.User = None):
        """Buena tula

        Genera un pene de tamaño aleatorio.
        Uso:
        fur penis            --> Tu tula
        fur penis @<usuario> --> La tula de @<usuario>
        """

        num = random.randint(1, 15)
        output = "El pene de {}\n"
        if user is None:
            usuario = context.author.username
        else:
            usuario = user.username

        output += "8"
        for x in range(num):
            output += "="
        output += "D"
        await context.respond(output.format(usuario))

    @lightbulb.command()
    async def communism(self, context: lightbulb.Context, user: hikari.User = None):
        """Serás un comunista bolivariano que apoya al Coletas?"""

        num = random.randint(0, 100)
        output = "{} es {}% comunista"
        if user is None:
            usuario = context.author.username
        else:
            usuario = user.username
        await context.respond(output.format(usuario, num))

    @lightbulb.command()
    async def gay(self, context: lightbulb.Context, user: hikari.User = None):
        """Maricon el ultimo"""

        num = random.randint(0, 100)
        output = "{} es {}% gay"
        if user is None:
            usuario = context.author.username
        else:
            usuario = user.username

        await context.respond(output.format(usuario, num))

    @lightbulb.command()
    async def str8(self, context: lightbulb.Context, user: hikari.User = None):
        """Super str8 el ultimo"""

        num = random.randint(0, 100)
        output = "{} es {}% hetero"
        if user is None:
            usuario = context.author.username
        else:
            usuario = user.username

        await context.respond(output.format(usuario, num))

    @lightbulb.command()
    async def capitalist(self, context: lightbulb.Context, user: hikari.User = None):
        """Serás capitalista y te convertirás en el nuevo lobo de Wall Street?"""

        num = random.randint(0, 100)
        output = "{} es {}% capitalista"
        if user is None:
            usuario = context.author.username
        else:
            usuario = user.username
        await context.respond(output.format(usuario, num))


def load(bot):
    bot.add_plugin(Fun(bot))


def unload(bot: lightbulb.Bot):
    bot.remove_plugin("Fun")
