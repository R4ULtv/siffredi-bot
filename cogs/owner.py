from ast import alias
import discord
from discord.ext import commands
import json
import mysql.connector

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="load", hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("**`ERROR:`**")
        else:
            await ctx.send("**`SUCCESS`**")

    @commands.command(name="unload", hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send("**`ERROR:`**")
        else:
            await ctx.send("**`SUCCESS`**")

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("**`ERROR:`**")
        else:
            await ctx.send("**`SUCCESS`**")

    @commands.command(name="shards", hidden=True)
    @commands.is_owner()
    async def getShards(self, ctx):
        await ctx.send("Shards: " + str(self.bot.shard_count))

    @commands.command(name="sc", hidden=True)
    @commands.is_owner()
    async def server_count(self, ctx):
        embed = discord.Embed(
            title = '',
            description = "I'm in **" + str(len(self.bot.guilds)) + "** servers",
        )
        await ctx.send(embed= embed)    

    @commands.command(name="guilds", hidden=True)
    @commands.is_owner()
    async def guilds(self, ctx):
        mydb = mysql.connector.connect( host=config['aws']['host'], user=config['aws']['user'], passwd=config['aws']['password'], database=config['aws']['database'] )
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM main_guilds")
        guilds = self.bot.guilds
        for guild in guilds:
            mycursor.execute("INSERT INTO main_guilds (guild_id, guild_name, guild_icon_id, prefix, music_time_left) VALUES (%s, %s, %s, %s, %s)", (str(guild.id), str(guild.name), str(guild.icon), "-",150,))
            mydb.commit()
        mycursor.close()
        mydb.close()
        await ctx.send('Guilds updated.')
    
    @commands.command(name="cmds", hidden=True)
    @commands.is_owner()
    async def cmds(self, ctx):
        mydb = mysql.connector.connect( host=config['aws']['host'], user=config['aws']['user'], passwd=config['aws']['password'], database=config['aws']['database'] )
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM commands_command")

        id = 1
        for cmd in self.bot.commands:
            id += 1
            sql = "INSERT INTO commands_command (id, name, description, syntax, type, aliases) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (int(id), str(cmd.name), str(cmd.help), str(cmd.usage), str(cmd.cog_name), str(cmd.aliases))
            mycursor.execute(sql, val)
            mydb.commit()
        mycursor.close()
        mydb.close()
        await ctx.send('Commands updated.')

    @commands.command(name="announcement", aliases=['anc'],  hidden=True)
    @commands.is_owner()
    async def announcement(self, ctx, *, message):
        for guild in self.bot.guilds:
            embed = discord.Embed(
                title = 'Announcement',
                description = message,
                colour= discord.Color.purple()
            )
            embed.set_footer(text=config["siffredi_footer"])
            try:
                await guild.system_channel.send(embed=embed)
            except:
                pass

def setup(bot):
    bot.add_cog(Owner(bot))
