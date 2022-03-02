import asyncio
import random
from nextcord.ext import commands
from utils.bot import Bot
import requests
import nextcord


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
    async def pregunta(self, ctx: commands.Context):
        """Pregunta al azar"""

        def check(reaction: nextcord.Reaction, user: nextcord.Member) -> bool:
            return user.id == ctx.author.id

        data = requests.get("https://opentdb.com/api.php?amount=1&category=9").json()
        data = data["results"][0]

        # Get data
        question = data["question"]
        correct_answer = data["correct_answer"]
        incorrect_answers = data["incorrect_answers"]
        difficulty = data["difficulty"]
        question_type = data["type"]

        # Randomize answers
        incorrect_answers.append(correct_answer)
        answers = random.choices(incorrect_answers, k=4)

        ANSWERS_DICT[EMOJI_A] = answers[0]
        ANSWERS_DICT[EMOJI_B] = answers[1]
        ANSWERS_DICT[EMOJI_C] = answers[2]
        ANSWERS_DICT[EMOJI_D] = answers[3]

        # Create Embed
        embed = nextcord.Embed(title="Trivia", description=question, color=0x00FF00)
        embed.add_field(name="Dificultad", value=difficulty, inline=True)
        embed.add_field(name="Tipo", value=question_type, inline=True)
        embed.add_field(name="Opcion A", value=answers[0], inline=False)
        embed.add_field(name="Opcion B", value=answers[1], inline=False)
        embed.add_field(name="Opcion C", value=answers[2], inline=False)
        embed.add_field(name="Opcion D", value=answers[3], inline=False)

        embed = await ctx.send(embed=embed)
        await embed.add_reaction(EMOJI_A)
        await embed.add_reaction(EMOJI_B)
        await embed.add_reaction(EMOJI_C)
        await embed.add_reaction(EMOJI_D)

        # msg = await self.bot.wait_for("message", check=check, timeout=60)
        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=60.0, check=check
            )
        except asyncio.TimeoutError:
            await ctx.send("Tiempo agotado")
            return

        if ANSWERS_DICT[reaction.emoji] == correct_answer:
            await ctx.send("Correcto")
        else:
            await ctx.send(
                "Incorrecto, la respuesta correcta es: {}".format(correct_answer)
            )


def setup(bot: commands.Bot):
    bot.add_cog(trivia(bot))
