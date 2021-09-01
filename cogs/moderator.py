import discord
import os
import asyncio
import json
import time
import datetime
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands, tasks

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

td=datetime.datetime.now().date()
bd=datetime.date(2003,4,20)
age_years=int((td-bd).days /365.25)


class ModeratorCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(2,60,BucketType.user) 
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix):
        with open('data.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('data.json', 'w') as f:
            json.dump(prefixes, f ,indent=4)

        embed = discord.Embed(
            title= "The bot prefix has changed",
            description= f'The new one is: `{prefix}`',
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.cooldown(2,60,BucketType.user) 
    @commands.command()
    async def donation(self, ctx):
        embed= discord.Embed(
            title='Do you want to support the progress of the bot?', 
            description= ':arrow_forward: [Make a donation](https://www.paypal.com/donate?hosted_button_id=C2894CD24MW82) :arrow_backward:',
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.cooldown(2,60,BucketType.user) 
    @commands.command()
    async def ping(self, ctx):
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
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        embed= discord.Embed(
            title=':bangbang: Kick:', 
            description= f'{member.mention} has been kicked for {reason} ', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await member.kick(reason=reason)
        await member.send(f"You have been kicked from the server {ctx.guild.name} for: {reason}")
        await ctx.send(embed=embed)
        print (f'kick >> The command was successfully executed')

    @commands.cooldown(2,60,BucketType.user) 
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        embed= discord.Embed(
            title=':no_entry_sign: Ban:', 
            description= f'{member.mention} has been banned for {reason}', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await member.ban(reason=reason)
        await ctx.send(embed=embed)
        print (f'ban >> The command was successfully executed')

    @commands.cooldown(2,60,BucketType.user) 
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
        embed= discord.Embed(
            title=':peace: UnBan', 
            description= f'{user.name} has been unbanned from the server', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)
        return print (f'!unban >> The command was successfully executed')

    @commands.cooldown(2,60,BucketType.user) 
    @commands.command()
    async def invite(self, ctx):
        embed= discord.Embed(
            title='This is the link to invite me to your server', 
            description= f' :arrow_forward: https://bit.ly/2CvbI33', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.cooldown(2,60,BucketType.user) 
    @commands.command(aliases = ['cl'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        if amount < 500:
            await ctx.channel.purge(limit=amount+1)
        else:
            await ctx.send("too many numbers I can't do it, Max 500")

    @commands.cooldown(2,60,BucketType.user) 
    @commands.command()
    async def support(self, ctx):
        embed= discord.Embed(
            title='Join into my server for help', 
            description= f' :arrow_forward: http://siffrdi.vpsgh.it/support', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.cooldown(2,60,BucketType.user) 
    @commands.command(aliases = ['is'])
    @commands.has_permissions(administrator=True)
    async def infoserver(self, ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)
        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)

        embed = discord.Embed(
            title=name + "",
            description=description,
            colour= discord.Color.purple()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)
        
    @commands.cooldown(2,60,BucketType.user) 
    @commands.command()
    async def ticket(self, ctx , *, arg):
        embed= discord.Embed(
            title='Richiesta Ticket', 
            description= f' :arrow_forward: {arg} \n by [<@{ctx.author.id}>]', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ModeratorCog(bot))