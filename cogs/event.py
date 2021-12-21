import discord
import json
import math
import youtube_dl
from discord.ext import commands, tasks

import logging
import sys

from logs import DiscordLogs

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("prefixes.json", 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = '-'

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f ,indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f ,indent=4)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = discord.Embed(
        title='',
        color=discord.Color.red())
        if isinstance(error, commands.CommandNotFound):
            pass

        elif isinstance(error, commands.DisabledCommand):
            embed.add_field(name='Disabled Command', value='This command has been disabled')
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
            embed.add_field(name=f'Invalid Bot Permissions', value=_message)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
            embed.add_field(name=f'Invalid Permissions', value=_message)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandOnCooldown):
            _message = "This command is on cooldown, please retry in {}s.".format(math.ceil(error.retry_after))
            embed.add_field(name=f'Take it easy', value=_message)
            await ctx.send(embed=embed)

        else:
            logger = DiscordLogs().logger
            logger.warning(error)

            embed.add_field(name = f':x: Terminal Error', value = f"```{error}``` [Join the Support Server for Help](https://siffredi.altervista.org/redirect/support)", inline=False)
            await ctx.send(embed = embed)
            # raise error
        

def setup(bot):
    bot.add_cog(Events(bot))