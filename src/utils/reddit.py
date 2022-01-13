import logging
import sqlite3
from utils.database import check_record_in_database, create_record
import praw
import os

log = logging.getLogger(__name__)


class Reddit:
    def __init__(self) -> None:
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
            check_for_async=False,
        )

    def get_hot_subreddit_image(
        self,
        sub_reddit: str,
        posts_limit: int,
        database_connection: sqlite3.Connection,
        not_flair: str = None,
    ) -> None:
        """Returns the URL of a subreddit post that has an image

        Args:
            sub_reddit (str): subreddit to look for
            posts_limit (int): limit of posts to load
            database_connection (sqlite3.Connection): Connection to database
            not_flair (str, optional): Flairs to avoid. Defaults to None.
        """
        posts = self.reddit.subreddit(sub_reddit).hot(limit=posts_limit)
        try:
            for post in posts:

                if post.over_18 is False:  # Check if post is SFW

                    if not_flair is None:

                        if post.url.endswith("jpg") and not check_record_in_database(
                            database_connection, post.url
                        ):
                            create_record(database_connection, ["reddit", post.url])
                            return post.url
                    else:
                        if (
                            (
                                not post.link_flair_text
                                or not_flair in post.link_flair_text
                            )
                            and post.url.endswith("jpg")
                            and not check_record_in_database(
                                database_connection, post.url
                            )
                        ):
                            create_record(database_connection, ["reddit", post.url])

                            return post.url

        except Exception as error:
            logging.error("Error in get_hot_subreddit_image: {}".format(error))
            return "Error: {}".format(error)
