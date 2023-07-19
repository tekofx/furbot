import io
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from pyrae import dle
from core.bot import Bot
import datetime
from geopy.geocoders import Nominatim
from ui.Button import Button
import requests
from staticmap import StaticMap, CircleMarker


emojis = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪", "🟫", "⬜"]

weathercodes = {
    0: {'text': 'Cielo despejado', 'emoji': '☀️'},
    1: {'text': 'Principalmente despejado', 'emoji': '🌤️'},
    2: {'text': 'Parcialmente nublado', 'emoji': '⛅'},
    3: {'text': 'Nublado', 'emoji': '☁️'},
    45: {'text': 'Niebla', 'emoji': '🌫️'},
    48: {'text': 'Escarcha depositada por la niebla', 'emoji': '🧊'},
    51: {'text': 'Llovizna: Intensidad ligera', 'emoji': '🌧️'},
    53: {'text': 'Llovizna: Intensidad moderada', 'emoji': '🌧️'},
    55: {'text': 'Llovizna: Intensidad densa', 'emoji': '🌧️'},
    56: {'text': 'Llovizna helada: Intensidad ligera', 'emoji': '🌧️'},
    57: {'text': 'Llovizna helada: Intensidad densa', 'emoji': '🌧️'},
    61: {'text': 'Lluvia: Intensidad ligera', 'emoji': '🌧️'},
    63: {'text':'Lluvia: Intensidad moderada','emoji':'🌧️'},
    65 :{'text':'Lluvia: Intensidad fuerte','emoji':'🌧️'},
    66 :{'text':'Lluvia helada: Intensidad ligera','emoji':'🌧️'},
    67 :{'text':'Lluvia helada: Intensidad fuerte','emoji':'🌧️'},
    71 :{'text':'Nieve ligera','emoji':'🌨️'},
    73 :{'text':'Nieve moderada','emoji':'🌨️'},
    75 :{'text':'Nieve fuerte','emoji':'🌨️'},
    77 :{'text':'Granizo','emoji':'🌨️🧊'},
    80 :{'text':'Chubascos de lluvia ligeros','emoji':'🌧️'},
    81 :{'text':'Chubascos de lluvia moderados','emoji':'🌧️'},
    82 :{'text':'Chubascos de lluvia violentos','emoji':'🌧️'},
    85 :{'text':'Chubascos de nieve ligeros','emoji':'🌨️'}, 
    86 :{'text':'Chubascos de nieve fuertes','emoji':'🌨️'}, 
    95 :{'text':'Tormenta eléctrica con lluvia','emoji':'⛈️'}, 
    96 :{'text':'Tormenta eléctrica con granizo','emoji':'⛈️'}, 
    99 :{'text':'Tormenta eléctrica con polvo','emoji':'⛈️'}
}





