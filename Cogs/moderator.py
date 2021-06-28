import discord
import os
import asyncio

from discord.ext import commands, tasks

OWNERID = 495542366598594560

class ModeratorCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed= discord.Embed(
            title='', 
            description= 
            'Siffredi oltre a essere un porno-attore è un bot divertente creato interamente da una persona [IO](https://www.instagram.com/lil.poop__); ho 17 anni, faccio una scuola di informatica ma qua di bot e python non si vedono neanche con un binocolo così mi sono dediacato allo studio tramite tutte le documentazioni di [python](https://www.python.org/doc/) e  [discord.py](https://discordpy.readthedocs.io/en/latest/index.html).\n'
            f'\n''**Commands**\n' 'Un elenco completo dei comandi è disponibile [qui](http://siffredi.vpsgh.it).\n' 'Al momento però il sito web non è ancora attivo.\n'
            f'\n''**Add to Discord**\n''Siffredi Bot può essere aggiunto a tutti i server che desideri! \n' '[Clicca qui per aggiungerlo al tuo](https://bit.ly/2CvbI33).\n'
            f'\n''**Premium**\n''Attualmente non attivo nessun servizio premium ma in futuro potrà essere attuato un servizio a pagamento.\n'
            f'\n''**Support**\n''[Fai clic qui](https://discord.gg/WZejfkdcV3) per parlare con il supporto se hai problemi o hai domande.\n',
            colour= discord.Color.purple()
        )
        embed.set_footer(text='discord.gg/TBSNK3V - Siffredi Bot')
        embed.set_author(name='Siffredi Bot',icon_url='https://cdn.discordapp.com/attachments/691220858638827523/746134348427690074/magik.png')
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        embed= discord.Embed(
            title='This is my ping', 
            description= f' {round((self.bot.latency * 1000)-48)}ms', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text='discord.gg/TBSNK3V - Siffredi Bot')
        await ctx.send(embed=embed)

    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        embed= discord.Embed(
            title=':bangbang: Kick:', 
            description= f'{member.mention} has been kicked for {reason} ', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text='discord.gg/TBSNK3V - Siffredi Bot')
        if ctx.author.id == OWNERID:
            await member.kick(reason=reason)
            await member.send(f"You have been kicked from the server {ctx.guild.name} for: {reason}")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"You are not cool enough to use this command")
        print (f'kick >> The command was successfully executed')

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        embed= discord.Embed(
            title=':no_entry_sign: Ban:', 
            description= f'{member.mention} has been banned for {reason}', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text='discord.gg/TBSNK3V - Siffredi Bot')
        if ctx.author.id == OWNERID:
            await member.ban(reason=reason)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"You are not cool enough to use this command")
        print (f'ban >> The command was successfully executed')

    @commands.command()
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
        embed.set_footer(text='discord.gg/TBSNK3V - Siffredi Bot')
        await ctx.send(embed=embed)
        return print (f'!unban >> The command was successfully executed')

    @commands.command()
    async def invite(self, ctx):
        embed= discord.Embed(
            title='This is the link to invite me to your server', 
            description= f' :arrow_forward: https://bit.ly/2CvbI33', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text='discord.gg/TBSNK3V - Siffredi Bot')
        await ctx.send(embed=embed)

    @commands.command(aliases = ['cl'])
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)

    @commands.command()
    async def server(self, ctx):
        embed= discord.Embed(
            title='Join into my server for help and fun', 
            description= f' :arrow_forward: https://discord.gg/TBSNK3V', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text='discord.gg/TBSNK3V - Siffredi Bot')
        await ctx.send(embed=embed)

    @commands.command(aliases = ['is'])
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
        embed.set_footer(text='discord.gg/TBSNK3V - Siffredi Bot')
        await ctx.send(embed=embed)

    @commands.command()
    async def ticket(self, ctx , *, arg):
        embed= discord.Embed(
            title='Richiesta Ticket', 
            description= f' :arrow_forward: {arg} \n by [<@{ctx.author.id}>]', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text='discord.gg/TBSNK3V - Siffredi Bot')
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed)


    @commands.command()
    async def poll(self, ctx, option1: str, option2: str, *, question):
        if option1==None and option2==None:
            await ctx.channel.purge(limit=1)
            embed= discord.Embed(
                title='New poll:', 
                description= f':arrow_right:  **{question}**\n\n✅ = Si\n❎ = No', 
                colour= discord.Color.purple()
            )
            embed.set_footer(text='discord.gg/TBSNK3V - Siffredi Bot')
            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
            await message.add_reaction('❎')
        elif option1==None:
            await ctx.channel.purge(limit=1)
            embed= discord.Embed(
                title='New poll:', 
                description= f':arrow_right:  **{question}**\n\n✅ = {option1}\n❎ = No', 
                colour= discord.Color.purple()
            )
            embed.set_footer(text='discord.gg/TBSNK3V - Siffredi Bot')
            embed.add_field(name=f'{option1}', value='✅')
            embed.add_field(name='No', value='❎')
            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
            await message.add_reaction('❎')
        elif option2==None:
            await ctx.channel.purge(limit=1)
            embed= discord.Embed(
                title='New poll:', 
                description= f':arrow_right:  **{question}**\n\n✅ = Si\n❎ = {option2}', 
                colour= discord.Color.purple()
            )
            embed.set_footer(text='discord.gg/TBSNK3V - Siffredi Bot')
            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
            await message.add_reaction('❎')
        else:
            await ctx.channel.purge(limit=1)
            embed= discord.Embed(
                title='New poll:', 
                description= f':arrow_right:  **{question}**\n\n✅ = {option1}\n❎ = {option2}', 
                colour= discord.Color.purple()
            )
            embed.set_footer(text='discord.gg/TBSNK3V - Siffredi Bot')
            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
            await message.add_reaction('❎')

def setup(client):
    client.add_cog(ModeratorCog(client))