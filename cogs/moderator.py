import discord
import json
import mysql.connector
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

class Moderator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(2,300,BucketType.user) 
    @commands.hybrid_command(name="prefix", usage="-prefix [!]")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix:str):
        """You can change the bot prefix for your server"""
        mydb = mysql.connector.connect( host=config['aws']['host'], user=config['aws']['user'], passwd=config['aws']['password'], database=config['aws']['database'] )
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE main_guilds SET prefix=%s WHERE guild_id=%s", (prefix, str(ctx.guild.id)))
        mydb.commit()

        embed = discord.Embed(
            title= "The bot prefix has changed",
            description= f'The new one is: `{prefix}`',
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.cooldown(2,150,BucketType.user) 
    @commands.hybrid_command(name="kick", usage="-kick [member] Optional[reason]")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        """You can kick a person"""
        embed= discord.Embed(
            title=':bangbang: Kick:', 
            description= f'{member.mention} has been kicked for {reason} ', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await member.kick(reason=reason)
        await member.send(f"You have been kicked from the server {ctx.guild.name} for: {reason}")
        await ctx.send(embed=embed)

    @commands.cooldown(2,300,BucketType.user) 
    @commands.hybrid_command(name="ban", usage="-ban [member] Optional[reason]")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        """You can ban a person"""
        embed= discord.Embed(
            title=':no_entry_sign: Ban:', 
            description= f'{member.mention} has been banned for {reason}', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await member.ban(reason=reason)
        await ctx.send(embed=embed)

    @commands.cooldown(2,150,BucketType.user) 
    @commands.hybrid_command(name="unban", usage="-unban [member]")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        """You can unban a person"""
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

    @commands.cooldown(2,60,BucketType.user) 
    @commands.command(name="clear", usage="-clear [number<500]", aliases = ['cl'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """You can delete messages"""
        if amount < 500:
            await ctx.channel.purge(limit=amount)
        else:
            embed= discord.Embed(
                title=':warning: Error:',
                description= f'You can only delete 500 messages at a time',
                colour= discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.cooldown(2,60,BucketType.user) 
    @commands.hybrid_command(name="info", usage="-info [server/user] Optional[@user]")
    @commands.has_permissions(administrator=True)
    async def info(self, ctx, info, user: discord.Member = None):
        """You can get current server information or you can get user info for yourself or someone in the guild"""

        user = user or ctx.message.author
        embed = discord.Embed(colour= discord.Color.purple())
        roles = " ".join([role.mention for role in user.roles])

        if info == 'server' or info == 'guild':
            embed.add_field(name="Name:", value=str(ctx.guild.name))
            embed.add_field(name="Description:", value=str(ctx.guild.description), inline=False)
            embed.add_field(name="Owner:", value=str(ctx.guild.owner))
            embed.add_field(name="Server ID:", value=str(ctx.guild.id))
            embed.add_field(name="Member Count:", value=str(ctx.guild.member_count))
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

        elif info == 'user' or info == 'member':
            embed.add_field(name="Member:", value=f"{user.mention}")
            embed.add_field(name="Member name", value=f"{user}")
            embed.add_field(name="Member id:", value=f"{user.id}")
            embed.add_field(name="Nickname:", value=f"{user.nick}")
            embed.add_field(name='Account Created: ', value=user.created_at.__format__('%A, %B %d, %Y'))
            embed.add_field(name="Joined at:", value=f"{user.joined_at.__format__('%A, %B %d, %Y')}")
            embed.add_field(name="Roles:", value=f"{roles}", inline=False)
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

        else:
            embed =  discord.Embed(description="You need to choose between user or server. eg -info server", colour= discord.Color.purple())
            await ctx.send(embed=embed)       
        

    @commands.cooldown(2,60,BucketType.user) 
    @commands.hybrid_command(name="ticket", usage="-ticket [text]")
    async def ticket(self, ctx , *, arg):
        """You can create a ticket"""
        embed= discord.Embed(
            title='Ticket Request', 
            description= f' :arrow_forward: {arg} \n by [<@{ctx.author.id}>]', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderator(bot))