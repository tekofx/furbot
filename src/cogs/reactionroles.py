import asyncio
import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
from utils.bot import Bot
import logging

log = logging.getLogger(__name__)


class RoleView(nextcord.ui.View):
    pass

    def __init__(self, aux: str):
        self.value = None
        super().__init__(timeout=None)

    @nextcord.ui.button(label="hola", style=nextcord.ButtonStyle.blurple)
    async def hola(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        aux = nextcord.ui.View(timeout=None)
        await interaction.response.send_message("hola que ase", ephemeral=True)
        """ self.value = False
        self.stop() """
        pass


class ReactionRoles(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        # Run when cog is loaded
        self.bot.add_view(RoleView())

    def create_view(self, roles: list, emojis: list, ctx: commands.Context) -> View:
        """Creates a view

        Args:
            roles (list): containing id of roles
            emojis (list): containing emojis
            ctx (commands.Context): context of the command

        Returns:
            View: Reaction Role view
        """
        view = View(timeout=None)
        for role, emoji in zip(roles, emojis):
            role = ctx.guild.get_role(role)
            button = Button(
                label=role.name, style=nextcord.ButtonStyle.primary, emoji=emoji
            )
            button.callback = self.callback
            view.add_item(button)

        return view

    async def callback(self, interaction: nextcord.Interaction):
        print("hola")

    @commands.command(name="reactionrole")
    async def create_reaction_role(self, ctx: commands.Context):
        def check_response(m: nextcord.Message):
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
            log.error("a")
            raise commands.CommandError
        else:
            roles = []
            emojis = []
            for x in str(msg.content).split():
                if "<@" in x:  # role
                    x = x.replace("<", "")
                    x = x.replace("@", "")
                    x = x.replace(">", "")
                    x = x.replace("&", "")

                    roles.append(int(x))

                else:  # emoji
                    emojis.append(x)

            view = self.create_view(roles, emojis, ctx)
            await ctx.send("Elige los roles que quieras", view=view)

        """ await view.wait()
        if view.value is None:
            return
        elif view.value:
            await ctx.send("Pulsaste")
        else:
            await ctx.send("ksajdfñkjsdflkj") """


def setup(bot: commands.Bot):
    bot.add_cog(ReactionRoles(bot))
