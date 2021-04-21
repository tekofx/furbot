import logging

import discord
from discord.ext import commands
import asyncio
import random
from cogs.functions import get_user_role, get_user_roles, get_user, get_user_avatar
import wget

memeTemplatesPath = "memes_templates/"


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


    @commands.command()
    async def carnet(self,context, *,user : discord.Member=None):
        """Muestra tu carnet como miembro de Villa Furrense
        """
        logging.info(str(context.author)+" used command carnet")

        rangos=['Furrense recién llegado','Furrense Nuevo', 'Furrense Viejo', 'Furrense Veterano','Furrense de Oro', 'Furrense VIP']
        usr=get_user(context, user)
        name=usr.display_name
        rango=get_user_role(usr, rangos)
        roles=get_user_roles(usr, rangos)
        fecha=str(usr.joined_at)
        fecha=fecha.split()
        
        embed=discord.Embed(title="Carnet Villafurrense", color=0x0f8af5)
        embed.set_author(name=usr, icon_url=usr.avatar_url)
        embed.set_thumbnail(url=usr.avatar_url)
        embed.add_field(name="Nombre", value=name, inline=False)
        embed.add_field(name="Fecha de entrada", value=fecha[0], inline=False)
        embed.add_field(name="Rango", value=rango, inline=False)
        embed.add_field(name="Roles", value=roles, inline=False)
        await context.channel.send(embed=embed)

    # FIXME: No funciona el comando
    @commands.command()
    async def uwu(self,context, *,user : discord.Member=None):
        if user==None:
            wget.download(context.author.avatar_url, memeTemplatesPath + '01.webp')
            os.system('rm wget-log*')
            print('a')
            await context.channel.send(file=discord.File(memeTemplatesPath + "01.webp"))
        else:
            wget.download(user.avatar_url, memeTemplatesPath + '01.webp')
            await context.channel.send(file=discord.File(memeTemplatesPath + "01.webp"))

        print('s')



def setup(bot):
    bot.add_cog(utilities(bot))