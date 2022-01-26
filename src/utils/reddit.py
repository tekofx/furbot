import logging
import sqlite3
from utils.database import check_record_in_database, create_record
import os
import asyncpraw

log = logging.getLogger(__name__)


class Reddit:
    def __init__(self) -> None:
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = os.getenv("REDDIT_USER_AGENT")

    async def get_hot_subreddit_images(
        self,
        sub_reddit: str,
        posts_limit: int,
    ) -> list:
        reddit = asyncpraw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
            check_for_async=False,
        )

        subreddit = await reddit.subreddit(sub_reddit)
        log.info(sub_reddit + "\n")
        hot_posts = subreddit.hot(limit=posts_limit)
        posts = []
        async for post in hot_posts:
            if post.url.endswith("jpg") or post.url.endswith("png"):
                posts.append(post.url)
        return posts

    async def get_hot_subreddit_image(
        self,
        sub_reddit: str,
        posts_limit: int,
        database_connection: sqlite3.Connection,
    ) -> str:
        """Returns the URL of a subreddit post that has an image

        Args:
            sub_reddit (str): subreddit to look for
            posts_limit (int): limit of posts to load
            database_connection (sqlite3.Connection): Connection to database
        """
        reddit = asyncpraw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
            check_for_async=False,
        )

        subreddit = await reddit.subreddit(sub_reddit)
        await reddit.close()
        hot_posts = subreddit.hot(limit=posts_limit)
        posts = []
        async for post in hot_posts:
            posts.append(post)

        try:
            for post in posts:
                if post.over_18 is False:

                    if post.url.endswith("jpg") and not check_record_in_database(
                        database_connection, post.url
                    ):
                        create_record(database_connection, ["reddit", post.url])
                        log.info("Return {}".format(post.url))
                        return post.url

        except Exception as error:
            logging.error("Error in get_hot_subreddit_image: {}".format(error))
            return "Error: {}".format(error)
