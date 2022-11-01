from typing import Optional
import discord
import json
import datetime
from discord.utils import get
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

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

    @commands.cooldown(3,60,BucketType.user)
    @commands.hybrid_command(name='help', usage="-help Optional[command name]")
    async def help(self, ctx, commands: Optional[str]):
        """Yo you need Help with Help wtf"""
        if commands is None:
            embed= discord.Embed(
                title='', 
                description= 
                f'Besides being a porn actor, Siffredi is a funny bot created entirely by [me](https://www.instagram.com/lil.poop__/); I am {age_years} years old, I do a computer science school but here bots and python are not seen even with binoculars so I devoted myself to studying through all the documentation of [python](https://www.python.org/doc/) and [discord.py](https://discordpy.readthedocs.io/en/latest/index.html).\n'
                f'\n**Issues**\nIf you have any problems with the bot, report it [here](https://github.com/R4ULtv/siffredi-bot/issues).\n'
                f'\n**Commands**\nA complete list of commands is available [here](http://siffredi.altervista.org/commands/).\n'
                f'\n**Add to Discord**\nSiffredi Bot can be added to as many servers as you want, [Click here to add it to yours](https://siffredi.altervista.org/redirect/invite).\n'
                f'\n**Premium**\nCurrently no premium service is active but in the future a paid service may be implemented.\n'
                f'\n**Support**\n[Click here](https://siffredi.altervista.org/redirect/support) to speak to support if you have any problems or questions.\n',
                colour= discord.Color.purple()
            )
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)
        else:
            if(command := get(self.bot.commands, name=commands)):
                embed= discord.Embed(
                    title=f'{commands.upper()}', 
                    description=f'*{command.help}*\n\n**Usage**\n{command.usage}\n\n**Aliases**\n{command.aliases}',
                    colour= discord.Color.purple()
                )
                embed.set_footer(text=config["siffredi_footer"])
                await ctx.send(embed=embed)
            else:
                embed= discord.Embed(
                    title='',
                    description=f'The *{commands}* command does not exist.',
                    colour= discord.Color.red()
                )
                await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))