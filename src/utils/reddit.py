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
        self, sub_reddit: str, posts_limit: int, num: int
    ) -> list:
        """Gets a list of subreddit pics

        Args:
            sub_reddit (str): subreddit to get pics from
            pics_limit (int): num of pics to charge
            num (int): num of pics to return

        Returns:
            list: containing reddit posts
        """
        reddit = asyncpraw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
            check_for_async=False,
        )

        subreddit = await reddit.subreddit(sub_reddit)
        hot_posts = subreddit.hot(limit=posts_limit)

        posts = []
        async for post in hot_posts:
            if "jpg" in post.url or "png" in post.url and not post.over_18:
                posts.append(post.url)
        await reddit.close()
        return posts
