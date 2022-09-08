import io
from nextcord.ext import commands, tasks
from utils.bot import Bot
from utils.data import get_server_path, resources_path
import random
from utils import logger
from datetime import datetime, timedelta
import asyncio
import nextcord
from pyrae import dle
import json
import os
from PIL import ImageFont, ImageDraw, Image
from utils.data import meme_resources_path
from nextcord import Interaction, SlashOption
import os


log = logger.getLogger(__name__)


GREEN_SQUARE = "🟩"
YELLOW_SQUARE = "🟨"
GREY_SQUARE = "⬜"
WORD_LENGHT = 5
WORDLE_JSON = "wordle.json"

GREEN = "#5c824c"
YELLOW = "#c8a111"
GREY = "#474b4d"


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

    def add_to_list(self, interaction: Interaction, key: str, element: str):
        """Adds an element to the json file

        Args:
            ctx (commands.Context): context of the command
            key (str): key of the element
            element (str): element to add
        """
        server_path = get_server_path(interaction.guild)
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

    def add_partial_letter(self, interaction: Interaction, letter: str, index: int):
        """Adds a letter to the partial letters list

        Args:
            guild (nextcord.Guild): guild to add the letter
            letter (str): letter to add
        """
        server_path = get_server_path(interaction.guild)

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

    async def create_and_send_embed(
        self, interaction: Interaction, word: str
    ) -> nextcord.Embed:
        """Creates and sends an embed with the word

        Args:
            ctx (commands.Context): _description_
            word (str): word to embed

        Returns:
            nextcord.Embed: embed with the word
        """
        info = self.process_word(interaction, word)
        word = info["word"] + "\n" + "".join(info["squares"])
        picture = self.word_picture(info["word"], info["colors"])
        file = nextcord.File(picture, "output.png")

        discarded_letters = self.get_discarded_letters(interaction.guild)
        correct_letters = self.get_correct_letters(interaction.guild)
        partial_letters = self.get_partial_letters(interaction.guild)

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
        embed.add_field(name="Palabra", value=word, inline=True)
        embed.add_field(
            name="Solución parcial", value="".join(partial_letters), inline=True
        )
        embed.add_field(name="Letras acertadas", value=correct_letters, inline=False)
        embed.add_field(name="Letras descartadas", value=discarded_letters, inline=True)
        embed.set_image(url="attachment://output.png")

        await interaction.send(file=file, embed=embed)

    def correct_input(self, interaction: Interaction, word: str) -> str:
        if self.word_guessed(interaction.guild):
            return "La palabra ya fue adivinada, espera hasta la siguiente palabra"

        if interaction.user.id in self.get_users(interaction.guild):
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

    def word_picture(self, word: str, colors: list) -> io.BytesIO:
        """Creates a picture of the word"""
        word = word.upper()
        image = Image.new("RGB", (600, 300), "white")
        font = ImageFont.truetype(meme_resources_path + "Calibri.ttf", 100)
        x = 50
        y = 100

        for letter, color in zip(word, colors):
            square = Image.new("RGB", (90, 90), color)
            square_w, square_h = square.size
            text = ImageDraw.Draw(square)
            text_w, text_h = text.textsize(letter, font=font)
            text.text(
                ((square_w - text_w) / 2, (square_h - text_h) / 2 - 5),
                letter,
                font=font,
                fill="black",
            )
            image.paste(square, (x, y))
            x += 100

        bytes_io = io.BytesIO()
        image.save(bytes_io, "PNG")
        bytes_io.seek(0)
        return bytes_io

    def process_word(self, interaction: Interaction, word: str) -> dict:
        """Processes the word to get the correct letters

        Args:
            ctx (commands.Context): context of the command
            word (str): word to process
        Returns:
            dict: dictionary with {word:"word", squares:[], colors:[]}
        """
        var = {"word": word, "squares": [], "colors": []}
        solution = self.get_solution_word(interaction.guild)
        count = 0
        for char1, char2 in zip(word, solution):
            if char1 in solution:
                self.add_to_list(interaction, "correct_letters", char1)

                if char1 == char2:
                    var["squares"].append(GREEN_SQUARE)
                    var["colors"].append(GREEN)
                    self.add_partial_letter(interaction, char1, count)

                else:
                    var["squares"].append(YELLOW_SQUARE)
                    var["colors"].append(YELLOW)

            else:
                var["squares"].append(GREY_SQUARE)
                var["colors"].append(GREY)
                self.add_to_list(interaction, "discarded_letters", char1)
            count += 1

        return var

    @nextcord.slash_command(name="guess")
    async def guess(self, interaction: Interaction, word: str):
        """Intentar adivinar la palabra del wordle"""
        word = word.lower()
        # Check requirements are met
        aux = self.correct_input(interaction, word)
        if aux != None:
            msg = await interaction.send(aux)
            await msg.delete(delay=5)
            return

        # Add user to json
        self.add_user(interaction.guild, interaction.user.id)

        # Send embed
        await self.create_and_send_embed(interaction, word)

        # Check if the word was guessed
        solution = self.get_solution_word(interaction.guild)
        if word == solution:
            await interaction.send("Palabra correcta!!!!")
            os.remove(get_server_path(interaction.guild) + WORDLE_JSON)

            # Get definition
            definicion = str(dle.search_by_word(word))
            await interaction.send('"{}": {}'.format(word, definicion))

            self.get_random_word(interaction.guild)
            await self.bot.channel_send(
                interaction.guild,
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
