from ast import List
import json
import os
from nextcord.ext import commands
from utils.bot import Bot
import nextcord

from utils.data import get_server_path
from utils.database import get_channel

JSON_CONTENT = {"number": 0, "last_user": None, "record": 0}
NUMBERS_JSON = "numbers.json"
CORRECT_EMOJI = "✅"
INCORRECT_EMOJI = "❌"


class numbers(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.generate_numbers_file(self.bot.guilds)

    def generate_numbers_file(self, guilds: list) -> None:
        for guild in guilds:
            server_path = get_server_path(guild)
            if not os.path.isfile(server_path + NUMBERS_JSON):
                # Create file
                with open(server_path + NUMBERS_JSON, "w+") as f:
                    json_object = json.dumps(JSON_CONTENT)
                    f.write(json_object)

    def get_number(self, guild: nextcord.Guild) -> int:
        server_path = get_server_path(guild)
        with open(server_path + NUMBERS_JSON, "r") as f:
            json_object = json.load(f)
            letters = json_object["number"]

        return letters

    def get_last_user(self, guild: nextcord.Guild) -> int:
        server_path = get_server_path(guild)
        with open(server_path + NUMBERS_JSON, "r") as f:
            json_object = json.load(f)
            letters = json_object["last_user"]

        return letters

    def get_record(self, guild: nextcord.Guild) -> int:
        server_path = get_server_path(guild)
        with open(server_path + NUMBERS_JSON, "r") as f:
            json_object = json.load(f)
            letters = json_object["record"]

        return letters

    def update_json(self, guild: nextcord.Guild, number: int, last_user: int) -> None:
        server_path = get_server_path(guild)

        with open(server_path + NUMBERS_JSON, "r+") as f:

            json_object = json.load(f)
            json_object["number"] = number
            json_object["last_user"] = last_user
            if json_object["record"] < number:
                json_object["record"] = number

            f.seek(0)
            json.dump(json_object, f)
            f.truncate()

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if get_channel(message.guild, "numbers") != message.channel.id:
            return
        content = message.content
        number = self.get_number(message.guild)
        last_user = self.get_last_user(message.guild)
        record = self.get_record(message.guild)
        if message.author != self.bot.user and content.isnumeric():
            if last_user == message.author.id:
                await message.add_reaction(INCORRECT_EMOJI)
                await message.channel.send(
                    "{} arruinó la cuenta en {}".format(message.author.mention, number)
                )
                await message.channel.send("Record hasta ahora `{}`".format(record))
                self.update_json(message.guild, 0, None)
            elif int(content) != number + 1:
                await message.add_reaction(INCORRECT_EMOJI)
                await message.channel.send(
                    "{} no es el número correcto".format(message.author.mention)
                )
                await message.channel.send("Record hasta ahora `{}`".format(record))
                self.update_json(message.guild, 0, None)

            else:
                await message.add_reaction(CORRECT_EMOJI)
                self.update_json(message.guild, int(content), message.author.id)


def setup(bot: commands.Bot):
    bot.add_cog(numbers(bot))
