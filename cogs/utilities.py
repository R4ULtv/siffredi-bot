import discord
import json
import random
import string
import typing
from forex_python.converter import CurrencyRates
import time
import urllib.request, json 
from datetime import datetime, timezone

from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands
import requests

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

class Utilities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(2,60,BucketType.user) 
    @commands.hybrid_command(name="support", usage="-support")
    async def support(self, ctx):
        """You can join my server for help"""
        embed= discord.Embed(
            title='Join into my server for help', 
            description= f' :arrow_forward: https://siffredi.altervista.org/redirect/support', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.cooldown(2,60,BucketType.user) 
    @commands.hybrid_command(name="invite", usage="-invite")
    async def invite(self, ctx):
        """You can get the link to add the bot to your server"""
        embed= discord.Embed(
            title='This is the link to invite me to your server', 
            description= f' :arrow_forward: [discord.com/siffredi-bot](https://discord.com/api/oauth2/authorize?client_id=744249413202870353&permissions=8&scope=bot%20applications.commands)', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.cooldown(2,60,BucketType.user) 
    @commands.hybrid_command(name="donation", usage="-donation")
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
    @commands.hybrid_command(name="ping", usage="-ping")
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

    @commands.cooldown(2,60,BucketType.user) 
    @commands.hybrid_command(name='weather', aliases=['wth'], usage="-weather [city]")
    async def weather(self, ctx, city:str):
        """You can view the weather of the city you want"""
        with urllib.request.urlopen(f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={config["owak"]}') as url:
            data = json.loads(url.read().decode())
        embed= discord.Embed(colour= discord.Color.purple())
        embed.set_author(name="OpenWeatherMap", url="https://openweathermap.org/")
        embed.set_thumbnail(url=f'https://openweathermap.org/img/w/{data["weather"][0]["icon"]}.png')
        embed.add_field(name='Location', value=data['name'] + ', ' + data['sys']['country'])
        embed.add_field(name="Time", value=datetime.fromtimestamp(data['dt'], tz=timezone.utc).strftime('%H:%M:%S') + " UTC")
        embed.add_field(name='Weather', value=data['weather'][0]['main'] + ": " + data['weather'][0]['description'])
        embed.add_field(name='Temperature', value=str(int(data['main']['temp'])) + "°C")
        embed.add_field(name='Pressure', value=str(data['main']['pressure']) + " hPa")
        embed.add_field(name='Humidity', value=str(data['main']['humidity']) + "%")
        embed.add_field(name='Wind', value=str(data['wind']['speed']) + " m/s")
        embed.add_field(name='Visibility', value=str(data['visibility']) + " m")
        embed.add_field(name='Coordinates', value=str(data['coord']['lat']) + "°N" + " " + str(data['coord']['lon']) + "°E")
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.cooldown(2,60,BucketType.user) 
    @commands.hybrid_command(name="password", usage="-password [lenght]", aliases=['psw'])
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

    @commands.cooldown(2,60,BucketType.user) 
    @commands.hybrid_command(name="dice", usage="-dice")
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

    @commands.cooldown(3,30,BucketType.user)
    @commands.hybrid_command(name="flip", aliases=['f'], usage="-flip")
    async def flip(self, ctx):
        """Flip a coin"""
        list = ['heads', 'tails']
        rand = list[random.randint(0,1)]
        embed = discord.Embed(title='', description= f'{rand}', colour= discord.Color.purple())
        await ctx.send(embed=embed)

    @commands.cooldown(2,60,BucketType.user) 
    @commands.hybrid_command(name="convert", usage="-convert [from currency] [to currency]", aliases=['cc','currency'])
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

    @commands.cooldown(2,60,BucketType.user)
    @commands.hybrid_command(name="apod", usage="-apod")
    async def apod(self, ctx):
        """Astronomy Picture of the Day"""
        with urllib.request.urlopen(f'https://api.nasa.gov/planetary/apod?api_key={config["nasa_api"]}') as url:
            space = json.loads(url.read().decode())
        embed= discord.Embed(
                title='Space Facts',
                description= f'{space["title"]}\n\n{space["explanation"]}',
                colour= discord.Color.purple()
            )
        embed.add_field(name='Date', value=space['date'])
        try:
            embed.add_field(name='Copyright', value=space['copyright'])
        except:
            pass

        try:
            embed.set_image(url=space['hdurl'])
        except:
            embed.set_image(url=space['url'])

        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.cooldown(1,150,BucketType.user)
    @commands.hybrid_command(name="tinyurl", usage="-tinyurl [url]" , aliases=['url'])
    async def tinyurl(self, ctx, url: str):
        """Shorten your url"""
        request = requests.get(f'http://tinyurl.com/api-create.php?url={url}')
        if request.text == "Error":
            embed = discord.Embed(
                title='Error',
                description= f'{ctx.author.mention}, I could not shorten your url. Please make sure you have a valid url.',
                colour= discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            embed= discord.Embed(
                title='Shorten URL',
                description= f'{request.text}',
                colour= discord.Color.purple()
            )
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.cooldown(2,30,BucketType.user)
    @commands.hybrid_command(name="version", usage="-version [version]", aliases=['ver', 'whatsnew'])
    async def version(self, ctx, version: typing.Literal["3.0", "2.2", "2.1", "2.0"]):
        """Show what's new about Siffredi Bot"""

        with open('version.json') as config_file:
            versions = json.load(config_file)

        for v in versions:
            if v['name'] == version:
                embed=discord.Embed(
                    title='What\'s New ?',
                    description= f'The main news are listed below, to see all the news look [here]({v["project_url"]}).\n Current Version: **3.0** - Next Version: **3.1**\n\n News about Version {v["name"]}: \n',
                    colour= discord.Color.purple()
                )
                for fiedl in v["fiedls"]:
                    embed.add_field(name=fiedl["name"], value=fiedl["value"], inline=False)
                embed.set_image(url=v["image_url"])
                embed.set_footer(text=config["siffredi_footer"])
                return await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilities(bot))