class Utils(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        
        
    @nextcord.slash_command(name="tiempo", guild_ids=[788479325787258961])
    async def tiempo(self,interaction:Interaction, ubicacion:str):
        """Obten el pronostico del tiempo para hoy

        Args:
            ubicacion (str): Ubicación de la que obtener el pronostico
        """        
        geolocator = Nominatim(user_agent="furbot")
        location = geolocator.geocode(ubicacion)

        params={
            "latitude":location.latitude,
            "longitude":location.longitude,
            "daily":"weathercode,apparent_temperature_max,apparent_temperature_min",
            "timezone":"Europe/London",
            "forecast_days":"1",
            "models":"ecmwf_ifs04"
        }
        var=requests.get("https://api.open-meteo.com/v1/forecast",params=params).json()
        daily=var["daily"]
        aparent_max_temp=daily["apparent_temperature_max"][0]
        aparent_min_temp=daily["apparent_temperature_min"][0]
        weather_code=daily["weathercode"][0]
        forecast=weathercodes[weather_code]["text"]
        forecast_emoji=weathercodes[weather_code]["emoji"]
        
        m = StaticMap(600, 600)

        marker = CircleMarker((location.longitude, location.latitude), 'red', 6)
        m.add_marker(marker)
        image = m.render(zoom=7)
        
        bytes_io = io.BytesIO()
        image.save(bytes_io, "PNG")
        bytes_io.seek(0)
        file=nextcord.File(bytes_io, "output.png")
        
        embed=nextcord.Embed(title=f"{ubicacion.capitalize()}",description=f"{forecast_emoji} {forecast} - {aparent_max_temp}ºC/{aparent_min_temp}ºC")
        embed.set_image(url="attachment://output.png")
        await interaction.send(embed=embed,file=file)    
        
        
    @nextcord.slash_command(name="avatar")
    async def avatar(self, interaction:Interaction, usuario:nextcord.Member):
        """Obtiene el avatar de un usuario

        Args:
            usuario (nextcord.Member): Usuario del que enviar el avatar
        """        
        await interaction.send(usuario.display_avatar.url)

    @nextcord.slash_command(name="ping")
    async def ping(self, interaction: Interaction):
        """Comprobar si el bot está online"""
        await interaction.send("Pim pam trucu trucu")
        
    @nextcord.slash_command(name="e621")
    async def e621(self, interaction:Interaction, tags:str):
        """Envia una imagen de e621 con los tags especificados.

        Args:
            tags (str): Tags de la imagen. Deben estar separados por espacios
        """
        if not interaction.channel.is_nsfw():
            await interaction.send("Este comando solo se puede usar en canales NSFW")
            return
        await self.send_e621_post(interaction,tags)
        
    async def send_e621_post(self,interaction:Interaction,tags:str):
        post=self.bot.e621.get_post_not_repeated(interaction.guild,tags)
        if post is None:
            await interaction.send("No se ha encontrado nada con esa/s tags. Comprueba que las tags existen")
            return
        button=Button()
        output=f"{post.tags}\n{post.file.url}"
        await interaction.send(output,view=button)
        await button.wait()
        if button.value is None:
            return
        if button.value:
            
            await self.send_e621_post(interaction,tags)
        
    @nextcord.slash_command(name="e926")
    async def e926(self, interaction:Interaction, tags:str):
        """Envia una imagen de e926 con los tags especificados.

        Args:
            tags (str): Tags de la imagen. Deben estar separados por espacios
        """
        await self.send_e926_post(interaction,tags)
    
            
    async def send_e926_post(self,interaction:Interaction,tags:str):
        post=self.bot.e926.get_post_not_repeated(interaction.guild,tags)
        if post is None:
            await interaction.send("No se ha encontrado nada con esa/s tags. Comprueba que las tags existen")
            return
        button=Button()
        output=f"{post.tags}\n{post.file.url}"
        await interaction.send(output,view=button)
        await button.wait()
        if button.value is None:
            return
        if button.value:
            await self.send_e926_post(interaction,tags)
        
        
    @nextcord.slash_command(name="avatar")
    async def avatar(self, interaction: Interaction, usuario: nextcord.Member):
        """Muestra el avatar de un usuario"""
        await interaction.send(usuario.display_avatar.url)
        
        
    @nextcord.slash_command(name="votacion")
    async def votacion(
        self,
        interaction: Interaction,
        titulo:str,
        descripcion:str,
        opciones: str
    ):
        """Crea una votacion

        Args:
            titulo (str): Titulo de la votación
            descripcion (str): Descripción de la votación
            opciones (str): Lista de opciones a votar. Separar por comas.
        """        
        embed=nextcord.Embed(title=titulo,description=descripcion)
        opciones=opciones.split(",")
        for x in opciones:
            i=opciones.index(x)
            embed.add_field(name=f"Opción {emojis[i]}",value=x)      
            
        msg=await interaction.response.send_message(embed=embed)
        msg=await msg.fetch()
        for x in opciones:
            i=opciones.index(x)
            await msg.add_reaction(emojis[i])

    @nextcord.slash_command(name="rae")
    async def rae(self, interaction: Interaction, palabra: str):
        """Define una palabra"""

        msg = await interaction.send("Buscando en la RAE")

        output = str(dle.search_by_word(palabra))

        if "«Diccionario de la lengua española»" in output:
            await msg.edit(content="Termino no encontrado")
        else:
            await msg.edit(content=output)

    @nextcord.slash_command(name="cumple")
    async def birthday(self, interaction: Interaction):
        pass

    @birthday.subcommand(name="añadir")
    async def birthday_add(
        self, interaction: Interaction, dia: int, mes: int, año: int
    ):
        """Añade tu cumpleaños al bot para que te felicite

        Args:
            dia (int): del 1 al 31
            mes (int): del 1 al 12
            año (int): numero de 4 digitos

        """

        birth_date = datetime.date(año, mes, dia)
        self.bot.db.set_user_birthday(interaction.user, birth_date)
        await interaction.send("Cumpleaños guardado en la base de datos")

    @birthday.subcommand(name="ver")
    async def birthday_get(self, interaction: Interaction, usuario: nextcord.Member):
        """Mira el cumpleaños de un usuario

        Args:
            usuario (nextcord.Member): Usuario del que ver el cumpleaños
        """

        user=self.bot.db.get_user(usuario)
        cumple=user[4]
        if not cumple:
            await interaction.send(
                f"No existe el cumpleaños de {usuario.display_name} en la base de datos"
            )
            return
        await interaction.send(
            f"El cumpleaños de {usuario.display_name} es el {cumple.day}-{cumple.month}-{cumple.year}"
        )
        
    


def setup(bot: commands.Bot):
    bot.add_cog(Utils(bot))


def get_weather(place:str):
    geolocator = Nominatim(user_agent="furbot")
    location = geolocator.geocode(place)

    params={
        "latitude":location.latitude,
        "longitude":location.longitude,
        "daily":"apparent_temperature_max,apparent_temperature_min",
        "timezone":"Europe/London",
        "forecast_days":"1",
        "models":"ecmwf_ifs04"
    }
    var=requests.get("https://api.open-meteo.com/v1/forecast",params=params).json()
    daily=var["daily"]
    aparent_max_temp=daily["apparent_temperature_max"][0]
    aparent_min_temp=daily["apparent_temperature_min"][0]