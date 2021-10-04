import lightbulb
from functions import exists_string_in_file, get_hot_subreddit_image, write_in_file
from dotenv import load_dotenv
import os
import tweepy as tw
import requests

animal_history_txt = "files/resources/data/animal_history.txt"

load_dotenv()
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")


class Animal(lightbulb.Plugin):
    def __init__(self, *, name: str = None) -> None:
        super().__init__(name=name)
        self.auth = tw.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tw.API(self.auth, wait_on_rate_limit=True)

    @lightbulb.command()
    async def fox(self, ctx: lightbulb.Context):
        message = await ctx.respond("Buscando fotos de zorros hermosos")
        tweets = self.api.user_timeline(
            screen_name="hourlyFox",
            count=200,
            include_rts=False,
        )

        for tweet in tweets:
            tweet_image_url = tweet.entities["media"][0]["media_url"]
            if not exists_string_in_file(animal_history_txt, tweet_image_url):
                write_in_file(animal_history_txt, tweet_image_url + "\n")
                r = requests.get(tweet_image_url, allow_redirects=True)
                open("files/" + "image.jpg", "wb").write(r.content)
                break

        await message.delete()
        await ctx.respond(attachment="files/" + "image.jpg")
        os.remove("files/image.jpg")

    @lightbulb.command()
    async def wolf(self, ctx: lightbulb.Context):
        message = await ctx.respond("Buscando fotos de lobos lobitos lobones")
        tweets = self.api.user_timeline(
            screen_name="hourlywolvesbot",
            count=200,
            include_rts=False,
        )

        for tweet in tweets:
            tweet_image_url = tweet.entities["media"][0]["media_url"]
            if not exists_string_in_file(animal_history_txt, tweet_image_url):
                write_in_file(animal_history_txt, tweet_image_url + "\n")
                r = requests.get(tweet_image_url, allow_redirects=True)
                open("files/" + "image.jpg", "wb").write(r.content)
                break

        await message.delete()
        await ctx.respond(attachment="files/" + "image.jpg")
        os.remove("files/image.jpg")


def load(bot) -> None:
    bot.add_plugin(Animal)
