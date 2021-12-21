import discord
from discord import channel
from discord.ext import commands
from discord.utils import get
import json
from ftplib import FTP

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
        print(cog)
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

    @commands.command(name="sid")
    @commands.is_owner()
    async def server_id(self, ctx):
        for guild in self.bot.guilds:
            embed = discord.Embed(
                title = '',
                description = f"Server Name = **{guild.name}**\n Server Id = **{guild.id}**",
            )
            await ctx.send(embed= embed)

    @commands.command(name='data')
    @commands.is_owner()
    async def data(self, ctx):
        guilds = self.bot.guilds
        members = 0
        channel = 0
        for guild in guilds:
            members += guild.member_count
            channel += len(guild.text_channels)

        with open("data.json", 'r') as f:
                data = json.load(f)

        data = {"servers":  len(guilds), "users": members, "channels": channel}

        with open('data.json', 'w') as f:
            json.dump(data, f,indent=4)

        message = await ctx.send("`Generated File`")

        ftp = FTP(host=config["ftp-host"], encoding='latin-1')
        ftp.login(user=config["ftp-user"], passwd=config["ftp-pass"]) 
        ftp.cwd('assets/json')
        with open('data.json', 'rb') as fp:
            ftp.storbinary('STOR data.json', fp)
        await message.edit("`Uploaded File`")
        ftp.quit()

    @commands.command(name='commands')
    @commands.is_owner()
    async def commands(self, ctx):

        commands_name = []
        commands_help = []
        commands_aliases = []
        commands_cog_name = []
        commands_usage = []
        commands_perm = []

        for cmd in self.bot.commands:
            commands_name.append(cmd.name)
            commands_help.append(cmd.help)
            commands_aliases.append(cmd.aliases)
            commands_cog_name.append(cmd.cog_name)
            commands_usage.append(cmd.usage)
            commands_perm.append(cmd.brief)

        # commands_name.sort()

        with open("commands.json", 'r') as f:
            commands_ = json.load(f)

        commands_ = {"name":  commands_name, "description": commands_help, "syntax": commands_usage, "type" : commands_cog_name, "aliases" : commands_aliases}

        with open('commands.json', 'w') as f:
            json.dump(commands_, f,indent=4)

        message = await ctx.send("`Generated File`")

        ftp = FTP(host=config["ftp-host"], encoding='latin-1')
        ftp.login(user=config["ftp-user"], passwd=config["ftp-pass"]) 
        ftp.cwd('assets/json')
        with open('commands.json', 'rb') as fp:
            ftp.storbinary('STOR commands.json', fp)
        await message.edit("`Uploaded File`")
        ftp.quit()

def setup(bot):
    bot.add_cog(Owner(bot))
