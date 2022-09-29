import discord
import json
import math
from discord.ext import commands
import mysql.connector
from logs import DiscordLogs

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        mydb = mysql.connector.connect( host=config['aws']['host'], user=config['aws']['user'], passwd=config['aws']['password'], database=config['aws']['database'] )
        mycursor = mydb.cursor()
        mycursor.execute("INSERT INTO main_guilds (guild_id, guild_name, guild_icon_id, prefix, music_time_left) VALUES (%s, %s, %s,'-', 150)", (str(guild.id), str(guild.name), str(guild.icon)))
        mydb.commit()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        mydb = mysql.connector.connect( host=config['aws']['host'], user=config['aws']['user'], passwd=config['aws']['password'], database=config['aws']['database'] )
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM main_guilds WHERE guild_id=%s", (str(guild.id),))
        mydb.commit()

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

        elif isinstance(error, commands.MissingRequiredArgument):
            _message = "You are missing a required argument."
            embed.add_field(name=f'Missing Required Argument', value=_message)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BadArgument):
            _message = "You have provided an invalid argument."
            embed.add_field(name=f'Invalid Argument', value=_message)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandError):
            try:
                embed.add_field(name=error.message(), value=error)
                await ctx.send(embed=embed)
            except:
                raise error

        else:
            logger = DiscordLogs().logger
            logger.warning(error)

            # embed.add_field(name = f':x: Terminal Error', value = f"```{error}``` [Join the Support Server for Help](https://siffredi.altervista.org/redirect/support)", inline=False)
            # await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Events(bot))