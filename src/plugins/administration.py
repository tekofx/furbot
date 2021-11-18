import logging
import hikari
import lightbulb
from hikari import permissions
from utils.functions import yaml_f
from asyncio import sleep
from utils.database import (
    create_color,
    set_birthday,
    check_entry_in_database,
    create_connection,
    create_rank,
    create_specie,
    create_user,
)

log = logging.getLogger(__name__)


class Administration(lightbulb.Plugin):
    def __init__(self, bot: lightbulb.Bot):
        super().__init__(name="Administration")
        self.bot = bot

    @lightbulb.command(name="activity")
    async def change_activity(self, ctx: lightbulb.Context, activity_name: str):
        """[Admin] Cambiar actividad del bot"""
        await self.bot.rest.trigger_typing(ctx.get_channel())

        yaml_f.change_activity(activity_name)
        activity = hikari.Activity(name=activity_name)

        try:
            await self.bot.update_presence(activity=activity)

        except Exception:
            await ctx.respond("Error: Contacte con un administrador")
            log.error("Error: ".format(Exception))

        await ctx.respond("Cambiada actividad a " + activity_name)
        log.info("Changed activity to " + activity_name)

    @lightbulb.check(
        lightbulb.has_guild_permissions(permissions.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command(name="addspecie")
    async def add_species(self, ctx: lightbulb.Context, specie: hikari.Role):
        """[Admin] Añade una especie al bot

        Uso:
            fur addspecie <rol>
        """
        await self.bot.rest.trigger_typing(ctx.get_channel())
        server = str(ctx.guild_id)
        con = create_connection(server)
        specie_data = [specie.id, specie.name]
        create_specie(con, specie_data)
        await ctx.respond("Especie {} añadida".format(specie.mention))
        log.info("Added specie " + specie.name)

    @lightbulb.check(
        lightbulb.has_guild_permissions(permissions.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command(name="addrank")
    async def add_rank(self, ctx: lightbulb.Context, rank: hikari.Role):
        """[Admin] Añade una especie al bot

        Uso:
            fur addspecie <rol>
        """
        await self.bot.rest.trigger_typing(ctx.get_channel())
        server = str(ctx.guild_id)
        con = create_connection(server)
        specie_data = [rank.id, rank.name]
        create_rank(con, specie_data)
        await ctx.respond("Especie {} añadida".format(rank.mention))
        log.info("Added specie " + rank.name)

    @lightbulb.check(
        lightbulb.has_guild_permissions(permissions.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command(name="addcolor")
    async def add_color(self, ctx: lightbulb.Context, color: hikari.Role):
        """[Admin] Añade una especie al bot

        Uso:
            fur addspecie <rol>
        """
        await self.bot.rest.trigger_typing(ctx.get_channel())
        server = str(ctx.guild_id)
        con = create_connection(server)
        specie_data = [color.id, color.name]
        create_color(con, specie_data)
        await ctx.respond("Color {} añadido".format(color.mention))
        log.info("Added color " + color.name)

    @lightbulb.check(
        lightbulb.has_guild_permissions(permissions.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command(name="upuser")
    async def update_users(self, ctx: lightbulb.Context):
        """[Admin] Actualiza la lista de usuarios con los usuarios que no existen\n"""
        await self.bot.rest.trigger_typing(ctx.get_channel())
        users = await self.bot.rest.fetch_members(ctx.get_guild())
        server = str(ctx.guild_id)
        con = create_connection(server)
        for user in users:
            if not user.is_bot and not check_entry_in_database(con, "users", user.id):

                user_data = [user.id, user.username, user.joined_at, 1]
                create_user(con, user_data)

        await ctx.respond("Actualizada lista de usuarios")
        log.info("Updated users in database")

    @lightbulb.check(
        lightbulb.has_guild_permissions(permissions.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command()
    async def addcumple(
        self, ctx: lightbulb.Context, birthday: str, user: hikari.Member
    ):
        """[Admin] Añade el cumpleaños de alguien al bot

        Uso:
            fur addcumple <dia>-<mes> @<usuario>

        Ejemplo:
            fur addcumple 16-1 @Teko
        """
        await self.bot.rest.trigger_typing(ctx.get_channel())
        con = create_connection(str(ctx.guild_id))
        set_birthday(con, user.id, birthday)
        await ctx.respond("Añadido cumpleaños de " + user.username)

    @lightbulb.check(
        lightbulb.has_guild_permissions(permissions.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command()
    async def clear(self, ctx: lightbulb.Context, num: int):
        """[Admin] Elimina mensajes de un canal"""
        await self.bot.rest.trigger_typing(ctx.get_channel())
        await ctx.message.delete()
        messages = ctx.get_channel().fetch_history()
        count = 0
        async for i, message in messages.enumerate():
            if count == num:
                break
            await message.delete()
            count += 1
        message = await ctx.respond("Eliminados {} mensajes".format(num))
        await sleep(5)
        await message.delete()

    @lightbulb.check(
        lightbulb.has_guild_permissions(permissions.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command()
    async def ban(
        self, ctx: lightbulb.Context, *users: hikari.Member, motivo: str = None
    ):
        """[Admin] Banea a un usuario\n\n

        Uso:\n
            fur ban <user_1> <user_2>... <user_n> <motivo>

        """
        await self.bot.rest.trigger_typing(ctx.get_channel())
        for user in users:

            if motivo is None:
                await user.ban()
                output = "{} baneado".format(user.mention)
            else:
                await user.ban(reason=motivo)
                output = "{} baneado con motivo: {}".format(user.mention, motivo)

            await ctx.respond(output)

    @lightbulb.check(
        lightbulb.has_guild_permissions(permissions.Permissions.ADMINISTRATOR)
    )
    @lightbulb.command()
    async def kick(
        self, ctx: lightbulb.Context, *users: hikari.Member, motivo: str = None
    ):
        """[Admin] Kickea a un usuario\n\n

        Uso:\n
            fur kick <user_1> <user_2>... <user_n> <motivo>
        """
        await self.bot.rest.trigger_typing(ctx.get_channel())
        for user in users:
            if motivo is None:
                await user.kick()
                output = "{} kickeado".format(user.mention)
            else:
                await user.kick(reason=motivo)
                output = "{} kickeado con motivo: {}".format(user.mention, motivo)

            await ctx.respond(output)


def load(bot: lightbulb.Bot):
    bot.add_plugin(Administration(bot))


def unload(bot: lightbulb.Bot):
    bot.remove_plugin("Administration")
