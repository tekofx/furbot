from lightbulb import slash_commands, Option
import lightbulb
import random
import hikari
import typing
import sys
import inspect


class Penis(slash_commands.SlashCommand):
    description = "Como la tienes de larga?"
    enabled_guilds: typing.Iterable[int] = [788479325787258961]

    # Options
    user: hikari.User = Option("Usuario")

    async def callback(self, context: slash_commands.SlashCommandContext):

        num = random.randint(1, 15)
        context.options.user

        usuario = await self.bot.rest.fetch_member(
            context.guild_id, int(context.options.user)
        )

        output = "El pene de {}\n".format(usuario.mention)
        output += "8"
        for x in range(num):
            output += "="
        output += "D"
        await context.respond(output)


class Communism(slash_commands.SlashCommand):
    description = "Eres comunista?"
    enabled_guilds: typing.Iterable[int] = [788479325787258961]

    # Options
    user: hikari.User = Option("Usuario")

    async def callback(self, context: slash_commands.SlashCommandContext):

        num = random.randint(1, 15)
        context.options.user

        usuario = await self.bot.rest.fetch_member(
            context.guild_id, int(context.options.user)
        )

        output = "{} es {}% comunista".format(usuario.mention, num)

        await context.respond(output)


class Capitalist(slash_commands.SlashCommand):
    description = "Eres comunista?"
    enabled_guilds: typing.Iterable[int] = [788479325787258961]

    # Options
    user: hikari.User = Option("Usuario")

    async def callback(self, context: slash_commands.SlashCommandContext):

        num = random.randint(1, 15)
        context.options.user

        usuario = await self.bot.rest.fetch_member(
            context.guild_id, int(context.options.user)
        )

        output = "{} es {}% capitalista".format(usuario.mention, num)

        await context.respond(output)


class Gay(slash_commands.SlashCommand):
    description = "Eres gay?"
    enabled_guilds: typing.Iterable[int] = [788479325787258961]

    # Options
    user: hikari.User = Option("Usuario")

    async def callback(self, context: slash_commands.SlashCommandContext):

        num = random.randint(1, 15)
        context.options.user

        usuario = await self.bot.rest.fetch_member(
            context.guild_id, int(context.options.user)
        )

        output = "{} es {}% gay".format(usuario.mention, num)

        await context.respond(output)


class Str8(slash_commands.SlashCommand):
    description = "Eres hetero?"
    enabled_guilds: typing.Iterable[int] = [788479325787258961]

    # Options
    user: hikari.User = Option("Usuario")

    async def callback(self, context: slash_commands.SlashCommandContext):

        num = random.randint(1, 15)
        context.options.user

        usuario = await self.bot.rest.fetch_member(
            context.guild_id, int(context.options.user)
        )

        output = "{} es {}% hetero".format(usuario.mention, num)

        await context.respond(output)


def load(bot: lightbulb.Bot):
    for _, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(obj, slash_commands.SlashCommand):
            bot.add_slash_command(obj)


def unload(bot: lightbulb.Bot):
    for _, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(obj, slash_commands.SlashCommand):
            bot.remove_slash_command(obj)
