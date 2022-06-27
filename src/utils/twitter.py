import logging
import tweepy as tw
import os
from utils.database import check_record_in_database
import nextcord

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

    def get_timeline(self, username: str) -> list:
        """Get the first 200 posts of a user

        Args:
            username (str): user to get posts from

        Returns:
            list: containing tweets
        """
        tweets = self.api.user_timeline(
            screen_name=username, count=200, include_rts=False, tweet_mode="extended"
        )
        return tweets

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
        self, guild: nextcord.Guild, username: str, count: int
    ) -> list:

        """Gets the URL the latest images urls posted by some user

        Args:
            guild (nextcord.Guild): guild to look
            username (str): user to look
            count (int): number of images to return

        Returns:
            list: containin URLs of latest image posted
        """

        images = []
        num = 0
        tweets = self.api.user_timeline(
            screen_name=username, count=200, include_rts=True, tweet_mode="extended"
        )
        for tweet in tweets:

            if "media" in tweet.entities:
                tweet_url = tweet.entities["media"][0]["media_url"]
                if not check_record_in_database(guild, tweet_url):

                    num += 1
                    images.append(tweet_url)

            if count == num:
                break

        return images
