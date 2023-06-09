from html import entities
from core import logger
import tweepy as tw
import os
import nextcord
from nextcord import Embed
from nextcord.colour import Colour
from core.database import Database

log = logger.getLogger(__name__)


class Twitter:
    def __init__(self,db:Database) -> None:
        consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        self.auth = tw.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tw.API(self.auth, wait_on_rate_limit=True)
        self.db = db

    def exists_account(self, username: str) -> bool:
        try:
            tweets = self.api.user_timeline(
                screen_name=username,
                count=200,
                include_rts=False,
                tweet_mode="extended",
            )
        except Exception:
            return False

        return True

    def get_latest_media(self, username: str) -> str:
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
                return tweet.entities["media"][0]["expanded_url"]

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
            screen_name=username, count=50, include_rts=True, tweet_mode="extended"
        )
        for tweet in tweets:

            if "media" in tweet.entities:
                tweet_url = tweet.entities["media"][0]["media_url"]
                
                if not self.db.record_exists(guild, tweet_url):
                    self.db.insert_record(guild, record_type, tweet_url,username)
                    num += 1
                    output.append(tweet_url)

            if count == num:
                break

        # Remove records that are not fetched
        tweets_urls = [
            tweet.entities["media"][0]["media_url"] if "media" in tweet.entities else ""
            for tweet in tweets
        ]
        self.db.clean_records(guild, "animal", tweets_urls)

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
                
                if not self.db.record_exists(guild, tweet_url):
                    self.db.insert_record(guild, record_type, tweet_url, username)

                    output = tweet
                    break
        
        if output is None:
            return None

        # Remove tweets from db if they are not fetched
        tweets_urls = [
            tweet.entities["media"][0]["media_url"] if "media" in tweet.entities else ""
            for tweet in tweets
        ]
        self.db.clean_records(guild, record_type, tweets_urls)

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
