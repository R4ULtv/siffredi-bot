import discord
import os
import asyncio
import json

from discord.ext import commands, tasks
from random import choice

from discord.ext.commands.core import command


with open('config.json') as config_file:
    config = json.load(config_file)

class FunnyCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def list(self, ctx):
        list_commands = ""
        for command in self.bot.commands:
            list_commands+=f'{command}\n'
        await ctx.send(list_commands)

    @commands.command()
    async def fun(self, ctx):
        contents = ["1", "2", "3", "4"]
        pages = 4
        cur_page = 1
        embed = discord.Embed(
            title='List of funny commands',
            description = f'{contents[cur_page-1]}',
            colour= discord.Color.purple()
            )
        message = await ctx.send(embed=embed)
        # getting the message object for editing and reacting

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed = discord.Embed(title='List of funny commands', description = f'{contents[cur_page-1]}', colour= discord.Color.purple()))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed = discord.Embed(title='List of funny commands', description = f'{contents[cur_page-1]}', colour= discord.Color.purple()))
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break
                # ending the loop if user doesn't react after x seconds

    @commands.command()
    async def blyatman(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            song = ('https://spoti.fi/3fFoGJr')
            embed= discord.Embed(
                title=':notes: Playlist di Spotify', 
                description= f'{song}', 
                colour= discord.Color.purple()
            )
            embed.set_author(name='Dj Blyatman',icon_url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/blaytman-icon.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/blyatman.jpeg')
            await ctx.send(embed=embed)

    @commands.command()
    async def gere(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            song = ('https://open.spotify.com/playlist/5OUoX5E2W8ta1qRFvEMqyz?si=E_HfNms1QSWvwPVBuItQTg')
            embed= discord.Embed(
                title=':notes: Playlist di Spotify del gere', 
                description= f'{song}', 
                colour= discord.Color.purple()
            )
            embed.set_author(name='disco music',icon_url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/gere-spotify.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def nibba(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='My favorite gif', 
                description= f' :arrow_forward: Nibba Dance', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='https://media0.giphy.com/media/S6qnBS6gJDrUiVbTSx/giphy.gif')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def helo(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='My favorite gif', 
                description= f' :arrow_forward: Eyeroll What GIF', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='https://media1.tenor.com/images/a81d51b51638e71c1dea16132519af01/tenor.gif')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def clown(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lei?', 
                description= f' :clown: Bassani Josita', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/clown.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def scrofa(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lei?', 
                description= f' :arrow_forward: Mariagrazia Papetti', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/scrofa.png')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def ippo(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lei?', 
                description= f' :arrow_forward: Laura Bresciani', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/ippo.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def fabrizio(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: Il gatto Fabrizio', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/fabrizio.png')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def down(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: Il ragazzo più bello di sempre', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='https://media2.giphy.com/media/d7kmbKxjiYDefvw38b/giphy.gif')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def suora(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lei?', 
                description= f' :arrow_forward: La suora Vittoria', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/suora.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def mino(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: Brioche e Cappuccino ad ogni ora', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/mino.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def terrone(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: Cremo il Terrone in persona', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/terrone.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def boomer(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: Il miglior boomer di sempre', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/salti.png')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def dio(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: Il nostro gesù di fiducia', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/dio.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def defendi(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: Colui che ama i bambini', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/defendi.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def esperto(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: Sa tutto di tutti', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/esperto.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def boss(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: Il boss del POPPIN', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/boss.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def bit(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: 0101101 solo lui li fa così', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/bit.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def cagna(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: Va a solo a banconote da 5€', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/cagna.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def kit(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: Il bomber kit', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/kit.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def gay(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: Ingoio cazzi ', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/gay.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def napoli(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: Il sommo NapoleThanos', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/napoli.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def india(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title=' :notes: Light up Skechers', 
                description= f' :arrow_forward: https://www.youtube.com/watch?v=feq6MOg3qpA', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/india.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def india2(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title=' :notes: Places', 
                description= f' :arrow_forward: https://www.youtube.com/watch?v=PlVPv5Oxg68', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/india2.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def mauro(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title=' Hey ma stai parlando di lui?', 
                description= f' Gli occhi di Mauro non mentono mai', 
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/mauro.png')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def faggot(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title=' Hey ma stai parlando di lui?', 
                description= f':arrow_right: ***Cer_Faggot***',
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/faggot.jpeg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def cvicev(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title=' Hey ma stai parlando di lui?', 
                description= f':arrow_right: **Cvicev** pazzo sgravato',
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/cvicev.jpeg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def spotify(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='My playlist on Spotify', 
                description= f' :arrow_forward: https://spoti.fi/39nyKTP',
                colour= discord.Color.purple()
            )
            embed.set_author(name='R4ULtv', icon_url='https://upload.wikimedia.org/wikipedia/commons/f/f2/Logoappliandrospotify.png')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def off(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title='We sciao beli io vado a nanna', 
                description= f' :arrow_forward: I miei cazzo di neuroni sono stanchi',
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/off.jpg')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

    @commands.command()
    async def ninja(self, ctx):
        if (ctx.guild.id == int(config["fun_guild_id"])):
            embed= discord.Embed(
                title=' Hey ma stai parlando di lui?', 
                description= f' :arrow_forward: Er **Ninja** de Bari',
                colour= discord.Color.purple()
            )
            embed.set_image(url='http://siffredi.vpsgh.it/img/image-discord/image-discord-funny/ninja.png')
            embed.set_footer(text=config["siffredi_footer"])
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FunnyCog(bot))