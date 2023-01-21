import discord
from discord.ext import commands
import json
from discord.ext.commands.cooldowns import BucketType

from cogs.music import embed

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.cooldown(2,60,BucketType.user) 
    @commands.hybrid_command(name="poll", usage="-poll {title} [description]")
    async def poll(self, ctx, title:str, description:str = None):
        """You can create a poll"""
        embed= discord.Embed(
            title=title,
            description= description,
            colour= discord.Color.purple()
        )
        message = await ctx.send(embed = embed)
        await message.add_reaction('👍')
        await message.add_reaction('👎')

async def setup(bot):
    await bot.add_cog(Poll(bot))
