import asyncio
import random
import re
from nextcord.ext import commands
from utils.bot import Bot
import requests
import nextcord
from utils.data import resources_path

EMOJI_A = "🇦"
EMOJI_B = "🇧"
EMOJI_C = "🇨"
EMOJI_D = "🇩"

ANSWERS_DICT = {
    EMOJI_A: "A",
    EMOJI_B: "B",
    EMOJI_C: "C",
    EMOJI_D: "D",
}


class trivia(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def trivial(self, ctx: commands.Context):

        pass

    def create_embed(self, trivial_dict: dict) -> nextcord.Embed:
        """Creates a embed

        Args:
            trivial_dict (dict): dict with the information containing
            {
            "title": "",
            "question": "",
            "difficulty": "",
            "type": "",
            "answers": {
                EMOJI_A: "",
                EMOJI_B: "",
                EMOJI_C: "",
                EMOJI_D: "",
            },
        }

        Returns:
            nextcord.Embed: embed with the information
        """
        answers = trivial_dict["answers"]

        embed = nextcord.Embed(
            title="Trivia", description=trivial_dict["question"], color=0x00FF00
        )
        embed.add_field(
            name="Dificultad", value=trivial_dict["difficulty"], inline=True
        )
        embed.add_field(name="Tipo", value=trivial_dict["type"], inline=True)
        embed.add_field(name="Opcion A", value=answers[EMOJI_A], inline=False)
        embed.add_field(name="Opcion B", value=answers[EMOJI_B], inline=False)
        embed.add_field(name="Opcion C", value=answers[EMOJI_C], inline=False)
        embed.add_field(name="Opcion D", value=answers[EMOJI_D], inline=False)
        embed.set_thumbnail(
            url="https://cdn3.f-cdn.com/contestentries/1233731/27978425/5a61f080ea253_thumb900.jpg"
        )
        return embed

    @commands.command()
    async def pregunta(self, ctx: commands.Context):
        """Pregunta al azar"""

        def check(reaction: nextcord.Reaction, user: nextcord.Member) -> bool:
            return user.id == ctx.author.id

        data = requests.get("https://opentdb.com/api.php?amount=1&category=9").json()
        data = data["results"][0]

        # Get data
        question = data["question"].replace("&quot;", "'")
        correct_answer = data["correct_answer"]
        incorrect_answers = data["incorrect_answers"]
        difficulty = data["difficulty"]
        question_type = data["type"]

        # Randomize answers
        incorrect_answers.append(correct_answer)
        answers = random.sample(incorrect_answers, k=4)

        var = {
            "title": "Trivia",
            "question": question,
            "difficulty": difficulty,
            "type": question_type,
            "answers": {
                EMOJI_A: answers[0],
                EMOJI_B: answers[1],
                EMOJI_C: answers[2],
                EMOJI_D: answers[3],
            },
        }

        embed = self.create_embed(var)

        embed_msg = await ctx.send(embed=embed)
        await embed_msg.add_reaction(EMOJI_A)
        await embed_msg.add_reaction(EMOJI_B)
        await embed_msg.add_reaction(EMOJI_C)
        await embed_msg.add_reaction(EMOJI_D)

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=60.0, check=check
            )
        except asyncio.TimeoutError:
            await ctx.send("Tiempo agotado")
            return

        if var["answers"][reaction.emoji] == correct_answer:
            await ctx.send("Correcto")
        else:
            await ctx.send(
                "Incorrecto, la respuesta correcta es: {}".format(correct_answer)
            )


def setup(bot: commands.Bot):
    bot.add_cog(trivia(bot))
