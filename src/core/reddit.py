from core import logger
import nextcord
import os
import asyncpraw
from nextcord import Embed
from nextcord.colour import Colour
from nextcord.ext import commands
from core.database import Database
log = logger.getLogger(__name__)


class Reddit:
    def __init__(self,db:Database) -> None:
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = os.getenv("REDDIT_USER_AGENT")
        self.reddit = asyncpraw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
            check_for_async=False,
        )
        self.db = db
        log.info("Enabled Reddit")

    async def exists_subreddit(self, name: str) -> bool:
        """Checks if a subreddit exists

        Args:
            name (str): name of subrredit

        Returns:
            bool: True if subreddit exists
        """
        try:
            subreddit = await self.reddit.subreddit(name)
            hot_posts = subreddit.hot(limit=1)
            async for post in hot_posts:
                pass
        except:
            return False

        return True

    async def get_hot_subreddit_submissions_with_media(
        self,
        sub_reddit: str,
        posts_limit: int,
    ) -> list:
        """Gets a list of subreddit pics

        Args:
            sub_reddit (str): subreddit to get pics from
            pics_limit (int): num of pics to charge
            num (int): num of pics to return

        Returns:
            list: containing reddit posts
        """

        subreddit = await self.reddit.subreddit(sub_reddit)
        hot_posts = subreddit.hot(limit=posts_limit)

        posts = []
        async for post in hot_posts:

            if ("jpg" in post.url or "png" in post.url) and not post.over_18:

                posts.append(post)
        # await reddit.close()
        return posts

    async def get_hot_pic_not_repeated(
        self,
        guild: nextcord.Guild,
        sub_reddit: str,
        record_type: str,
        nsfw: bool,
    ) -> nextcord.Embed:
        """Gets a list of subreddit pics

        Args:
            sub_reddit (str): subreddit to get pics from
            pics_limit (int): num of pics to charge
            num (int): num of pics to return

        Returns:
            list: containing reddit posts
        """

        subreddit = await self.reddit.subreddit(sub_reddit)
        hot_posts = subreddit.hot(limit=100)

        output = None
        posts = []
        async for post in hot_posts:

            if ("jpg" in post.url or "png" in post.url) and post.over_18 is nsfw:
                posts.append(post)

        for post in posts:
            
            if not self.db.record_exists(guild, post.url):
                self.db.insert_record(guild, record_type, post.url,sub_reddit)
                output = post
                break

        # Remove posts from db if they are not fetched
        posts_urls = [x.url for x in posts]
        self.db.clean_records(guild, record_type, posts_urls)
        if output is None:
            return None

        # await reddit.close()
        embed = self.create_embed(output)
        return embed

    def create_embed(
        self,
        post: asyncpraw.reddit.models.Submission,
    ) -> Embed:
        """Creates an embed from a reddit post

        Args:
            post (asyncpraw.models.Submission): post to create embed from

        Returns:
            Embed: embed created from post
        """
        link = "[Link](https://reddit.com{})".format(post.permalink)

        embed = Embed(
            title=post.title,
            description=link,
            color=Colour.from_rgb(255, 86, 0),
        )

        embed.set_author(
            name="r/" + post.subreddit.display_name,
            icon_url="https://www.redditinc.com/assets/images/site/reddit-logo.png",
        )

        embed.set_image(url=post.url)
        return embed
