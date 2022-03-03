from http import server
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

from utils.database import (
    user_in_wordle,
    create_word,
    empty_wordle_table,
    table_empty,
    word_in_wordle,
)

log = logging.getLogger(__name__)


GREEN_SQUARE = "🟩"
YELLOW_SQUARE = "🟨"
GREY_SQUARE = "⬜"
WORD_LENGHT = 5
WORDLE_JSON = "wordle.json"


WORDLE_DICT = {
    "word": "",
    "discarded_letters": [],
    "partial_letters": ["-", "-", "-", "-", "-"],
}


class wordle(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.generate_word.start()
        self.remove_users_from_wordle.start()

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

    def discarded_letters_txt(self, guild: nextcord.Guild) -> str:
        output = "Letras descartadas: "

        with open(get_server_path(guild) + WORDLE_JSON, "r") as f:
            json_object = json.load(f)
            letters = json_object["discarded_letters"]
            output += ", ".join(letters)

        return output

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

    @commands.command()
    async def guess(self, ctx: commands.Context, word: str):
        """Intentar adivinar la palabra del wordle"""
        if self.word_guessed(ctx.guild):
            await ctx.send(
                "La palabra ya fue adivinada, espera hasta la siguiente palabra"
            )
            return

        if user_in_wordle(ctx.guild, ctx.author.id):
            now = datetime.now().hour
            msg = await ctx.send("No puedes jugar más hasta las {}:00".format(now + 1))
            await msg.delete(delay=4)
            await ctx.message.delete(delay=4)
            return

        word = word.lower()
        if len(word) != WORD_LENGHT:
            msg = await ctx.send(
                "La palabra debe tener {} letras, inténtalo otra vez".format(
                    WORD_LENGHT
                )
            )
            await msg.delete(delay=4)
            await ctx.message.delete(delay=4)

            return

        if not self.word_in_word_list(word):
            await ctx.send(
                "La palabra no está en la lista de palabras, inténtalo otra vez"
            )
            await msg.delete(delay=4)
            await ctx.message.delete(delay=4)

            return

        # Add user to db
        create_word(ctx.guild, [word, ctx.author.id])

        # Generate squares
        solution = self.get_solution_word(ctx.guild)
        output = word + "\n"
        count = 0
        for char1, char2 in zip(word, solution):
            if char1 in solution:
                if char1 == char2:
                    output += GREEN_SQUARE
                    self.add_partial_letter(ctx.guild, char1, count)
                    count += 1

                else:
                    output += YELLOW_SQUARE

            else:
                output += GREY_SQUARE
                self.add_discarded_letter(ctx.guild, char1)

        discarded_letters = self.get_discarded_letters(ctx.guild)
        partial_letters = self.get_partial_letters(ctx.guild)
        output += "\n\nSolucion parcial: " + "".join(partial_letters)
        output += "\n\nLetras descartadas: " + ", ".join(discarded_letters)
        await ctx.send(output)

        if word == solution:
            await ctx.send("Palabra correcta!!!!")
            empty_wordle_table(ctx.guild)
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
            empty_wordle_table(guild)

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

    @remove_users_from_wordle.before_loop
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
