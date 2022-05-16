from typing import Optional
import discord
import json
import datetime
from discord.utils import get
from discord.ext import commands

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

# YEARS (my birthday)
td=datetime.datetime.now().date()
bd=datetime.date(2003,4,20)
age_years=int((td-bd).days /365.25)

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', usage="-help Optional[command name]")
    async def help(self, ctx, cmd: Optional[str]):
        """Yo you need Help with Help wtf"""
        if cmd is None:
            embed= discord.Embed(
                title='', 
                description= 
                f'Siffredi oltre a essere un porno-attore è un bot divertente creato interamente da una persona [IO](https://www.raulcarini.com); ho {age_years} anni, faccio una scuola di informatica ma qua di bot e python non si vedono neanche con un binocolo così mi sono dediacato allo studio tramite tutte le documentazioni di [python](https://www.python.org/doc/) e  [discord.py](https://discordpy.readthedocs.io/en/latest/index.html).\n'
                f'\n''**Commands**\n' 'Un elenco completo dei comandi è disponibile [qui](http://siffredi.altervista.org/commands/).\n'
                f'\n''**Add to Discord**\n''Siffredi Bot può essere aggiunto a tutti i server che desideri! \n' '[Clicca qui per aggiungerlo al tuo](https://siffredi.altervista.org/redirect/invite).\n'
                f'\n''**Premium**\n''Attualmente non attivo nessun servizio premium ma in futuro potrà essere attuato un servizio a pagamento.\n'
                f'\n''**Support**\n''[Fai clic qui](https://siffredi.altervista.org/redirect/support) per parlare con il supporto se hai problemi o hai domande.\n',
                colour= discord.Color.purple()
            )
            embed.set_footer(text=config["siffredi_footer"])
            embed.set_author(name='Siffredi Bot',icon_url='https://cdn.discordapp.com/attachments/691220858638827523/746134348427690074/magik.png')
            await ctx.send(embed=embed)
        else:
            if(command := get(self.bot.commands, name=cmd)):
                embed= discord.Embed(
                    title=f'{cmd.upper()}', 
                    description=f'*{command.help}*',
                    colour= discord.Color.purple()
                )
                embed.set_footer(text=config["siffredi_footer"])
                await ctx.send(embed=embed)
            else:
                await ctx.send('That command does not exist.')


def setup(bot):
    bot.add_cog(Help(bot))