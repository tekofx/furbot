import random
from nextcord.ext import commands
from utils.bot import Bot
import requests
import nextcord
import asyncio
import unidecode
from nextcord import Interaction
import os

local_guild = os.getenv("LOCAL_GUILD")


class countries(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(
        guild_ids=[local_guild],
        name="pais",
        description="""Información sobre un país

        Args:
            nombre : nombre del pais
        """,
    )
    async def pais(self, interaction: Interaction, nombre: str):
        url = "https://restcountries.com/v3.1/name/{}".format(nombre.lower())

        data = requests.get(url)

        if data.status_code != 200:
            await interaction.send(
                "Error, no se encuentra el pais. Prueba el nombre en inglés"
            )
            return

        data = data.json()[0]
        embed = nextcord.Embed(title=data["name"]["common"])
        embed.set_image(url=data["flags"]["png"])
        embed.set_thumbnail(url=data["coatOfArms"]["png"])
        embed.add_field(name="Capital", value="".join(data["capital"]), inline=True)
        embed.add_field(name="Región", value=data["region"], inline=True)
        embed.add_field(name="Subregión", value=data["subregion"], inline=True)
        embed.add_field(name="Población", value=data["population"], inline=False)

        currencies = []
        for x in data["currencies"]:
            name = data["currencies"][x]["name"]
            symbol = data["currencies"][x]["symbol"]
            currencies += [name + " (" + symbol + ")"]
        embed.add_field(name="Moneda/s", value=",".join(currencies), inline=False)

        languages = []
        for x in data["languages"]:
            name = data["languages"][x]
            languages += [name]
        embed.add_field(name="Idioma/s", value=",".join(languages), inline=False)
        embed.add_field(
            name="Google Maps", value=data["maps"]["googleMaps"], inline=False
        )

        await interaction.send(embed=embed)

    @nextcord.slash_command(
        guild_ids=[local_guild],
        name="bandera",
        description="Intenta adivinar la bandera del país",
    )
    async def bandera(self, interaction: Interaction):
        """Intenta adivinar la bandera del país"""

        def check(msg=nextcord.Message) -> bool:
            return msg.author == interaction.user and msg.channel == interaction.channel

        data = requests.get("https://restcountries.com/v3.1/all").json()
        country = random.choice(data)

        name = country["translations"]["spa"]["common"]
        flag = country["flags"]["png"]
        capital = " ".join(country["capital"])
        region = country["region"]
        subregion = country["subregion"]
        google_maps = country["maps"]["googleMaps"]

        embed = nextcord.Embed(title="Adivina la bandera")
        embed.set_image(url=flag)

        await interaction.send(embed=embed)
        try:
            message = await self.bot.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await interaction.send("Tiempo agotado")
            await interaction.send(name)
            return

        if (
            unidecode.unidecode(message.content.lower())
            in unidecode.unidecode(name.lower())
            and len(message.content.lower()) > 2
        ):
            await interaction.send("Correcto")
        else:
            await interaction.send("Incorrecto: {}".format(name))

        embed = nextcord.Embed(title=name)
        embed.add_field(name="Capital", value=capital)
        embed.add_field(name="Región", value=region)
        embed.add_field(name="Subregión", value=subregion)
        embed.add_field(name="Google Maps", value=google_maps)
        embed.set_image(url=flag)
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(countries(bot))
