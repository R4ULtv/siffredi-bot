import discord
import json
from discord.ext import commands
from random import randint
from discord.ext.commands.cooldowns import BucketType

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(3,60,BucketType.user)
    @commands.command(name="rockpaperscissors", aliases=['rps'], usage="-rockpaperscissors [choice]")
    async def rock_paper_scissors(self, ctx, choice):
        """Play rock paper scissors"""
        list = ['rock', 'paper', 'scissors']
        rand = list[randint(0,2)]
        answer = ""
        if choice == rand:
            answer = '**tie** :man_shrugging:'
        elif choice == 'rock': 
            if rand == "paper":
                answer = "**You lost** :man_shrugging: \n\n:roll_of_" + rand + ": ***covers*** :" + choice + ":"
            else:
                answer = "**You won** :trophy: \n\n:" + choice + ": ***smashes*** :" + rand + ":"
        elif choice == "paper":
            if rand == "scissors":
                answer = "**You lost** :man_shrugging: \n\n:" + rand + ": ***cuts*** :roll_of_" + choice + ":"
            else:
                answer = "**You won** :trophy: \n\n:roll_of_" + choice + ": ***covers*** :" + rand + ":"
        elif choice == "scissors":
            if rand == "paper":
                answer = "**You won** :trophy: \n\n:" + choice + ": ***cuts*** :roll_of_" +  rand + ":"
            else:
                answer = "**You lost** :man_shrugging: \n\n:" + rand + ": ***smashes*** :" + choice + ":"
        else:
            answer = "Invalid input. Check what you write."

        embed = discord.Embed(title='', description= f'{answer}', colour= discord.Color.purple())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Games(bot))