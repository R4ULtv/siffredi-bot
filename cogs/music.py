import discord
from discord.ext import commands

import json
import asyncio
import itertools
import sys
import traceback
import mysql.connector
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

def create_embed(title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.purple())
    return embed

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    #'before_options': '-nostdin',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')
        self.id = data.get('id')
        self.duration = data.get('duration')
        self.thumbnail = data.get('thumbnail')
        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=True):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
            
        embed= discord.Embed(
            title='Queued', 
            description= f'[{data["title"]}]({data["webpage_url"]}) \n'f' [<@{ctx.author.id}>]', 
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)



class MusicPlayer(commands.Cog):
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None # Now playing message
        self.volume = .5 # Default volume
        self.current = None

        mydb = mysql.connector.connect( host=config['aws']['host'], user=config['aws']['user'], passwd=config['aws']['password'], database=config['aws']['database'] )
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT music_time_left FROM main_guilds WHERE guild_id={ctx.guild.id}")
        self.time_left = int(mycursor.fetchone()[0]) # default 5 minutes
        mydb.close()

        ctx.bot.loop.create_task(self.player_loop())


    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()
            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(self.time_left):
                    source = await self.queue.get()
                    
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(embed=create_embed('There was an error processing your song.',e))
                    continue

            source.volume = self.volume
            self.current = source

            mydb = mysql.connector.connect( host=config['aws']['host'], user=config['aws']['user'], passwd=config['aws']['password'], database=config['aws']['database'] )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT name, time_played FROM main_song WHERE name=%s", (source.title,))

            song = mycursor.fetchone()

            if song == None:
                mycursor.execute("INSERT INTO main_song (name, url, duration, thumbnail, uploader_name, uploader_url, time_played) VALUES (%s, %s, %s, %s, %s, %s, 1)", (source.title, source.web_url, source.duration, source.thumbnail, source.uploader, source.uploader_url))
                mydb.commit()
            elif song[0] == source.title:
                mycursor.execute("UPDATE main_song SET time_played=%s WHERE name=%s", (song[1] + 1 , song[0]))
                mydb.commit()

            mydb.close()

            embed= discord.Embed(
                title='Now Playing', 
                description= f'[{source.title}]({source.web_url}) \n'f' [<@{source.requester.id}>]',
                colour= discord.Color.purple()
            )
            embed.set_image(url=source.thumbnail)
            embed.set_footer(text=config["siffredi_footer"])

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(embed=embed)
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    """Music related commands."""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send(embed=create_embed('Error','This command can not be used in Private Messages.'))
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send(embed=create_embed('Error','Error connecting to Voice Channel. \nPlease make sure you are in a valid channel or provide me with one'))

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.cooldown(2,60,commands.BucketType.user)
    @commands.command(name='connect', usage="-connect", aliases=['join'])
    async def connect_(self, ctx):
        """The bot will enter the voice channel"""
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            raise InvalidVoiceChannel('No channel to join.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')

        embed= discord.Embed(
            title='', 
            description= f'Connected to: **{channel}**',
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.cooldown(5,60,commands.BucketType.user)
    @commands.command(name='play', usage="-play [search title/link]", aliases=['sing' , 'p'])
    async def play_(self, ctx, *, search: str):
        """You can play a song or a video"""
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)

    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.command(name='pause', usage="-pause")
    async def pause_(self, ctx):
        """Pause the currently playing song"""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send('I am not currently playing anything!')
        elif vc.is_paused():
            return

        vc.pause()
        embed= discord.Embed(
            title='', 
            description= f'<@{ctx.author.id}>: Paused the song!',
            colour= discord.Color.purple()
        )
        await ctx.send(embed=embed)

    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.command(name='resume', usage="-resume")
    async def resume_(self, ctx):
        """Resume the currently paused song"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', )
        elif not vc.is_paused():
            return

        vc.resume()
        embed= discord.Embed(
            title='', 
            description= f'<@{ctx.author.id}>: Resumed the song!',
            colour= discord.Color.purple()
        )
        await ctx.send(embed=embed)

    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.command(name='skip', usage="-skip")
    async def skip_(self, ctx):
        """Skip the song"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!')

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        embed= discord.Embed(
            title='', 
            description= f'<@{ctx.author.id}>: Skipped the song!',
            colour= discord.Color.purple()
        )
        await ctx.send(embed=embed)

    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.command(name='queue', usage="-queue" ,aliases=['q', 'playlist'])
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!')

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('There are currently no more queued songs.')

        # Grab up to 5 entries from the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f"`{_['title']}`" for _ in upcoming)
        embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt, colour= discord.Color.purple())
        embed.set_footer(text=config["siffredi_footer"])

        await ctx.send(embed=embed)

    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.command(name='song', usage="-song",  aliases=['current', 'currentsong', 'playing'])
    async def now_playing_(self, ctx):
        """Display information about the currently playing song"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', )

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send('I am not currently playing anything!')

        #try:
            # Remove our previous now_playing message.
            await player.np.delete()
        #except discord.HTTPException:
            pass
        embed= discord.Embed(
            title='Now Playing:', 
            description= f'[{vc.source.title}]({vc.source.web_url}) \n'f' [<@{vc.source.requester.id}>]',
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        player.np = await ctx.send(embed=embed)

    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.command(name='volume', usage="-volume [number betwenn 1 and 100]", aliases=['vol'])
    async def change_volume(self, ctx, *, vol: float):
        """Change the player volume"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', )

        if not 0 < vol < 101:
            return await ctx.send('Please enter a value between 1 and 100.')

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        loading = ''
        not_load = ''
        for i in range(int(vol/10)):
            loading += ':purple_square:' 
            
        for i in range(10-int(vol/10)):
            not_load += ':black_large_square:'

        embed= discord.Embed(
            title=f'Set the volume to **{int(vol)}%**', 
            description= f'{loading}{not_load}',
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

    @commands.cooldown(1,30,commands.BucketType.user)
    @commands.command(name='disconnect', usage="-disconnect", aliases=['leave'])
    async def stop_(self, ctx):
        """Stop the currently playing song and destroy the player"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!')

        await self.cleanup(ctx.guild)

    @commands.cooldown(2,60,commands.BucketType.user)
    @commands.command(name='topsongs', usage="-topsongs", aliases=['top', 'top10', 'top10songs', 'leaderboard'])
    async def top_songs(self, ctx):
        """Display the top 10 songs"""
        mydb = mysql.connector.connect( host=config['aws']['host'], user=config['aws']['user'], passwd=config['aws']['password'], database=config['aws']['database'] )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM main_song ORDER BY time_played DESC LIMIT 10")
        myresult = mycursor.fetchall()
        embed= discord.Embed(
            title='Top 10 Songs of Siffredi Bot',
            colour= discord.Color.purple()
        )
        for index, song in enumerate(myresult):
            embed.add_field(name=f'{index+1}.', value=f'[{song[1]}]({song[2]})', inline=False)
        embed.set_footer(text=config["siffredi_footer"])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Music(bot))
