from http import server
from types import NoneType
from nextcord.ext import commands, tasks
from utils.bot import Bot
from utils.data import get_server_path, resources_path
import random
import logging
from datetime import date, datetime, timedelta, time
import asyncio
import nextcord
from pyrae import dle
import json
import os


log = logging.getLogger(__name__)


GREEN_SQUARE = "🟩"
YELLOW_SQUARE = "🟨"
GREY_SQUARE = "⬜"
WORD_LENGHT = 5
WORDLE_JSON = "wordle.json"


YELLOW_POINTS = 1
GREEN_POINTS = 2
WORD_GUESSED_POINTS = 3


WORDLE_DICT = {
    "word": "",
    "discarded_letters": [],
    "correct_letters": [],
    "partial_letters": ["-", "-", "-", "-", "-"],
    "users": [],
}


class wordle(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.generate_word.start()
        self.remove_users_from_wordle.start()

    def add_to_list(self, guild: nextcord.Guild, key: str, element: str):
        """Adds an element to the json file

        Args:
            guild (nextcord.Guild): guild to add the element
            key (str): key of the element
            element (str): element to add
        """
        server_path = get_server_path(guild)
        with open(server_path + WORDLE_JSON, "r+") as f:

            json_object = json.load(f)
            if element not in json_object[key]:
                json_object[key].append(element)
                json_object[key].sort()

            f.seek(0)
            json.dump(json_object, f)
            f.truncate()

    def add_discarded_letter(self, guild: nextcord.Guild, letter: str):
        """Adds a letter to the discarded letters list

        Args:
            guild (nextcord.Guild): guild to add the letter
            letter (str): letter to add
        """

        # Check if the letter is already in the list
        server_path = get_server_path(guild)
        with open(server_path + WORDLE_JSON, "r+") as f:

            json_object = json.load(f)
            letters = json_object["discarded_letters"]

            if letter not in letters:
                letters.append(letter)
                letters.sort()

            json_object["discarded_letters"] = letters
            f.seek(0)
            json.dump(json_object, f)
            f.truncate()

    def add_user(self, guild: nextcord.Guild, user: int):
        """Adds a user to json file

        Args:
            guild (nextcord.Guild): guild to add the letter
            user (int): id of user to add
        """

        # Check if the letter is already in the list
        server_path = get_server_path(guild)
        with open(server_path + WORDLE_JSON, "r+") as f:

            json_object = json.load(f)
            users = json_object["users"]

            if user not in users:
                users.append(user)

            json_object["users"] = users
            f.seek(0)
            json.dump(json_object, f)
            f.truncate()

    def add_correct_letter(self, guild: nextcord.Guild, letter: str):
        """Adds a letter to the correct letters list

        Args:
            guild (nextcord.Guild): guild to add the letter
            letter (str): letter to add
        """

        # Check if the letter is already in the list
        server_path = get_server_path(guild)
        with open(server_path + WORDLE_JSON, "r+") as f:

            json_object = json.load(f)
            letters = json_object["correct_letters"]

            if letter not in letters:
                letters.append(letter)
                letters.sort()

            json_object["correct_letters"] = letters
            f.seek(0)
            json.dump(json_object, f)
            f.truncate()

    def add_partial_letter(self, guild: nextcord.Guild, letter: str, index: int):
        """Adds a letter to the partial letters list

        Args:
            guild (nextcord.Guild): guild to add the letter
            letter (str): letter to add
        """
        server_path = get_server_path(guild)

        with open(server_path + WORDLE_JSON, "r+") as f:

            json_object = json.load(f)
            letters = json_object["partial_letters"]

            if letters[index] != "-":
                return

            letters[index] = letter

            f.seek(0)
            json.dump(json_object, f)
            f.truncate()

    def get_partial_letters(self, guild: nextcord.Guild) -> list:
        """Gets the partial letters

        Args:
            guild (nextcord.Guild): guild to get the letters

        Returns:
            list: list of partial letters
        """
        server_path = get_server_path(guild)
        with open(server_path + WORDLE_JSON, "r") as f:
            json_object = json.load(f)
            letters = json_object["partial_letters"]

        return letters

    def get_users(self, guild: nextcord.Guild) -> list:
        """Gets the users from json file

        Args:
            guild (nextcord.Guild): guild to get the users

        Returns:
            list: list of users
        """
        server_path = get_server_path(guild)
        with open(server_path + WORDLE_JSON, "r") as f:
            json_object = json.load(f)
            letters = json_object["users"]

        return letters

    def remove_users(self, guild: nextcord.Guild):
        """Removes users from json file

        Args:
            guild (nextcord.Guild): guild to remove the users
        """
        server_path = get_server_path(guild)
        with open(server_path + WORDLE_JSON, "r+") as f:

            json_object = json.load(f)
            json_object["users"] = []
            f.seek(0)
            json.dump(json_object, f)
            f.truncate()

    def get_discarded_letters(self, guild: nextcord.Guild) -> list:
        """Gets the discarded letters

        Args:
            guild (nextcord.Guild): guild to get the letters

        Returns:
            list: list of discarded letters
        """
        server_path = get_server_path(guild)
        with open(server_path + WORDLE_JSON, "r") as f:
            json_object = json.load(f)
            letters = json_object["discarded_letters"]

        return letters

    def get_correct_letters(self, guild: nextcord.Guild) -> list:
        """Gets the correct letters

        Args:
            guild (nextcord.Guild): guild to get the letters

        Returns:
            list: list of correct letters
        """
        server_path = get_server_path(guild)
        with open(server_path + WORDLE_JSON, "r") as f:
            json_object = json.load(f)
            letters = json_object["correct_letters"]

        return letters

    def word_guessed(self, guild: nextcord.Guild) -> bool:
        """Checks if the word of the day was guessed

        Args:
            guild (nextcord.Guild): guild to check

        Returns:
            bool: True if the word was guessed, False otherwise
        """
        server_path = get_server_path(guild)
        if os.path.isfile(server_path + WORDLE_JSON):
            return False
        return True

    def get_solution_word(self, guild: nextcord.Guild) -> str:
        """Gets the solution word for the guild

        Args:
            guild (nextcord.Guild): guild to get the word

        Returns:
            str: solution word
        """
        server_path = get_server_path(guild)
        with open(server_path + WORDLE_JSON, "r") as file:
            data = json.load(file)
        return data["word"]

    def get_random_word(self, guild: nextcord.Guild):
        """Selects a random word from the words dictionary

        ARgs:
            guild (nextcord.Guild): guild to get the word

        """
        server_path = get_server_path(guild)
        if not os.path.isfile(server_path + WORDLE_JSON):
            lines = open(resources_path + "words.txt").readlines()
            word = random.choice(lines).strip()
            # Create file
            with open(server_path + WORDLE_JSON, "w+") as f:
                WORDLE_DICT["word"] = word
                json_object = json.dumps(WORDLE_DICT)
                f.write(json_object)

    def word_in_word_list(self, word: str) -> bool:
        """Checks if a word is in the words list

        Args:
            word (str): word to check

        Returns:
            bool: True if the word is in the list, False otherwise
        """
        lines = open(resources_path + "words.txt").read().splitlines()

        if word in lines:
            return True
        return False

    def create_embed(self, ctx: commands.Context, word: str) -> nextcord.Embed:
        """Creates an embed with the word

        Args:
            ctx (commands.Context): _description_
            word (str): word to embed

        Returns:
            nextcord.Embed: embed with the word
        """
        word = self.process_word(ctx, word)

        discarded_letters = self.get_discarded_letters(ctx.guild)
        correct_letters = self.get_correct_letters(ctx.guild)
        partial_letters = self.get_partial_letters(ctx.guild)

        if correct_letters == []:
            correct_letters = "."
        else:
            correct_letters = ", ".join(correct_letters)

        if discarded_letters == []:
            discarded_letters = "."
        else:
            discarded_letters = ", ".join(discarded_letters)

        if partial_letters == []:
            partial_letters = "-----"

        embed = nextcord.Embed(title="Wordle")
        embed.add_field(name="Palabra", value=word, inline=False)
        embed.add_field(
            name="Solución parcial", value="".join(partial_letters), inline=False
        )
        embed.add_field(name="Letras acertadas", value=correct_letters, inline=False)
        embed.add_field(name="Letras descartadas", value=discarded_letters)
        return embed

    def correct_input(self, ctx: commands.Context, word: str) -> str:
        if self.word_guessed(ctx.guild):
            return "La palabra ya fue adivinada, espera hasta la siguiente palabra"

        if ctx.author.id in self.get_users(ctx.guild):
            now = datetime.now().hour
            return "No puedes jugar más hasta las {}:00".format(now + 1)

        word = word.lower()
        if len(word) != WORD_LENGHT:
            return "La palabra debe tener {} letras, inténtalo otra vez".format(
                WORD_LENGHT
            )

        if not self.word_in_word_list(word):
            return "La palabra no está en la lista de palabras, inténtalo otra vez"

        return None

    def process_word(self, ctx: commands.Context, word: str) -> str:
        """Processes the word to get the correct letters

        Args:
            ctx (commands.Context): context of the command
            word (str): word to process
        Returns:
            str: processed word with the squares
        """
        output = word + "\n"
        solution = self.get_solution_word(ctx.guild)
        count = 0
        for char1, char2 in zip(word, solution):
            if char1 in solution:
                self.add_to_list(ctx.guild, "correct_letters", char1)

                if char1 == char2:
                    output += GREEN_SQUARE
                    self.add_partial_letter(ctx.guild, char1, count)

                else:
                    output += YELLOW_SQUARE

            else:
                output += GREY_SQUARE
                self.add_to_list(ctx.guild, "discarded_letters", char1)
            count += 1

        return output

    @commands.command()
    async def guess(self, ctx: commands.Context, word: str):
        """Intentar adivinar la palabra del wordle"""

        # Check requirements are met
        aux = self.correct_input(ctx, word)
        if aux != None:
            msg = await ctx.send(aux)
            await msg.delete(delay=5)
            return

        # Add user to json
        self.add_user(ctx.guild, ctx.author.id)

        # Send embed
        embed = self.create_embed(ctx, word)
        await ctx.send(embed=embed)

        # Check if the word was guessed
        solution = self.get_solution_word(ctx.guild)
        if word == solution:
            await ctx.send("Palabra correcta!!!!")
            os.remove(get_server_path(ctx.guild) + WORDLE_JSON)

            # Get definition
            definicion = str(dle.search_by_word(word))
            await ctx.send('"{}": {}'.format(word, definicion))

            self.get_random_word(ctx.guild)
            await self.bot.channel_send(
                ctx.guild,
                "wordle",
                "Nueva palabra generada, intenta adivinarla con `fur guess`",
            )

    @tasks.loop(hours=1)
    async def remove_users_from_wordle(self):
        await asyncio.sleep(5)
        for guild in self.bot.guilds:
            self.remove_users(guild)

    @tasks.loop(hours=24)
    async def generate_word(self):
        for guild in self.bot.guilds:
            if self.word_guessed(guild):
                self.get_random_word(guild)
                await self.bot.channel_send(
                    guild,
                    "wordle",
                    "Nueva palabra generada, intenta adivinarla con `fur guess`",
                )

    # @remove_users_from_wordle.before_loop
    async def prep(self):
        """Waits some time to execute tasks"""

        hours_from_now = 1
        minutes_from_now = 0
        seconds_from_now = 0
        now = datetime.now()
        after = now + timedelta(
            hours=hours_from_now, minutes=minutes_from_now, seconds=seconds_from_now
        )
        # Comment to try tasks that are not at oclock
        after = after.replace(minute=0, second=0)

        delta = (after - now).total_seconds()

        await asyncio.sleep(delta)


def setup(bot: commands.Bot):
    bot.add_cog(wordle(bot))
