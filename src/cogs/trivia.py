import asyncio
import random
from nextcord.ext import commands
from utils.bot import Bot
import requests
import nextcord
from nextcord import Interaction
import os

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

    @nextcord.slash_command(name="trivial")
    async def trivial(self, interaction: Interaction, rondas: int = 1):
        """Preguntas entre varias personas, a ver quien acierta mas"""
        await interaction.send("Responded a las siguientes preguntas:")
        victories = {}
        for _ in range(rondas):

            # Get Trivia data
            var = self.get_trivia_data()
            correct_answer = var["correct_answer"]

            # Create and send embed
            embed = self.create_embed(var)
            embed_msg = await interaction.channel.send(embed=embed)

            await embed_msg.add_reaction(EMOJI_A)
            await embed_msg.add_reaction(EMOJI_B)
            await embed_msg.add_reaction(EMOJI_C)
            await embed_msg.add_reaction(EMOJI_D)

            # Wait for answer
            await interaction.channel.send("Esperando 10 segundos")
            await asyncio.sleep(5)
            await interaction.channel.send("Quedan 5 segundos")
            await asyncio.sleep(5)

            message = await interaction.channel.fetch_message(embed_msg.id)
            reactions = message.reactions
            for reaction in reactions:
                reaction_answer = var["answers"][reaction.emoji]
                if reaction_answer == correct_answer:
                    aux = await reaction.users().flatten()
                    aux.remove(self.bot.user)
                    users = list(dict.fromkeys(aux))

                    for user in users:
                        if user not in victories:
                            temp = {user: 1}
                            victories.update(temp)
                        else:
                            temp = {user, victories[user] + 1}
                            victories.update(temp)

            if len(users) == 0:
                msg = "No hay ganadores"
            else:
                msg = "{} ganó la trivia".format("".join(str(x.mention) for x in users))
            await interaction.channel.send(msg)

        for x in victories:
            await interaction.channel.send(
                "{} ganó {} rondas".format(x.mention, victories[x])
            )

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

    def process_string(self, string):
        string = string.replace("&rsquo;", "'")
        string = string.replace("&quot;", '"')
        string = string.replace("&#039;", "'")
        string = string.replace("&amp;", "&")

        return string

    def get_trivia_data(self):
        data = requests.get("https://opentdb.com/api.php?amount=1&category=9").json()
        data = data["results"][0]

        # Get data
        question = self.process_string(data["question"])
        correct_answer = self.process_string(data["correct_answer"])
        incorrect_answers = []
        for x in data["incorrect_answers"]:
            incorrect_answers.append(self.process_string(x))
        difficulty = data["difficulty"]
        question_type = data["type"]

        # Randomize answers
        incorrect_answers.append(correct_answer)
        incorrect_answers = list(dict.fromkeys(incorrect_answers))
        answers = random.sample(incorrect_answers, k=4)

        var = {
            "title": "Trivia",
            "question": question,
            "difficulty": difficulty,
            "type": question_type,
            "correct_answer": correct_answer,
            "answers": {
                EMOJI_A: answers[0],
                EMOJI_B: answers[1],
                EMOJI_C: answers[2],
                EMOJI_D: answers[3],
            },
        }
        return var

    @nextcord.slash_command(name="pregunta")
    async def pregunta(self, interaction: Interaction):
        """Pregunta al azar"""
        await interaction.send("Responde a las siguientes preguntas:")

        def check(reaction: nextcord.Reaction, user: nextcord.Member) -> bool:
            return user.id == interaction.user.id

        # Get Trivia data
        var = self.get_trivia_data()
        answers = var["answers"]
        correct_answer = var["correct_answer"]

        # Create and send embed
        embed = self.create_embed(var)
        embed_msg = await interaction.channel.send(embed=embed)
        await embed_msg.add_reaction(EMOJI_A)
        await embed_msg.add_reaction(EMOJI_B)
        await embed_msg.add_reaction(EMOJI_C)
        await embed_msg.add_reaction(EMOJI_D)

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=60.0, check=check
            )
        except asyncio.TimeoutError:
            await interaction.channel.send("Tiempo agotado")
            return

        if answers[reaction.emoji] == correct_answer:
            await interaction.channel.send("Correcto")
        else:
            await interaction.channel.send(
                "Incorrecto, la respuesta correcta es: {}".format(correct_answer)
            )


def setup(bot: commands.Bot):
    bot.add_cog(trivia(bot))
