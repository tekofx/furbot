import lightbulb
from utils.functions import exists_string_in_file, write_in_file
from dotenv import load_dotenv
import os
import tweepy as tw
import requests
import logging

animal_history_txt = "files/resources/data/animal_history.txt"
log = logging.getLogger(__name__)

load_dotenv()
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")


class Animal(lightbulb.Plugin):
    def __init__(self):
        super().__init__(name="Animal")
        self.auth = tw.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tw.API(self.auth, wait_on_rate_limit=True)

    @lightbulb.command("fox", "Fotos de zorros hermosos")
    async def fox(self, ctx: lightbulb.context.Context):
        """Fotos de zorros hermosos"""
        await self.bot.rest.trigger_typing(ctx.get_channel())
        message = await ctx.respond("Buscando fotos de zorros hermosos")
        self.get_animal_image("hourlyFox")
        await ctx.respond(attachment="files/" + "image.jpg")
        os.remove("files/image.jpg")
        await message.delete()

    @lightbulb.command("arctic", "Fotos de zorros hermosos")
    async def arctic_fox(self, ctx: lightbulb.context.Context):
        """Fotos de zorros hermosos"""
        await self.bot.rest.trigger_typing(ctx.get_channel())
        message = await ctx.respond("Buscando fotos de zorros hermosos")
        self.get_animal_image("DailyArcticFox")
        await ctx.respond(attachment="files/" + "image.jpg")
        os.remove("files/image.jpg")
        await message.delete()

    @lightbulb.command("wolf", "Fotos de lobos lobitos lobones")
    async def wolf(self, ctx: lightbulb.context.Context):
        """Fotos de lobos lobitos lobones"""
        await self.bot.rest.trigger_typing(ctx.get_channel())
        message = await ctx.respond("Buscando fotos de lobos lobitos lobones")
        self.get_animal_image("hourlywolvesbot")
        await ctx.respond(attachment="files/" + "image.jpg")
        os.remove("files/image.jpg")
        await message.delete()

    @lightbulb.command("bird", "Fotos de pajaritos")
    async def bird(self, ctx: lightbulb.context.Context):
        """Fotos de pajaritos"""
        await self.bot.rest.trigger_typing(ctx.get_channel())
        try:
            message = await ctx.respond("Buscando fotos de pajaritos")
            self.get_animal_image("eugeniogarciac2")
            await ctx.respond(attachment="files/" + "image.jpg")
            os.remove("files/image.jpg")
            await message.delete()
        except Exception as error:
            log.info("Error ocurred: {}".format(error))

    @lightbulb.command("pigeon", "Fotos de palomas achuchables")
    async def pigeon(self, ctx: lightbulb.context.Context):
        """Fotos de palomas achuchables"""
        await self.bot.rest.trigger_typing(ctx.get_channel())
        try:
            message = await ctx.respond("Buscando fotos de palomas achuchables")
            self.get_animal_image("a_london_pigeon")
            await ctx.respond(attachment="files/" + "image.jpg")
            os.remove("files/image.jpg")
            await message.delete()
        except Exception as error:
            log.info("Error ocurred: {}".format(error))

    def get_animal_image(self, account: str):
        tweets = self.bot.twitter.get_timeline(account)
        for tweet in tweets:
            if "media" in tweet.entities:
                tweet_image_url = tweet.entities["media"][0]["media_url"]
                if not exists_string_in_file(animal_history_txt, tweet_image_url):
                    write_in_file(animal_history_txt, tweet_image_url + "\n")
                    r = requests.get(tweet_image_url, allow_redirects=True)
                    open("files/" + "image.jpg", "wb").write(r.content)
                    break


def load(bot: lightbulb.BotApp):
    bot.add_plugin(Animal())


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin("Animal")
