from hikari import permissions
import lightbulb
import hikari
import logging
from utils.functions import magnet_id
from utils.functions import get_random_line_of_file, insults_txt, animos_txt

log = logging.getLogger(__name__)


class Roast(lightbulb.Plugin):
    def __init__(self):
        super().__init__(name="Roast")

    @lightbulb.command("tecute", "Teko cute")
    async def tecute(self, ctx: lightbulb.context.Context):
        """Teko cute"""
        await self.bot.rest.trigger_typing(ctx.get_channel())
        if ctx.author.id is magnet_id:
            await ctx.respond("Teko cute")
        else:
            await ctx.respond("Teko NO cute")

    @lightbulb.command("teodio", "Muestra tu odio al bot")
    async def teodio(self, ctx: lightbulb.context.Context, user: hikari.User = None):
        """Muestra tu odio al bot"""
        await self.bot.rest.trigger_typing(ctx.get_channel())
        if user is None:
            usuario = ctx.author.mention
        else:
            usuario = user.mention
        output = "{} %s " % ("Yo te odio mas pedazo de basura")
        await ctx.respond(content=output.format(usuario), reply=True)

    @lightbulb.command("insult", "Insulta gente 7w7")
    async def insult(self, ctx: lightbulb.context.Context, user: hikari.User = None):
        """Insulta gente 7w7

        Genera un insulto aleatorio
        """
        await self.bot.rest.trigger_typing(ctx.get_channel())
        if user is None:
            usuario = ctx.author.mention
        else:
            usuario = user.mention

        try:
            output = usuario + " " + get_random_line_of_file(insults_txt)
            await ctx.respond(content=output, reply=True)
        except Exception:
            log.error("Error: {}".format(Exception))

    @lightbulb.add_checks(
        lightbulb.has_role_permissions(hikari.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command("addinsult", "[ADMIN] Añade insulto")
    async def addinsult(self, ctx, *insults: str):
        """[ADMIN] Añade insulto

        Uso:
            fur addinsulto <insulto>
            fur addinsulto <insulto1> <insulto2>...

        Ejemplo:
            fur addinsulto "feo" "horrible"
        """
        await self.bot.rest.trigger_typing(ctx.get_channel())
        try:
            f = open(insults_txt, "a")
            for insult in insults:
                insult = insult.replace('"', "")
                f.write(insult + "\n")
            f.close()
            await ctx.respond("Insulto/s añadido/s")
        except Exception:
            log.error("Error: {}".format(Exception))

    @lightbulb.command("animo", "Anima a la gente")
    async def animo(self, ctx, user: hikari.User = None):
        """Anima a la gente"""
        await self.bot.rest.trigger_typing(ctx.get_channel())
        if user is None:
            usuario = ctx.author.mention
        else:
            usuario = user.mention

        try:
            output = usuario + get_random_line_of_file(animos_txt)
            await ctx.respond(content=output, reply=True)
        except Exception:
            log.error("Error: {}".format(Exception))

    @lightbulb.add_checks(
        lightbulb.has_role_permissions(hikari.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command("addanimo", "[ADMIN] Añade animos")
    async def addanimo(self, ctx, *animos: str):
        """[ADMIN] Añade animos

        Uso:
            fur addanimo <animo>
            fur addanimo <animo1> <animo2>...

        Ejemplo:
            fur addanimo "guapo" "hermoso"
        """
        await self.bot.rest.trigger_typing(ctx.get_channel())
        try:
            f = open(animos_txt, "a")
            for animo in animos:
                animo = animo.replace('"', "")
                f.write(animo + "\n")
            f.close()
            await ctx.channel.send("animo/s añadido/s")
        except Exception:
            log.error("Error: {}".format(Exception))


def load(bot: lightbulb.BotApp):
    bot.add_plugin(Roast())


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin("Roast")
