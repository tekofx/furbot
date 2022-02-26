from nextcord.ext import commands, tasks
from utils.bot import Bot
from utils.data import resources_path
import random
import logging
from datetime import date, datetime, timedelta, time
import asyncio

from utils.database import (
    check_user_in_wordle,
    create_word,
    empty_wordle_table,
    get_word,
    table_empty,
)

log = logging.getLogger(__name__)


GREEN_SQUARE = "🟩"
YELLOW_SQUARE = "🟨"
GREY_SQUARE = "⬜"
WORD_NUM_CHARS = 5


class wordle(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.generate_word.start()

    def get_random_word(self) -> str:
        """get a random word from the wordle database

        Returns:
            str: word from the wordle database
        """
        lines = open(resources_path + "words.txt").readlines()
        word = random.choice(lines).strip()
        return word

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
        if table_empty(ctx.guild, "wordle"):
            await ctx.send("Ya se ha adivinado la palabra de hoy")
            return

        solution = get_word(ctx.guild)
        word = word.lower()

        if check_user_in_wordle(ctx.guild, ctx.author.id):
            # create_word(ctx.guild, [word, ctx.author.id])
            await ctx.send("No puedes jugar más hoy")
            return

        if len(word) != WORD_NUM_CHARS:
            await ctx.send(
                "La palabra debe tener {} letras, inténtalo otra vez".format(
                    WORD_NUM_CHARS
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

    @tasks.loop(hours=24)
    async def generate_word(self):
        # Generar palabra para adivinar
        log.info("Generating word for each server")

        for guild in self.bot.guilds:
            create_word(guild, [self.get_random_word(), 0])
            msg = "Ya está disponible la palabra de hoy, utiliza `fur guess` para adivinarla"
            await self.bot.channel_send(guild, "wordle", msg)

    @tasks.loop(hours=24)
    async def give_solution(self):
        # Dar la palabra solucion

        for guild in self.bot.guilds:
            word = get_word(guild)
            msg = "No se adivinó la palabra de hoy, la palabra era: {}".format(word)
            await self.bot.channel_send(guild, "wordle", msg)

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

        log.info("Waiting to generate word {} mins".format(str(secs_to_wait / 60)))

        await asyncio.sleep(secs_to_wait)

    @generate_word.before_loop
    async def prep2(self):
        """Waits some time to execute tasks"""
        now = datetime.now()
        if now < datetime(now.year, now.month, now.day, 23, 59, 0):
            next_time = datetime(now.year, now.month, now.day, 23, 59, 0)
        else:
            next_time = (now + timedelta(days=1)).replace(hour=23, minute=59, second=0)
        hour_to_wait = datetime(next_time.year, next_time.month, next_time.day, 23, 59)

        secs_to_wait = (hour_to_wait - datetime.now()).total_seconds()

        log.info("Waiting to give solution {} mins".format(str(secs_to_wait / 60)))

        await asyncio.sleep(secs_to_wait)


def setup(bot: commands.Bot):
    bot.add_cog(wordle(bot))
