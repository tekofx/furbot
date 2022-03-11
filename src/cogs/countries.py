import random
from nextcord.ext import commands
from utils.bot import Bot
import requests
import nextcord
import asyncio


class countries(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def bandera(self, ctx: commands.Context):
        """Intenta adivinar la bandera del país"""

        def check(msg=nextcord.Message) -> bool:
            return msg.author == ctx.author and msg.channel == ctx.channel

        data = requests.get("https://restcountries.com/v3.1/all").json()
        country = random.choice(data)
        name = country["translations"]["spa"]["common"]
        flag = country["flags"]["png"]

        embed = nextcord.Embed(title="Adivina la bandera")
        embed.set_image(url=flag)

        await ctx.send(embed=embed)
        try:
            message = await self.bot.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Tiempo agotado")
            return

        if message.content.lower() in name.lower():
            await ctx.send("Correcto")


def setup(bot: commands.Bot):
    bot.add_cog(countries(bot))
