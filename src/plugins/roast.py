from hikari import permissions
import lightbulb
from time import sleep
import hikari
import random

from functions import magnet_id
from functions import get_random_line_of_file, insults_txt, animos_txt


class Roast(lightbulb.Plugin):
    def __init__(self, bot: lightbulb.Bot):
        super().__init__(name="Roast")
        self.bot = bot

    @lightbulb.command()
    async def garich(self, context: lightbulb.Context):
        """Gala rich"""
        output = "Gala rich porque compra Axe, tiene 5 Alexas, tiene una limpiadora que le regala cosas y tiene una tele 4k"
        await context.respond(output)

    @lightbulb.command()
    async def tecute(self, context: lightbulb.Context):
        """Teko cute"""
        if context.author.id is magnet_id:
            await context.respond("Teko cute")
        else:
            await context.respond("Teko NO cute")

    @lightbulb.command()
    async def teodio(self, context: lightbulb.Context, user: hikari.User = None):
        """Muestra tu odio al bot"""
        if user is None:
            usuario = context.author.mention
        else:
            usuario = user.mention
        output = "{} %s " % ("Yo te odio mas pedazo de basura")
        await context.respond(content=output.format(usuario), reply=True)

    @lightbulb.command()
    async def insult(self, context: lightbulb.Context, user: hikari.User = None):
        """Insulta gente 7w7

        Genera un insulto aleatorio
        """
        if user is None:
            usuario = context.author.mention
        else:
            usuario = user.mention

        try:
            output = usuario + get_random_line_of_file(insults_txt)
            await context.respond(content=output, reply=True)
        except FileNotFoundError:
            # logging.error("Error at getting insults.txt")
            pass

    @lightbulb.check(
        lightbulb.has_guild_permissions(permissions.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command()
    async def addinsult(self, context, *insults: str):
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
            await context.respond("Insulto/s añadido/s")
        except FileNotFoundError:
            print("Error at getting insults.txt")
            # logging.error("Error at getting insults.txt")

    @lightbulb.command()
    async def animo(self, context, user: hikari.User = None):
        """Anima a la gente"""
        if user is None:
            usuario = context.author.mention
        else:
            usuario = user.mention

        try:
            output = usuario + get_random_line_of_file(animos_txt)
            await context.respond(content=output, reply=True)
        except FileNotFoundError:
            print("Error at getting animos.txt")
            # logging.error("Error at getting animos.txt")

    @lightbulb.check(
        lightbulb.has_guild_permissions(permissions.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command()
    async def addanimo(self, context, *animos: str):
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
            await context.channel.send("animo/s añadido/s")
        except FileNotFoundError:
            print("Error at getting animos.txt")
            # logging.error("Error at getting animos.txt")


def load(bot):
    bot.add_plugin(Roast(bot))
