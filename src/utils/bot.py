import datetime
import nextcord
from nextcord.errors import Forbidden
from nextcord.ext import commands
import nextcord.ext.application_checks
import os

from utils.database import (
    check_entry_in_database,
    check_record_in_database,
    create_record,
    create_user,
    exists_channel_of_type,
    get_channel_of_type,
    setup_database,
)
from utils.reddit import Reddit
from utils.twitter import Twitter
import requests
from utils.data import Data, get_activity, get_config
from utils import logger

log = logger.getLogger(__name__)
token = os.getenv("DISCORD_TOKEN")


class Bot(commands.Bot):
    def __init__(self, token):
        intents = nextcord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(
            intents=intents,
        )

        self.token = token
        self._twitter = Twitter()
        self._reddit = Reddit()

    @property
    def twitter(self) -> Twitter:
        return self._twitter

    @property
    def reddit(self) -> Reddit:
        return self._reddit

    async def new_github_release(self):
        "Checks if there is a new release on github and sends a message to the channel"
        r = requests.request(
            "GET", "https://api.github.com/repos/tekofx/furbot/releases"
        )
        r = r.json()
        version = r[0]["tag_name"]
        release_changelog = r[0]["body"]
        url = r[0]["html_url"]
        embed = nextcord.Embed(title="Nueva versión " + version, description=url)
        embed.set_thumbnail(
            url="https://raw.githubusercontent.com/tekofx/furbot/main/assets/furbot_logo.png"
        )

        release_changelog = release_changelog.replace("\r", "")

        release_changelog = release_changelog.split("#")

        embed.description = release_changelog.pop(0)

        for i in release_changelog:
            if i != "":
                i = i.splitlines()
                var = "\n".join(i[1:])
                embed.add_field(name=i[0], value=var, inline=False)
        for guild in self.guilds:
            if not exists_channel_of_type(guild, "noticias"):
                continue

            if not check_record_in_database(guild, r[0]["url"]):
                create_record(guild, "github", r[0]["url"])

                await self.channel_send(guild, "noticias", "a", embed)

    async def on_ready(self):
        """Performs an action when the bot is ready"""

        for guild in self.guilds:
            # Setup folders
            data = Data(guild)
            data.setup_folders()
            data.setup_files()
            del data

            # Setup database
            setup_database(guild)

        # Set activity
        activity = nextcord.Game(get_activity())
        await self.change_presence(activity=activity, status=nextcord.Status.online)

        # Load cogs
        cogs = os.listdir("src/cogs/")

        for c in cogs:
            if c.endswith(".py"):
                self.load_extension("cogs." + c[:-3])
                log.info("Loaded {}".format(c))

        log.info("Syncing application commands")
        await self.sync_application_commands(guild_id=788479325787258961)
        log.info("Application commands synced")

        # Send new version message if there's one
        await self.new_github_release()

        log.info("Furbot fully started as {}".format(self.user))

    async def on_member_join(self, member: nextcord.Member):

        if not member.bot:
            msg_join_user = get_config()["msg_join_user"].format(
                member.guild.name, member.display_name
            )
            msg_dm = get_config()["msg_dm"].format(member.guild.name, member.name)
            await self.channel_send(member.guild, "lobby", msg_join_user)
            try:
                await member.send(msg_dm)
            except:
                await self.channel_send(
                    member.guild,
                    "lobby",
                    get_config()["msg_dm"].format(member.guild.name, member.mention),
                )

        else:
            mensaje_lobby_bot = get_config()["msg_join_bot"].format(member.mention)

            await self.channel_send(member.guild, "lobby", mensaje_lobby_bot)

        entry_in_database = check_entry_in_database(member.guild, "users", member.id)
        if not entry_in_database and not member.bot:
            # Add to database
            try:
                joined_date = datetime.datetime.strftime(member.joined_at, "%Y-%m-%d")
                create_user(member.guild, [member.id, member.name, joined_date])
            except Exception as error:
                log.error(
                    "Error creating user on join: {}".format(error),
                    extra={"guild": member.guild.id},
                )
            else:
                log.info(
                    "Created user {} with id {}".format(member.name, member.id),
                    extra={"guild": member.guild.id},
                )

    async def on_member_remove(self, member: nextcord.Member):
        # When a user leaves a server

        if not member.bot:
            msg_leave_user = get_config()["msg_leave_user"].format(
                member.mention, member.name
            )
            await self.channel_send(member.guild, "lobby", msg_leave_user)
        else:
            msg_leave_bot = get_config()["msg_leave_bot"].format(
                member.mention, member.name
            )
            await self.channel_send(member.guild, "lobby", msg_leave_bot)

    def run(self):

        super().run(token=self.token)

    async def on_message(self, message: nextcord.Message):
        """Action performed for every message in channels/DM's
        Args:
            message ([nextcord.Message]): Message to check
        """
        if not message.author.bot:

            if message.content.lower() == "owo":
                await message.channel.send("OwO!")
            if "vaca " in message.content.lower():
                await message.channel.send("Muuu!")
            if "vacas " in message.content.lower():
                await message.channel.send("Muuu Muuu!")
            if message.content.lower() == "uwu":
                await message.channel.send("UwU!")
            if message.content.lower() == "7w7":
                await message.channel.send(":eyes:")
            if message.content.lower() == "ewe":
                await message.channel.send("EwE!")
            if message.content.lower() == "awa":
                await message.channel.send("AwA!")

        await self.process_commands(message)

    async def on_command(self, ctx):

        user = str(ctx.author)
        command = str(ctx.command)
        log.info(user + " used command " + command, extra={"guild": ctx.guild.id})

    async def format_options(self, options: dict):
        var = ""
        for x in options:
            print(x)
            if x["type"] == 6:
                user = await self.fetch_user(x["value"])
                user = user.display_name
                var += x["name"] + ":" + str(user) + " "
            else:
                var += x["name"] + ":" + str(x["value"]) + " "
        return var

    async def on_application_command_completion(
        self, interaction: nextcord.Interaction
    ):
        """When an slash command completes

        Args:
            interaction (nextcord.Interaction): slash command interaction
        """

        # FIXME: This does not work
        options = ""
        if "options" in interaction.data.keys():
            opt = interaction.data["options"]
            print(interaction.application_command.options)
            for x in interaction.application_command.options:
                print(x)
            print(opt)
            print()
            if "options" in opt:
                print(opt)
                opt = opt["options"]
                print(opt)

            options = await self.format_options(opt)
        log.info(
            "{} ({}) in #{} used /{} {}".format(
                interaction.user.display_name,
                interaction.user,
                interaction.channel.name,
                interaction.application_command.name,
                options,
            ),
            extra={"guild": interaction.guild_id},
        )

    async def on_application_command_error(
        self, interaction: nextcord.Interaction, error: Exception
    ):
        """Error in slash command

        Args:
            interaction (nextcord.Interaction): slash command interaction
            error (Exception): error of slash command
        """
        options = ""
        if "options" in interaction.data:
            options = await self.format_options(interaction.data["options"])
        log.error(
            "{} ({}) in #{} used /{} {}".format(
                interaction.user.display_name,
                interaction.user,
                interaction.channel.name,
                interaction.application_command.name,
                options,
            ),
            extra={"guild": interaction.guild_id},
        )

        await interaction.channel.send(
            "Error: comprueba si has usado el comando correctamente. Es posible que se trate de un error interno"
        )

    async def channel_send(
        self,
        guild: nextcord.Guild,
        channel_type: str,
        msg: str,
        embed: nextcord.Embed = None,
    ):
        """Send message to a determinated channel

        Args:
            guild (nextcord.Guild): guild to send the message
            channel_type (str): determinated channel to send the message
            msg (str): message to send
            embed (nextcord.Embed, optional): Embed to send. Defaults to None.

        Raises:
            Forbidden: If the bot doesn't have permissions to send the message
        """

        # Get general_channel id
        general_id = get_channel_of_type(guild, channel_type)

        if general_id != 0:
            try:
                # Fetch general_channel
                general_channel = await self.fetch_channel(general_id)
            except Forbidden as error:
                log.error(
                    "Error getting {} channel from server {}: {}".format(
                        channel_type, guild, error
                    ),
                    extra={"guild": general_channel.id},
                )
                raise Forbidden

            # Send message
            if embed:
                await general_channel.send(embed=embed)
            else:
                await general_channel.send(msg)

    async def on_command_error(
        self, context: commands.Context, error: commands.CommandError
    ) -> None:
        """Checks error on commands
        Args:
            context (commands.Context): Where the command was used
            error (commands.CommandError): Error of the command
        """
        await context.send(
            "Ya no soporto el uso del comando fur. Para acceder a mis comandos usa la barra diagonal `/`"
        )


def aux(dictionary: dict):
    pass
