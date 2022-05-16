import discord
import json
from bs4 import BeautifulSoup
import requests

import random
import string
from forex_python.converter import CurrencyRates

from discord.ext import commands

import time
from discord.ext.commands.cooldowns import BucketType

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)


class Utilities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(2,60,BucketType.user) 
    @commands.command(name="support", usage="-support")
    async def support(self, ctx):
        """You can join my server for help"""
        embed= discord.Embed(
            title='Join into my server for help', 
            description= f' :arrow_forward: http://siffrdi.vpsgh.it/support', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.cooldown(2,60,BucketType.user) 
    @commands.command(name="invite", usage="-invite")
    async def invite(self, ctx):
        """You can get the link to add the bot to your server"""
        embed= discord.Embed(
            title='This is the link to invite me to your server', 
            description= f' :arrow_forward: https://bit.ly/2CvbI33', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.cooldown(2,60,BucketType.user) 
    @commands.command(name="donation", usage="-donation")
    async def donation(self, ctx):
        """Receive the link to be able to donate to support the progress of the bot"""
        embed= discord.Embed(
            title='Do you want to support the progress of the bot?', 
            description= ':arrow_forward: [Make a donation](https://www.paypal.com/donate?hosted_button_id=C2894CD24MW82) :arrow_backward:',
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.cooldown(2,60,BucketType.user) 
    @commands.command(name="ping", usage="-ping")
    async def ping(self, ctx):
        """You can see the api ping and the bot server ping"""
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()
        await ctx.channel.purge(limit=1)
        embed= discord.Embed( 
            title='This is my ping', 
            description= f":hourglass: {round(self.bot.latency * 1000)}ms\n\n:stopwatch: {round((end_time - start_time) * 1000)}ms ", 
            colour= discord.Color.purple() 
            ) 
        embed.set_footer(text=config["siffredi_footer"]) 
        await ctx.send(embed=embed)

    @commands.command(name='weather', aliases=['wth'], usage="-weather [city]")
    async def weather(self, ctx, city: str):
        """You can view the weather of the city you want"""
        city=city + " weather"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        city=city.replace(" ","+")

        res = requests.get(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')   

        location = soup.select('#wob_loc')[0].getText().strip()  
        time = soup.select('#wob_dts')[0].getText().strip()       
        info = soup.select('#wob_dc')[0].getText().strip() 
        weather = soup.select('#wob_tm')[0].getText().strip()
        rainfall = soup.select('#wob_pp')[0].getText().strip()
        humidity = soup.select('#wob_hm')[0].getText().strip()
        wind = soup.select('#wob_ws')[0].getText().strip()

        embed= discord.Embed(
                title='Siffredi Weather', 
                description= f'', 
                colour= discord.Color.purple()
            )
        embed.add_field(name='Location', value=location)
        embed.add_field(name='Time', value=time)
        embed.add_field(name='Info', value=info)
        embed.add_field(name='Weather', value=weather+"°C")
        embed.add_field(name='Precipitazioni', value=rainfall)
        embed.add_field(name='Umidità', value=humidity)
        embed.add_field(name='Vento', value=wind)
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.command(name="password", usage="-password [lenght]", aliases=['psw'])
    async def password(self, ctx, length: int):
        """You can generate a password of the length you want"""
        result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
        embed= discord.Embed(
                title='Random Gen Password', 
                description= f':arrow_right: {result_str}', 
                colour= discord.Color.purple()
            )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.command(name="dice", usage="-dice")
    async def dice(self, ctx):
        """Generates a number between 1 and 6"""
        num = random.randint(1,6)
        embed= discord.Embed(
                title='Dice Roll Simulator', 
                description= f':arrow_right: {num}', 
                colour= discord.Color.purple()
            )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.command(name="convert", usage="-convert [from currency] [to currency]", aliases=['cc','currency'])
    async def convert(self, ctx, amount: int, from_currency: str, to_currency: str):
        """You can convert one currency to another"""
        c = CurrencyRates()
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        result = c.convert(from_currency, to_currency, amount)
        embed= discord.Embed(
                title='Currency Converter', 
                description= f'{from_currency} {amount} \n:arrow_down: :arrow_down: :arrow_down:\n  {to_currency} {round(result, 2)}', 
                colour= discord.Color.purple()
            )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utilities(bot))