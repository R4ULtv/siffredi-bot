import json
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class StrawPoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(2,60,BucketType.user) 
    @commands.hybrid_command(name="strawpoll", usage="-strawpoll title option1 option2")
    async def strawpoll(self, ctx, title:str, option1="Yes", option2="No", option3=None, option4=None):
        """You can create a strawpoll"""
        async with self.bot.http_session.post(
            "https://api.strawpoll.com/v3/polls",
            json={
                "title": title,
                "poll_options": [
                    {
                        "value": option1
                    },
                    {
                        "value": option2
                    },
                    {
                        "value": option3
                    },
                    {
                        "value": option4
                    }
                ]
            }
        ) as req:
            res = await req.json()
            await ctx.send("https://strawpoll.com/" + str(res["id"]))

async def setup(bot):
    await bot.add_cog(StrawPoll(bot))
