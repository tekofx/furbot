import logging
import discord
from discord.ext import commands
import random
import praw

reddit = praw.Reddit(client_id='pK48pKmt7MTGtA',
                     client_secret='UrsuDb6JQqyrppNb1KA0ezTX5SqDrA',
                     user_agent='prawuwu')


class Animal(commands.Cog):
    """Fotos de animalitos """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fox(self, context):
        """Fotos de zorros hermosos -/////-

            Envia una foto de r/foxes
        """
        await context.channel.send("Buscando fotos de zorros hermosos")
        await context.channel.send(get_reddit_image('foxes', 'Pics!', None))

    @commands.command()
    async def wolf(self, context):
        """Fotos de lobos lobitos lobones

            Envia una foto de r/wolves
        """
        await context.channel.send("Buscando fotos de lobos lobitos lobones")
        await context.channel.send(get_reddit_image('wolves', 'Pics', None))

    @commands.command()
    async def fish(self, context):
        """Fotos de pescaitos

            Envia una foto de r/fish
        """
        await context.channel.send("Buscando fotos de pescaitos")
        await context.channel.send(get_reddit_image('fish', 'Pic', None))

    @commands.command()
    async def reptile(self, context):
        """Fotos de lagartos y reptiles

            Envia una foto de r/reptiles
        """
        await context.channel.send("Buscando fotos de lagartos y reptiles")
        await context.channel.send(get_reddit_image('reptiles', Flair=None,
                                                    Filter='is_self:0 NOT site:(500px.com OR abload.de OR deviantart.com OR deviantart.net OR fav.me OR fbcdn.net OR flickr.com OR forgifs.com OR giphy.com OR gfycat.com OR gifsoup.com OR gyazo.com OR imageshack.us OR imgclean.com OR imgur.com OR instagr.am OR instagram.com OR mediacru.sh OR media.tumblr.com OR min.us OR minus.com OR myimghost.com OR photobucket.com OR picsarus.com OR puu.sh OR staticflickr.com OR tinypic.com OR twitpic.com)'))

    @commands.command()
    async def amphibian(self, context):
        """Fotos de ranas y anfibios monísimos

            Envia una foto de r/Amphibians
        """
        await context.channel.send("Buscando fotos de ranas y anfibios monísimos")
        await context.channel.send(get_reddit_image('Amphibians', Flair=None,
                                                    Filter='is_self:0 NOT site:(500px.com OR abload.de OR deviantart.com OR deviantart.net OR fav.me OR fbcdn.net OR flickr.com OR forgifs.com OR giphy.com OR gfycat.com OR gifsoup.com OR gyazo.com OR imageshack.us OR imgclean.com OR imgur.com OR instagr.am OR instagram.com OR mediacru.sh OR media.tumblr.com OR min.us OR minus.com OR myimghost.com OR photobucket.com OR picsarus.com OR puu.sh OR staticflickr.com OR tinypic.com OR twitpic.com)'))

    @commands.command()
    async def bird(self, context):
        """Fotos de pajaros

            Envia una foto de r/birds
        """
        await context.channel.send("Buscando fotos de pajaros")
        await context.channel.send(get_reddit_image('birds', Flair=None,
                                                    Filter='is_self:0 NOT site:(500px.com OR abload.de OR deviantart.com OR deviantart.net OR fav.me OR fbcdn.net OR flickr.com OR forgifs.com OR giphy.com OR gfycat.com OR gifsoup.com OR gyazo.com OR imageshack.us OR imgclean.com OR imgur.com OR instagr.am OR instagram.com OR mediacru.sh OR media.tumblr.com OR min.us OR minus.com OR myimghost.com OR photobucket.com OR picsarus.com OR puu.sh OR staticflickr.com OR tinypic.com OR twitpic.com)'))

    @commands.command()
    async def dankmeme(self,context):
        await context.channel.send("buscando dank meme")
        await context.channel.send(get_reddit_image('dankmemes', Flair=None,
                                                    Filter='is_self:0 NOT site:(500px.com OR abload.de OR deviantart.com OR deviantart.net OR fav.me OR fbcdn.net OR flickr.com OR forgifs.com OR giphy.com OR gfycat.com OR gifsoup.com OR gyazo.com OR imageshack.us OR imgclean.com OR imgur.com OR instagr.am OR instagram.com OR mediacru.sh OR media.tumblr.com OR min.us OR minus.com OR myimghost.com OR photobucket.com OR picsarus.com OR puu.sh OR staticflickr.com OR tinypic.com OR twitpic.com)'))

def get_reddit_image(Subreddit: str, Flair: str, Filter: str):
    """Gets a random Reddit image

    Args:
        Subreddit (str): [subreddit to get the photo from]
        Flair (str): [flair to filter by]
        Filter (str): [filter to search by]

    Returns:
        [str]: [url from a reddit image]
    """
    try:
        var = True
        while var:
            if Flair == None:
                memes_submissions = reddit.subreddit(Subreddit).search(
                    Filter)  # Gets a random images from r/foxes with flair Pics!
            else:
                memes_submissions = reddit.subreddit(Subreddit).search(
                    'Flair:' + Flair)  # Gets a random images from r/foxes with flair Pics!
            post_to_pick = random.randint(1, 10)
            for i in range(0, post_to_pick):
                submission = next(x for x in memes_submissions if not x.stickied)
            if submission.url.endswith('jpg'):
                var = False
    except:
        logging.error("Error at getting images from reddit")

    return submission.url


def setup(bot):
    bot.add_cog(Animal(bot))
