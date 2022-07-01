import logging
import tweepy as tw
import os
from utils.database import (
    check_record_in_database,
    clean_records,
    create_record,
    get_records_of_type,
    remove_record,
)
import nextcord
from nextcord import Embed
from nextcord.colour import Colour


log = logging.getLogger(__name__)


class Twitter:
    def __init__(self):
        consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        self.auth = tw.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tw.API(self.auth, wait_on_rate_limit=True)

    def get_latest_image(self, username: str) -> str:
        """Gets the URL the latest image url posted by some user

        Args:
            username (str): user to look

        Returns:
            str: URL of latest image posted
        """
        tweets = self.api.user_timeline(
            screen_name=username, count=200, include_rts=False, tweet_mode="extended"
        )
        for tweet in tweets:
            if "media" in tweet.entities:

                return tweet.entities["media"][0]["media_url"]

    def get_latest_images_not_repeated(
        self, guild: nextcord.Guild, username: str, count: int, record_type: str
    ) -> list:

        """Gets the URL the latest images urls posted by some user

        Args:
            guild (nextcord.Guild): guild to look
            username (str): user to look
            count (int): number of images to return

        Returns:
            list: containing URLs of latest image posted
        """

        output = []
        num = 0
        tweets = self.api.user_timeline(
            screen_name=username, count=100, include_rts=True, tweet_mode="extended"
        )
        for tweet in tweets:

            if "media" in tweet.entities:
                tweet_url = tweet.entities["media"][0]["media_url"]
                if not check_record_in_database(guild, tweet_url):
                    create_record(guild, record_type, tweet_url, username)
                    num += 1
                    output.append(tweet_url)

            if count == num:
                break

        # Remove records that are not fetched
        tweets_urls = [tweet.entities["media"][0]["media_url"] for tweet in tweets]
        clean_records(guild, "animal", username, tweets_urls)

        return output

    def get_latest_image_not_repeated(
        self,
        guild: nextcord.Guild,
        username: str,
        record_type: str,
    ) -> nextcord.Embed:

        """Gets the URL the latest image url posted by some user

        Args:
            guild (nextcord.Guild): guild to look
            username (str): user to look
            record_type (str): type of record

        Returns:
            nextcord.Embed: embed
        """

        output = None
        tweets = self.api.user_timeline(
            screen_name=username, count=100, include_rts=True, tweet_mode="extended"
        )

        for tweet in tweets:

            if "media" in tweet.entities:
                tweet_url = tweet.entities["media"][0]["media_url"]
                if not check_record_in_database(guild, tweet_url):
                    create_record(guild, record_type, tweet_url, username)

                    output = tweet
                    break

        if output is None:
            return None

        # Remove tweets from db if they are not fetched
        tweets_urls = [tweet.entities["media"][0]["media_url"] for tweet in tweets]
        clean_records(guild, record_type, username, tweets_urls)

        embed = self.create_embed(output)

        return embed

    def create_embed(self, tweet) -> Embed:
        """Creates an embed from a tweet

        Args:
            tweet (tw.Status): tweet to create embed from

        Returns:
            Embed: embed of tweet
        """
        user = tweet.user.name
        text = tweet.full_text
        embed = Embed(
            title="Twitter",
            description=text,
            color=Colour.from_rgb(29, 161, 242),
        )
        embed.set_image(url=tweet.entities["media"][0]["media_url"])
        embed.set_author(name=user, icon_url=tweet.user.profile_image_url)
        return embed
