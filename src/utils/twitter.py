import logging
import sqlite3
import tweepy as tw
import os
from utils.database import check_record_in_database


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
        """Gets the URL the latest image posted by some user

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

    def get_latest_image_not_repeated(
        self, username: str, database_connection: sqlite3.Connection
    ) -> str:
        """Gets the latest image checking in a database if that image was obtained
        before. If the image is in the database, it will get another until the picture
        is not in the database

        Args:
            username (str): user to search
            database_connection (sqlite3.Connection): Connection to database

        Returns:
            str: URL of image not repeated
        """
        tweets = self.api.user_timeline(
            screen_name=username, count=200, include_rts=False, tweet_mode="extended"
        )
        for tweet in tweets:
            if "media" in tweet.entities and not check_record_in_database(
                database_connection, tweet.entities["media"][0]["media_url"]
            ):

                return tweet.entities["media"][0]["media_url"]
