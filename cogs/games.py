import discord
import asyncio
from discord.ext import commands
import random
import urllib.request, json 
import json
import typing
from discord.ext.commands.cooldowns import BucketType

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(2,60,BucketType.user)
    @commands.hybrid_command(name="rockpaperscissors", aliases=['rps'], usage="-rockpaperscissors [choice]")
    async def rock_paper_scissors(self, ctx, choice: typing.Literal["Rock", "Paper", "Scissors"]):
        """Play rock paper scissors"""
        list = ['rock', 'paper', 'scissors']
        rand = list[random.randint(0,2)]
        answer = ""
        choice = choice.lower()
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

    @commands.cooldown(2,60,BucketType.user)
    @commands.hybrid_command(name="hangman", aliases=['hang'], usage="-hangman")
    async def hangman(self, ctx):
        """Play hangman"""
        with urllib.request.urlopen(f"https://api.wordnik.com/v4/words.json/randomWord?api_key={config['word_api']}") as url:
            word = json.loads(url.read().decode())
        word = word["word"]
        print(word)
        guesses = ""
        turns = 5
        while turns > 0:
            answer = "" 
            for char in word:
                if char in guesses:
                    answer += char
                else:
                    answer += '- '

            if word == answer:
                turns = 0
                await ctx.send(embed = discord.Embed(title='Hangman :man_standing:', description= f'You won! The word was: **{word}**', colour= discord.Color.purple()))
                return

            embed = discord.Embed(title='Hangman :man_standing:', description= f':arrow_right: {answer}', colour= discord.Color.purple())
            await ctx.send(embed=embed)
            try:
                guess = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                guesses += guess.content
            except asyncio.TimeoutError:
                await ctx.send(embed = discord.Embed(title='Hangman :man_standing:', description= f'You took too long. You lose.', colour= discord.Color.purple()))
                return

            if guess.content not in word:
                turns -= 1
                await ctx.send(embed = discord.Embed(title='Hangman :man_standing:', description= f'**{guess.content}** is not in the word. You have **{turns}** turns left.', colour= discord.Color.purple()))

        await ctx.send(embed = discord.Embed(title='Hangman :man_standing:', description= f'You lost! The word was: **{word}**', colour= discord.Color.purple()))
        
    @commands.cooldown(3,30,BucketType.user)
    @commands.hybrid_command(name="guess", aliases=['guessnumber'], usage="-guess [number]")
    async def guess(self, ctx, number:int):
        """Guess a number between 1 and 10"""
        if number == random.randint(1,10):
            answer = "You won!"
        else:
            answer = "You lost!"

        embed = discord.Embed(title='', description= f'{answer}', colour= discord.Color.purple())
        await ctx.send(embed=embed)

    @commands.cooldown(3,30,BucketType.user)
    @commands.hybrid_command(name="8ball", aliases=['8b'], usage="-8ball [question]")
    async def eight_ball(self, ctx, *, question):
        """Ask the 8ball a question"""
        list = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
        rand = list[random.randint(0,19)]

        embed = discord.Embed(title=f'{question}', description= f'{rand}', colour= discord.Color.purple())
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Games(bot))