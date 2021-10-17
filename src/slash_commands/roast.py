from lightbulb import slash_commands, Option
import typing
import hikari
from utils.functions import (
    get_random_line_of_file,
    insults_txt,
    animos_txt,
    magnet_id,
    write_in_file,
)
import lightbulb
import sys
import inspect


class Garich(slash_commands.SlashCommand):
    description = "Gala rich"
    enabled_guilds: typing.Iterable[int] = [788479325787258961]

    async def callback(self, context: slash_commands.SlashCommandContext):
        output = "Gala rich porque compra Axe, tiene 5 Alexas, tiene una limpiadora que le regala cosas y tiene una tele 4k"

        await context.respond(output)


class Teko_cute(slash_commands.SlashCommand):
    description = "Teko cute"
    enabled_guilds: typing.Iterable[int] = [788479325787258961]

    async def callback(self, context: slash_commands.SlashCommandContext):
        if context.author.id is magnet_id:
            output = "Teko cute"
        else:
            output = "Teko NO cute"
        await context.respond(output)


class Furbot_te_odio(slash_commands.SlashCommand):
    description = "Muestra tu odio al bot"
    enabled_guilds: typing.Iterable[int] = [788479325787258961]

    async def callback(self, context: slash_commands.SlashCommandContext):
        output = "Yo te odio mas pedazo de basura"
        await context.respond(output)


class Insult(slash_commands.SlashCommand):
    description = "Insulta gente 7w7"
    enabled_guilds: typing.Iterable[int] = [788479325787258961]

    # Options
    user: hikari.User = Option("Usuario")

    async def callback(self, context: slash_commands.SlashCommandContext):

        user = await self.bot.rest.fetch_member(
            context.guild_id, int(context.options.user)
        )

        output = user.mention + " " + get_random_line_of_file(insults_txt)

        await context.respond(output)


class Animo(slash_commands.SlashCommand):
    description = "Anima a la gente"
    enabled_guilds: typing.Iterable[int] = [788479325787258961]

    # Options
    user: hikari.User = Option("Usuario")

    async def callback(self, context: slash_commands.SlashCommandContext):

        user = await self.bot.rest.fetch_member(
            context.guild_id, int(context.options.user)
        )

        output = user.mention + " " + get_random_line_of_file(animos_txt)

        await context.respond(output)


class Añadir_insulto(slash_commands.SlashCommand):
    description = "Añade un insulto"
    enabled_guilds: typing.Iterable[int] = [788479325787258961]

    # Options
    insult: str = Option("Insulto")

    async def callback(self, context: slash_commands.SlashCommandContext):

        insult = context.options.insult
        write_in_file(insults_txt, insult + "\n")

        await context.respond("Insulto {} añadido".format(insult))


class Añadir_animo(slash_commands.SlashCommand):
    description = "Añade un animo"
    enabled_guilds: typing.Iterable[int] = [788479325787258961]

    # Options
    animo: str = Option("animo")

    async def callback(self, context: slash_commands.SlashCommandContext):

        animo = context.options.animo
        write_in_file(animos_txt, animo + "\n")

        await context.respond("Animo {} añadido".format(animo))


def load(bot: lightbulb.Bot):
    for _, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(obj, slash_commands.SlashCommand):
            bot.add_slash_command(obj)


def unload(bot: lightbulb.Bot):
    for _, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(obj, slash_commands.SlashCommand):
            bot.remove_slash_command(obj)
