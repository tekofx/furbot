import logging
from utils.functions import exists_string_in_file, write_in_file
import praw
import os

log = logging.getLogger(__name__)


class Reddit:
    # TODO: Añadir reddit memes history
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
        history_file: str,
        not_flair: str = None,
    ):
        """Get a hot subreddit post image

        Args:
            sub_reddit (str): subreddit to get the image from
            posts_limit (int): maxium number of posts to get
            history_file (str): file to save the posts that where
            not_flair (str): flair not present in post

        Returns:
            str: url of image
        """
        posts = self.reddit.subreddit(sub_reddit).hot(limit=posts_limit)
        try:
            for post in posts:
                if post.over_18 is False:  # Check if post is SFW

                    if not_flair is None:

                        if post.url.endswith("jpg") and not exists_string_in_file(
                            history_file, post.url
                        ):
                            write_in_file(history_file, post.url + "\n")
                            return post.url
                    else:
                        if (
                            (
                                not post.link_flair_text
                                or not_flair in post.link_flair_text
                            )
                            and post.url.endswith("jpg")
                            and not exists_string_in_file(history_file, post.url)
                        ):
                            write_in_file(history_file, post.url + "\n")
                            return post.url

        except Exception as error:
            logging.error("Error in get_hot_subreddit_image: {}".format(error))
            return "Error: {}".format(error)
