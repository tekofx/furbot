import lightbulb
from functions import get_hot_subreddit_image

animal_history_txt = "files/resources/data/animal_history.txt"


class Animal(lightbulb.Plugin):
    @lightbulb.command()
    async def fox(self, context: lightbulb.Context):
        """Fotos de zorritos hermosos"""
        message = await context.respond("Buscando fotos de zorros hermosos")
        await context.respond(
            attachment=get_hot_subreddit_image(
                "foxes", 100, animal_history_txt, "Pics!"
            )
        )
        message.delete()

    @lightbulb.command()
    async def wolf(self, context: lightbulb.Context):
        """Fotos de lobos lobitos lobones"""
        message = await context.respond("Buscando fotos de lobos lobitos lobones")
        await context.respond(
            attachment=get_hot_subreddit_image(
                "wolves", 100, animal_history_txt, "Pics"
            )
        )
        await message.delete()


def load(bot) -> None:
    bot.add_plugin(Animal)
