import discord
import os
import asyncio
import json
import datetime
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands, tasks

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

td=datetime.datetime.now().date()
bd=datetime.date(2003,4,20)
age_years=int((td-bd).days /365.25)

class HelpCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def help(self, ctx):
        embed= discord.Embed(
            title='', 
            description= 
            f'Siffredi oltre a essere un porno-attore è un bot divertente creato interamente da una persona [IO](https://www.raulcarini.com); ho {age_years} anni, faccio una scuola di informatica ma qua di bot e python non si vedono neanche con un binocolo così mi sono dediacato allo studio tramite tutte le documentazioni di [python](https://www.python.org/doc/) e  [discord.py](https://discordpy.readthedocs.io/en/latest/index.html).\n'
            f'\n''**Commands**\n' 'Un elenco completo dei comandi è disponibile [qui](http://siffredi.vpsgh.it/commands).\n' 'Al momento però il sito web non è ancora attivo.\n'
            f'\n''**Add to Discord**\n''Siffredi Bot può essere aggiunto a tutti i server che desideri! \n' '[Clicca qui per aggiungerlo al tuo](https://bit.ly/2CvbI33).\n'
            f'\n''**Premium**\n''Attualmente non attivo nessun servizio premium ma in futuro potrà essere attuato un servizio a pagamento.\n'
            f'\n''**Support**\n''[Fai clic qui](http://siffredi.vpsgh.it/support) per parlare con il supporto se hai problemi o hai domande.\n',
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        embed.set_author(name='Siffredi Bot',icon_url='https://cdn.discordapp.com/attachments/691220858638827523/746134348427690074/magik.png')
        await ctx.send(embed=embed)

    @help.command()
    async def prefix(self, ctx):
        embed = discord.Embed(
            title = 'Prefix',
            description = 'Change the bot prefix on your server'
        )
        embed.add_field(name = '**Syntax**', value = '`prefix [simbol e.g. !]`')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCog(bot))