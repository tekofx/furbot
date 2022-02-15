import nextcord
from nextcord.ext import commands
from pyrae import dle

from utils.database import (
    create_connection,
    get_birthday,
    get_colors,
    get_ranks,
    get_species,
)
from utils.bot import Bot


class utilities(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def ping(self, context):
        await context.channel.send("Pim pam trucu trucu")

    @commands.command()
    async def rae(self, ctx: commands.Context, palabra: str):
        """Obtiene una definición de la RAE

        Uso:
            fur rae <palabra>
        """

        tmp = await ctx.send("Buscando en la RAE")

        output = str(dle.search_by_word(palabra))

        if "«Diccionario de la lengua española»" in output:
            await tmp.edit(content="Termino no encontrado")
        else:
            await tmp.edit(content=output)

    @commands.command()
    async def cumple(self, ctx: commands.Context, user: nextcord.Member):
        """Obtiene el cumpleaños de un usuario

        Uso:
            fur cumple @<usuario>
        """
        con = create_connection(str(ctx.guild.id))

        output = "No existe el cumpleaños de " + user.display_name
        birthday = get_birthday(con, user.id).split("-")
        day = birthday[2]
        month = birthday[1]
        birthday = str(day) + "-" + str(month)

        output = "El cumpleaños de {user} es el {cumple}".format(
            user=user.display_name, cumple=birthday
        )
        await ctx.send(output)


def setup(bot: commands.Bot):
    bot.add_cog(utilities(bot))


def get_user_species(user: nextcord.Member):
    """Get user roles that are species

    Args:
        user (nextcord.Member): user to search for roles

    Returns:
        str: String containing roles
    """
    con = create_connection(user.guild.id)
    server_species = get_species(con)
    mention = []
    roles = user.roles
    for role in roles:
        if role.id in server_species:
            mention.append(role.name)

    b = ", ".join(mention)
    return b


def get_user_roles(user: nextcord.Member):
    """Get user roles that are not ranks

    Args:
        user (nextcord.Member): user to search for roles

    Returns:
        str: String containing roles
    """
    con = create_connection(user.guild.id)

    server_ranks = get_ranks(con)
    mention = []
    roles = user.roles

    for role in roles:
        if role.id in server_ranks:
            mention.append(role.name)

    b = ", ".join(mention)
    return str(b)


def get_user_ranks(user: nextcord.Member):
    """Get ranks from a user

    Args:
        user (nextcord.User): user to search for roles

    Returns:
        str: String containing all ranks
    """
    con = create_connection(user.guild.id)
    server_ranks = get_ranks(con)
    output = []
    roles = user.roles

    for role in roles:
        if role.id in server_ranks:
            output.append(role.name)
    if output:
        b = ", ".join(output)
    else:
        return "Admin"
    return str(b)


def get_user_color_code(user: nextcord.Member):
    """Get user roles that are not ranks

    Args:
        user (nextcord.User): user to search for roles

    Returns:
        str: String containing roles
    """
    con = create_connection(user.guild_id)

    server_colors = get_colors(con)
    roles = user.roles

    for role in roles:
        if role.id in server_colors:
            return role.colour.value
