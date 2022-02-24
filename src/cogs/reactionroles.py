import asyncio
import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
from utils.bot import Bot
import logging

log = logging.getLogger(__name__)


class ReactionRoles(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    def create_view(self, roles: list, emojis: list, ctx: commands.Context) -> View:
        """Creates a view

        Args:
            roles (list): containing id of roles
            emojis (list): containing emojis
            ctx (commands.Context): context of the command

        Returns:
            View: Reaction Role view
        """
        try:
            view = View(timeout=None)
            for role, emoji in zip(roles, emojis):
                role = ctx.guild.get_role(role)
                button = Button(
                    label=role.name,
                    style=nextcord.ButtonStyle.primary,
                    emoji=emoji,
                    custom_id=str(role.id),
                )
                button.callback = self.callback
                view.add_item(button)
        except commands.CommandError as error:
            log.error("Command: {}".format(error))
        else:
            return view

    async def callback(self, interaction: nextcord.Interaction):
        """Response when a button is pressed

        Args:
            interaction (nextcord.Interaction): button interaction

        Raises:
            error: Forbidden Exception, may be caused because bot's role is bellow the role
                    that wants to be assigned
        """
        try:
            role = interaction.guild.get_role(int(interaction.data["custom_id"]))
            if role in interaction.user.roles:
                message = "Se ha eliminado el rol {}".format(role.name)
                await interaction.user.remove_roles(role)
            else:
                message = "Se ha añadido el rol {}".format(role.name)
                await interaction.user.add_roles(role)

            await interaction.response.send_message(message)
        except nextcord.errors.Forbidden as error:
            message = "Error al asignar rol {}. Comprueba que mi rol está por encima del rol que se quiere asignar".format(
                role.name
            )
            await self.bot.channel_send(interaction.guild, "audit", message)
            raise error

    @commands.command(name="reactionrole")
    async def create_reaction_role(self, ctx: commands.Context, texto: str):
        """Crea un reaction role"""

        def check_response(m: nextcord.Message) -> bool:
            """Checks if a response to the command is sent

            Args:
                m (nextcord.Message): message to wait

            Returns:
                bool: True if the message is a response (in the same channel and by the same author
                that invoked the command)
            """
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        await ctx.send(
            "Crear reaction role, elige los roles añadiendo después de cada uno el emoji que quieres que los represente"
        )

        try:
            msg = await self.bot.wait_for(
                event="message", check=check_response, timeout=60.0
            )
        except asyncio.TimeoutError:
            await ctx.send("Se acabó el tiempo de espera")
            return
        except commands.CommandError:
            raise commands.CommandError
        else:

            roles, emojis = self.get_roles_and_emojis_from_msg(msg)

            view = self.create_view(roles, emojis, ctx)
            await ctx.send(texto, view=view)

    def get_roles_and_emojis_from_msg(self, message: nextcord.Message) -> list:
        """Extracts roles and emojis from a message

        Args:
            message (nextcord.Message): message to extract from

        Returns:
            list: containing 2 list [roles, emojis]
        """
        if "<" and ">" and "@" and "&" not in str(message.content):
            log.error(
                "Error: not correct format in reaction roles message: {}".format(
                    message.content
                )
            )
            raise commands.errors.UserInputError
        roles = []
        emojis = []
        for x in str(message.content).split():
            if "<@" in x:  # role
                x = x.replace("<", "")
                x = x.replace("@", "")
                x = x.replace(">", "")
                x = x.replace("&", "")
                roles.append(int(x))

            else:  # emoji
                emojis.append(x)
        return [roles, emojis]


def setup(bot: Bot):
    bot.add_cog(ReactionRoles(bot))
