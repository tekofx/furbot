from nextcord.ext import commands, tasks
from utils.bot import Bot
from utils.data import get_server_path, resources_path
import random
import logging
from datetime import date, datetime, timedelta, time
import asyncio
import nextcord
from pyrae import dle

import os

from utils.database import (
    check_user_in_wordle,
    create_word,
    empty_wordle_table,
    table_empty,
)

log = logging.getLogger(__name__)


GREEN_SQUARE = "🟩"
YELLOW_SQUARE = "🟨"
GREY_SQUARE = "⬜"
WORD_LENGHT = 5
WORD_FILE = "word.txt"


class wordle(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.generate_word.start()
        self.remove_users_from_wordle.start()

    def word_guessed(self, guild: nextcord.Guild) -> bool:
        """Checks if the word of the day was guesses

        Args:
            guild (nextcord.Guild): guild to check

        Returns:
            bool: True if the word was guessed, False otherwise
        """
        server_path = get_server_path(guild)
        if os.path.isfile(server_path + WORD_FILE):
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
        word = open(server_path + WORD_FILE, "r").read()
        return word

    def get_random_word(self, guild: nextcord.Guild):
        """Selects a random word from the words dictionary

        ARgs:
            guild (nextcord.Guild): guild to get the word

        """
        server_path = get_server_path(guild)
        if not os.path.isfile(server_path + WORD_FILE):

            lines = open(resources_path + "words.txt").readlines()
            word = random.choice(lines).strip()
            open(server_path + WORD_FILE, "w+").write(word)

    def word_in_word_dict(self, word: str) -> bool:
        """Checks if a word is in the words dictionary

        Args:
            word (str): word to check

        Returns:
            bool: True if the word is in the dictionary, False otherwise
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

        if check_user_in_wordle(ctx.guild, ctx.author.id):
            now = datetime.now().hour
            await ctx.send("No puedes jugar más hasta las {}:00".format(now + 1))
            return

        word = word.lower()
        if len(word) != WORD_LENGHT:
            await ctx.send(
                "La palabra debe tener {} letras, inténtalo otra vez".format(
                    WORD_LENGHT
                )
            )
            return

        if not self.word_in_word_dict(word):
            await ctx.send(
                "La palabra no está en la lista de palabras, inténtalo otra vez"
            )
            return

        # Add user to db
        create_word(ctx.guild, [word, ctx.author.id])

        # Generate squares
        solution = self.get_solution_word(ctx.guild)
        output = word + "\n"
        for char1, char2 in zip(word, solution):
            if char1 in solution:
                if char1 == char2:
                    output += GREEN_SQUARE
                else:
                    output += YELLOW_SQUARE
            else:
                output += GREY_SQUARE
        await ctx.send(output)

        if word == solution:
            await ctx.send("Palabra correcta!!!!")
            empty_wordle_table(ctx.guild)
            os.remove(get_server_path(ctx.guild) + "word.txt")

            # Get definition
            definicion = str(dle.search_by_word(word))
            await ctx.send('"{}": {}'.format(word, definicion))

            await ctx.send("Esperando a generar nueva palabra")

            # Wait randomly to generate a new word
            seconds = random.randint(1, 30) * 60
            log.info("Waiting {} seconds to generate a new word".format(seconds))
            await asyncio.sleep(seconds)
            self.get_random_word(ctx.guild)
            await self.bot.channel_send(
                ctx.guild,
                "wordle",
                "Nueva palabra generada, intenta adivinarla con `fur guess`",
            )

    @tasks.loop(hours=1)
    async def remove_users_from_wordle(self):
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

    @generate_word.before_loop
    async def prep(self):
        """Waits some time to execute tasks"""
        now = datetime.now()
        if now < datetime(now.year, now.month, now.day, 8, 0, 0):
            next_time = datetime(now.year, now.month, now.day, 8, 0, 0)
        else:
            next_time = (now + timedelta(days=1)).replace(hour=8, minute=0, second=0)
        hour_to_wait = datetime(next_time.year, next_time.month, next_time.day, 8)

        secs_to_wait = (hour_to_wait - datetime.now()).total_seconds()

        log.info(
            "Waiting to generate word and clear wordle table {} mins".format(
                str(secs_to_wait / 60)
            )
        )

        await asyncio.sleep(secs_to_wait)

    @remove_users_from_wordle.before_loop
    async def prep2(self):
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
