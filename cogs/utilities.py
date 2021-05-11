import logging
import discord
from discord.ext import commands
import asyncio
import random
from cogs.functions import *
import wget
import os
from cogs.functions import * 
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 



class utilities(commands.Cog):
    """Utilidades varias"""
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def random(self, context,min :int=None ,max : int=None , *, user : discord.Member=None):
        """ Genera un número aleatorio

            Uso: fur random                 ---> Genera un numero entre 1 y 100
                 fur random <min> <max>     ---> Genera un numero entre <min> y <max>
        """

        if min and max is not  None:
            num=str(random.randint(min,max))
        else:
            num=str(random.randint(0,100))
        tmp = await context.channel.send('Generando número aleatorio')

        await tmp.edit(content='Generando número aleatorio.')
        await asyncio.sleep(0.2)
        await tmp.edit(content='Generando número aleatorio..')
        await asyncio.sleep(0.2)
        await tmp.edit(content='Generando número aleatorio...')
        await asyncio.sleep(0.2)
        await tmp.edit(content='Generando número aleatorio....')
        await asyncio.sleep(0.2)
        await tmp.edit(content='Generando número aleatorio.....')
        await asyncio.sleep(0.2)
        await tmp.edit(content='Numero aletorio: '+num)


#     @commands.command()
    # async def carnet(self,context, *,user : discord.Member=None):
        # """Muestra tu carnet como miembro de Villa Furrense
        # """

        # # Get user info
        # usr=get_user(context, user)
        # name=usr.display_name
        # rango=get_user_ranks(usr)
        # roles=get_user_roles(usr)
        # fecha=str(usr.joined_at)
        # fecha=fecha.split()
        
        # # Add fields
        # embed=discord.Embed(title="Carnet Villafurrense", color=0x0f8af5)
        # embed.set_author(name=usr, icon_url=usr.avatar_url)
        # embed.set_thumbnail(url=usr.avatar_url)
        # embed.add_field(name="Nombre", value=name, inline=False)
        # embed.add_field(name="Fecha de entrada", value=fecha[0], inline=False)
        # embed.add_field(name="Rango", value=rango, inline=False)
        # embed.add_field(name="Roles", value=roles, inline=False)
        # await context.channel.send(embed=embed)


    @commands.command()
    async def carnet(self,context, *,user : discord.Member=None):
        """Muestra tu carnet como miembro de Villa Furrense
        """
        # Get user info
        usr=get_user(context, user)
        name=usr.display_name
        species=get_user_species(usr)
        rango=get_user_ranks(usr)
        print(species) 
        roles=get_user_roles(usr)
        fecha=str(usr.joined_at)
        fecha=fecha.split()


        var = "wget -O %s%s %s" % (memeTemplatesPath, '01'+".webp", usr.avatar_url)
        os.system(var)
        # get_user_avatar(usr,'01')
        convert_pic(memeTemplatesPath+'01.webp','01',300)
        user_avatar=memeTemplatesPath+'01.png'
        avatar=Image.open(user_avatar)

        # Open carnet to draw
        output = Image.open("carnet.png").convert("RGBA")
        draw = ImageDraw.Draw(output)
        font = ImageFont.truetype(memeTemplatesPath + "Calibri.ttf", 50)

        # Draw name
        draw.text(((420,260)),name,font=font,fill=(0,0,0,255))

        # Draw species
        draw.text(((420,384)),species,font=font,fill=(0,0,0,255))

        # Draw rank
        draw.text(((420,518)),rango,font=font,fill=(0,0,0,255))

        # Draw time in server
        draw.text(((420,642)),fecha[0],font=font,fill=(0,0,0,255))


        # Add avatar
        output.paste(avatar, (50,300))

        output.save(memeTemplatesPath+"output.png","PNG")
        await context.channel.send(file=discord.File(memeTemplatesPath+'output.png'))
        delete_files(('01.webp','output.png','01.png'))
    @commands.command()
    async def avatar(self,context, *,user : discord.Member=None):
        """Obtén la imagen de perfil de alguien"""

        avatar_url=get_user(context, user).avatar_url
        var="wget -O %s%s %s" % (memeTemplatesPath, "01.webp", avatar_url)
        os.system(var)
        convert_pic(memeTemplatesPath+'01.webp','01')
        await context.channel.send(file=discord.File(memeTemplatesPath+'01.png'))
        delete_files(('01.webp', '01.png'))


def setup(bot):
    bot.add_cog(utilities(bot))
