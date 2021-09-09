from discord.ext import commands
from functions import get_reddit_image


class Animal(commands.Cog):
    """Fotos de animalitos"""

    def __init__(self, bot):
        self.bot = bot

    awa = {"a", "b", "b", "c"}

    @commands.command()
    async def fox(self, context):
        """Fotos de zorros hermosos -/////-

        Envia una foto de r/foxes
        """
        message = await context.channel.send("Buscando fotos de zorros hermosos")
        await context.channel.send(get_reddit_image("foxes", "Pics!", None))
        await message.delete()

    @commands.command()
    async def wolf(self, context):
        """Fotos de lobos lobitos lobones

        Envia una foto de r/wolves
        """
        message = await context.channel.send("Buscando fotos de lobos lobitos lobones")
        await context.channel.send(get_reddit_image("wolves", "Pics", None))
        await message.delete()

    @commands.command()
    async def fish(self, context):
        """Fotos de pescaitos

        Envia una foto de r/fish
        """
        message = await context.channel.send("Buscando fotos de pescaitos")
        await context.channel.send(get_reddit_image("fish", "Pic", None))
        await message.delete()

    @commands.command()
    async def reptile(self, context):
        """Fotos de lagartos y reptiles

        Envia una foto de r/reptiles
        """
        message = await context.channel.send("Buscando fotos de lagartos y reptiles")
        await context.channel.send(
            get_reddit_image(
                "reptiles",
                Flair=None,
                Filter="is_self:0 NOT site:(500px.com OR abload.de OR deviantart.com OR deviantart.net OR fav.me OR fbcdn.net OR flickr.com OR forgifs.com OR giphy.com OR gfycat.com OR gifsoup.com OR gyazo.com OR imageshack.us OR imgclean.com OR imgur.com OR instagr.am OR instagram.com OR mediacru.sh OR media.tumblr.com OR min.us OR minus.com OR myimghost.com OR photobucket.com OR picsarus.com OR puu.sh OR staticflickr.com OR tinypic.com OR twitpic.com)",
            )
        )
        await message.delete()

    @commands.command()
    async def amphibian(self, context):
        """Fotos de ranas y anfibios monísimos

        Envia una foto de r/Amphibians
        """
        message = await context.channel.send(
            "Buscando fotos de ranas y anfibios monísimos"
        )
        await context.channel.send(
            get_reddit_image(
                "Amphibians",
                Flair=None,
                Filter="is_self:0 NOT site:(500px.com OR abload.de OR deviantart.com OR deviantart.net OR fav.me OR fbcdn.net OR flickr.com OR forgifs.com OR giphy.com OR gfycat.com OR gifsoup.com OR gyazo.com OR imageshack.us OR imgclean.com OR imgur.com OR instagr.am OR instagram.com OR mediacru.sh OR media.tumblr.com OR min.us OR minus.com OR myimghost.com OR photobucket.com OR picsarus.com OR puu.sh OR staticflickr.com OR tinypic.com OR twitpic.com)",
            )
        )
        await message.delete()

    @commands.command()
    async def bird(self, context):
        """Fotos de pajaros

        Envia una foto de r/birds
        """
        message = await context.channel.send("Buscando fotos de pajaros")
        await context.channel.send(
            get_reddit_image(
                "birds",
                Flair=None,
                Filter="is_self:0 NOT site:(500px.com OR abload.de OR deviantart.com OR deviantart.net OR fav.me OR fbcdn.net OR flickr.com OR forgifs.com OR giphy.com OR gfycat.com OR gifsoup.com OR gyazo.com OR imageshack.us OR imgclean.com OR imgur.com OR instagr.am OR instagram.com OR mediacru.sh OR media.tumblr.com OR min.us OR minus.com OR myimghost.com OR photobucket.com OR picsarus.com OR puu.sh OR staticflickr.com OR tinypic.com OR twitpic.com)",
            )
        )
        await message.delete()


def setup(bot):
    bot.add_cog(Animal(bot))
