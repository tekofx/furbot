import logging
import requests
import tweepy as tw
import os
from utils.functions import write_in_file, exists_string_in_file
from plugins.animal import animal_history_txt


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

    def get_timeline(self, username: str):
        tweets = self.api.user_timeline(
            screen_name=username, count=200, include_rts=False, tweet_mode="extended"
        )
        return tweets

    def get_latest_image(self, username: str):
        tweets = self.api.user_timeline(
            screen_name=username, count=200, include_rts=False, tweet_mode="extended"
        )
        for tweet in tweets:
            if "media" in tweet.entities:
                return tweet
