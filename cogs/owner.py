import discord
from discord.ext import commands


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




def setup(bot):
    bot.add_cog(Owner(bot))
