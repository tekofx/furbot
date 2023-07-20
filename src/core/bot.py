import asyncio
import nextcord
from nextcord.ext import commands
import nextcord.ext.application_checks
import os
from core.e621_e926 import e621, e926
from core.database import Database
from core.reddit import Reddit
from core.twitter import Twitter
from core.mastodon import Mastodon
import requests
from core.data import Data, get_activity, get_config
from core import logger

log = logger.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self, token):
        intents = nextcord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(
            intents=intents,
            
        )

        self.token = token
        self._db=Database()
        self._db.initialize()
        
        if os.getenv("TWITTER_ACCESS_TOKEN"):
            self._twitter = Twitter(self._db)
        if os.getenv("REDDIT_CLIENT_ID"):
            self._reddit = Reddit(self._db)
        if os.getenv("MASTODON_TOKEN"):
            self._mastodon = Mastodon(self._db)
            
        self._e621 = e621(self._db)
        self._e926 = e926(self._db)
        
            
            

        self._local_guild = int(
            os.getenv("LOCAL_GUILD")
        )  # Guild to fetch commands at startup

        self._tasks = {}

    @property
    def db(self) -> Database:
        return self._db
    
    @property
    def twitter(self) -> Twitter:
        return self._twitter

    @property
    def reddit(self) -> Reddit:
        return self._reddit

    @property
    def mastodon(self) -> Mastodon:
        return self._mastodon
    
    @property
    def e621(self) -> e621:
        return self._e621
    
    @property
    def e926(self) -> e926:
        return self._e926

    @property
    def tasks(self) -> dict[int, asyncio.Task]:
        """Dict of tasks containing the task_id as key and the task as value

        Returns:
            dict[int, asyncio.Task]: Dict of tasks
        """
        return self._tasks


    async def on_ready(self):
        """Performs an action when the bot is ready"""

        for guild in self.guilds:
            # Setup folders
            data = Data(guild)
            data.setup_folders()
            data.setup_files()
            del data

        # Set activity
        activity = nextcord.Game(get_activity())
        await self.change_presence(activity=activity, status=nextcord.Status.online)

        # Load cogs
        cogs = os.listdir("src/cogs/")

        for c in cogs:
            if c.endswith(".py"):
                self.load_extension("cogs." + c[:-3])
                log.info("Loaded {}".format(c))

        try:

            log.info("Syncing application commands")
            #await self.sync_application_commands()
            await self.sync_all_application_commands()
        except nextcord.errors.NotFound as e:
            log.error("Error syncing application commands: {}".format(e))

        

        log.info("Furbot fully started as {}".format(self.user))

    async def on_member_join(self, member: nextcord.Member):

        if member.bot:
            mensaje_lobby_bot = get_config()["msg_join_bot"].format(member.mention)
            await self.channel_send(member.guild, "lobby", mensaje_lobby_bot)
            return

        msg_join_user = get_config()["msg_join_user"].format(
            member.guild.name, member.mention
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

            # TODO: Remove
            """ if "e621" in message.content.lower():
                tags="fox wolf"
                post=self.e621.get_post_not_repeated(message.guild,tags.split(" "))
                await message.channel.send(post.file.url) """

        await self.process_commands(message)

    def format_options(self, interaction: nextcord.Interaction) -> str:
        """Formats slash command options

        Args:
            interaction (nextcord.Interaction): Slash command interaction

        Returns:
            str: string formatted
        """
        output = ""
        if "options" in interaction.data.keys():
            options = interaction.data["options"]

            if "options" in options[0]:
                options = options[0]["options"]

            for x in options:
                output += x.get("name") + ":" + str(x.get("value")) + " "

        return output

    async def on_application_command_completion(
        self, interaction: nextcord.Interaction
    ):
        """When an slash command completes

        Args:
            interaction (nextcord.Interaction): slash command interaction
        """

        options = self.format_options(interaction)
        log.info(
            "{} ({}) in #{} used /{} {}".format(
                interaction.user.display_name,
                interaction.user,
                interaction.channel.name,
                interaction.application_command.name,
                options,
            ),
            extra={"guild": interaction.guild.name},
        )

    async def on_application_command_error(
        self, interaction: nextcord.Interaction, error: Exception
    ):
        """Error in slash command

        Args:
            interaction (nextcord.Interaction): slash command interaction
            error (Exception): error of slash command
        """
        options = self.format_options(interaction)
        log.error(
            "{} ({}) in #{} used /{} {}. {}".format(
                interaction.user.display_name,
                interaction.user,
                interaction.channel.name,
                interaction.application_command.name,
                options,
                error,
            ),
            extra={"guild": interaction.guild.name},
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
        general=self.db.get_channel_of_type(guild, channel_type)
        if general==None:
            return
        print(general)
        general_id = general[0]

        if general_id != 0:
            try:
                # Fetch general_channel
                general_channel = await self.fetch_channel(general_id)
            except Exception as error:
                log.error(
                    "Error getting {} channel from server {}: {}".format(
                        channel_type, guild, error
                    ),
                    extra={"guild": guild.name},
                )
                raise error

            # Send message
            if embed:
                await general_channel.send(embed=embed)
            else:
                await general_channel.send(msg)


def aux(dictionary: dict):
    pass
