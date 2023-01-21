from asyncio import QueueEmpty
import discord
from discord.ext import commands
import wavelink
from wavelink.ext import spotify
import json
import random
import mysql.connector
import typing

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

# EMBED CREATOR
def embed(title, description, thumb=None, image=None, footer=False):
    embed= discord.Embed(
            title=title,
            description= description,
            colour= discord.Color.purple()
        )
    if thumb != None:
        embed.set_thumbnail(url = thumb)
    if image != None:
        embed.set_image(url = image)
    if footer:
        embed.set_footer(text=config["siffredi_footer"])
    return embed

class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""

    def message(self):
        return 'Voice Connection Error'

class NoSongPlaying(VoiceConnectionError):
    """Custom Exception class for currently playing anything errors."""

    def message(self):
        return 'No Song Playing'

class NoConnectedToVoiceChannel(VoiceConnectionError):
    """Custom Exception class for connected voice channel."""

    def message(self):
        return 'No Connected to Voice Channel'

class InvalidQueueRequest(VoiceConnectionError):
    """Custom Exception class for invalid queue request."""

    def message(self):
        return 'Invalid Queue Request'

class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""
    
    def message(self):
        return 'Invalid Voice Channel'


class Music(commands.Cog):
    """Music cog to hold Wavelink related commands and listeners."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.bot, host=config["lavalink"]["host"], port=config["lavalink"]["port"], password=config["lavalink"]["password"], https=True,
                                            spotify_client=spotify.SpotifyClient(client_id=config["spotify"]["client_id"], client_secret=config["spotify"]["client_secret"]))

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Connected to Lavalink Node: <{node.identifier}>')

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):

        ctx = player.ctx
        vc: player = ctx.voice_client

        if vc.loop:
            return await vc.play(track)

        if vc.queue.is_empty:
            return

        if vc.shuffle:
            random.shuffle(vc.queue._queue)

        # UPLOAD ON DB DATA
        mydb = mysql.connector.connect( host=config['aws']['host'], user=config['aws']['user'], passwd=config['aws']['password'], database=config['aws']['database'] )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT name, time_played FROM main_song WHERE name=%s", (track.title,))
        song = mycursor.fetchone()
        if song == None:
            mycursor.execute("INSERT INTO main_song (name, url, duration, thumbnail, uploader_name, uploader_url, time_played) VALUES (%s, %s, %s, %s, %s, %s, 1)", (track.title, track.uri, track.duration, "null", track.author, "null"))
            mydb.commit()
        elif song[0] == track.title:
            mycursor.execute("UPDATE main_song SET time_played=%s WHERE name=%s", (song[1] + 1 , song[0]))
            mydb.commit()
        mydb.close()

        next = await vc.queue.get_wait()
        await vc.play(next)
        await ctx.send(embed = embed("Now Playing", f'[{next.title}]({next.uri}) \n'f' [<@{player.ctx.author.id}>]', image = next.thumb, footer=True))

    @commands.cooldown(5,60,commands.BucketType.user)
    @commands.hybrid_command(name='play', usage="-play [search title/link]", aliases=['sing' , 'p'])
    async def play(self, ctx, *, search: str):
        """You can play a song or add the song to the queue"""

        if not ctx.voice_client:
            await self.connect(ctx)
        
        vc: wavelink.Player = ctx.voice_client

        setattr(vc, "loop", False)
        setattr(vc, "shuffle", False)

        vc.ctx = ctx

        if search.startswith("https://www.youtube.com/watch"):
            song = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        elif search.startswith("https://soundcloud.com/"):
            song = await wavelink.SoundCloudTrack.search(query=search, return_first=True)

        elif search.startswith("https://open.spotify.com/track/"):
            song = await spotify.SpotifyTrack.search(query=search, return_first=True)

        else:
            song = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        if not vc.is_playing() and vc.queue.is_empty:
            await vc.play(song)
            if isinstance(song, wavelink.YouTubeTrack):
                await ctx.send(embed = embed("Now Playing", f'[{song.title}]({song.uri}) \n'f' [<@{ctx.author.id}>]', image = song.thumb, footer=True))
            else:
                await ctx.send(embed = embed("Now Playing", f'[{song.title}]({song.uri}) \n'f' [<@{ctx.author.id}>]', footer=True))
        else:
            await vc.queue.put_wait(song)

            if isinstance(song, wavelink.YouTubeTrack):
                await ctx.send(embed = embed("Queued", f'[{song.title}]({song.uri}) \n'f' [<@{ctx.author.id}>]', thumb = song.thumb, footer=True))
            else:
                await ctx.send(embed = embed("Queued", f'[{song.title}]({song.uri}) \n'f' [<@{ctx.author.id}>]', footer=True))

    @commands.cooldown(2,30, commands.BucketType.user)
    @commands.hybrid_command(name='song', usage="-song",  aliases=['current', 'currentsong', 'playing'])
    async def song(self, ctx):
        """Display information about the currently playing song"""
        if not ctx.voice_client:
            raise NoConnectedToVoiceChannel("I'm not connected to a Voice Channel")

        vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            raise NoSongPlaying("I'm not currently playing anything!")

        embed = embed= discord.Embed(
            title="Current Song Info",
            description= f"[{vc.track.title}]({vc.track.uri}) - ***by {vc.track.author}***",
            colour= discord.Color.purple()
        )
        embed.set_footer(text=config["siffredi_footer"])
        embed.add_field(name="Position", value=f"{vc.position}s")
        embed.add_field(name="Duration", value=f"{vc.track.duration}s")

        await ctx.send(embed = embed)

    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.hybrid_command(name='next', usage='-next [search title/link]', aliases=['n'])
    async def next(self, ctx, *, search: str):
        """You can play a song next to the current one"""
        if not ctx.voice_client:
            raise NoConnectedToVoiceChannel("I'm not connected to a Voice Channel")

        vc: wavelink.Player = ctx.voice_client

        if search.startswith("https://www.youtube.com/watch"):
            song = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        elif search.startswith("https://soundcloud.com/"):
            song = await wavelink.SoundCloudTrack.search(query=search, return_first=True)

        elif search.startswith("https://open.spotify.com/track/"):
            song = await spotify.SpotifyTrack.search(query=search, return_first=True)

        else:
            song = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        if vc.is_playing():

            if isinstance(song, wavelink.YouTubeTrack):
                await ctx.send(embed = embed("Next", f'[{song.title}]({song.uri}) \n'f' [<@{ctx.author.id}>]', thumb = song.thumb, footer=True))
            else:
                await ctx.send(embed = embed("Next", f'[{song.title}]({song.uri}) \n'f' [<@{ctx.author.id}>]', footer=True))

            await vc.queue.put_at_front(song)
            

    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.hybrid_command(name='remove', usage="-remove [index]")
    async def remove(self, ctx, index:int):
        """Removes a given song from the queue"""

        if not ctx.voice_client:
            raise NoConnectedToVoiceChannel("I'm not connected to a Voice Channel")

        vc: wavelink.Player = ctx.voice_client
        if not vc.queue.is_empty:
            del vc.queue._queue[index-1]
            await ctx.send(embed = embed("", f"<@{ctx.author.id}>: Removed #**{index}** from the queue."))
        else:
            raise InvalidQueueRequest("The queue is empty.")
    
    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.hybrid_command(name="loop", usage="-loop")
    async def loop(self, ctx):
        """You can loop the song"""
        if not ctx.voice_client:
            raise NoConnectedToVoiceChannel("I'm not connected to a Voice Channel")

        vc: wavelink.Player = ctx.voice_client        

        if vc.is_playing():
            vc.loop = not vc.loop
            if vc.loop:
                await ctx.send(embed = embed("", f"<@{ctx.author.id}>: Loop Activated"))
            else:
                await ctx.send(embed = embed("", f"<@{ctx.author.id}>: Loop Disabled"))
        else:
            raise NoSongPlaying("I'm not currently playing anything!")

    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.hybrid_command(name="shuffle", usage="-skip")
    async def shuffle(self, ctx):
        """You can shuffle the queue"""
        if not ctx.voice_client:
            raise NoConnectedToVoiceChannel("I'm not connected to a Voice Channel")

        vc: wavelink.Player = ctx.voice_client
        vc.shuffle = not vc.shuffle
        
        if vc.shuffle:
            await ctx.send(embed = embed("", f"<@{ctx.author.id}>: Shuffle Activated"))
        else:
            await ctx.send(embed = embed("", f"<@{ctx.author.id}>: Shuffle Disabled"))

    @commands.cooldown(2,30, commands.BucketType.user)
    @commands.hybrid_command(name="filter", usage="-filter [name]")
    async def filter(self, ctx, name: typing.Literal["None", "Bass Boost", "Errape", "TikTok Mode"]):
        """You can apply a filter to songs"""
        if not ctx.voice_client:
            raise NoConnectedToVoiceChannel("I'm not connected to a Voice Channel")

        vc: wavelink.Player = ctx.voice_client

        if name == "None":
            await vc.set_filter(wavelink.Filter(equalizer=wavelink.Equalizer.flat()))
            return await ctx.send(embed = embed("",f"<@{ctx.author.id}>: Filter Disabled"))

        if name == "Bass Boost":
            bands = [
                (0, 0), (1, 0.0), (2, 0.15), (3, 0.15), (4, 0.10),
                (5, 0), (6, 0), (7, 0), (8, 0), (9, 0),
                (10, 0), (11, 0), (12, 0), (13, 0), (14, 0)
            ]
            await vc.set_filter(wavelink.Filter(equalizer=wavelink.Equalizer(name="BassBoost", bands=bands)))
        elif name == "Errape":
            bands = [
                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
                (5, 1), (6, 1), (7, 1), (8, 1), (9, 1),
                (10, 1), (11, 1), (12, 1), (13, 1), (14, 1)
            ]
            await vc.set_filter(wavelink.Filter(equalizer=wavelink.Equalizer(name="Errape", bands=bands)))
        elif name == "TikTok Mode":
            await vc.set_filter(wavelink.Filter(timescale=wavelink.Timescale(speed=0.85, pitch=0.85)))
        await ctx.send(embed = embed("",f"<@{ctx.author.id}>: Filter **{name}** Activated"))

    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.hybrid_command(name='pause', usage="-pause")
    async def pause(self, ctx):
        """Pause the currently playing song"""
        if not ctx.voice_client:
            raise NoConnectedToVoiceChannel("I'm not connected to a Voice Channel")

        vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            raise NoSongPlaying("I'm not currently playing anything!")
        
        await vc.pause()
        await ctx.send(embed = embed("",f'<@{ctx.author.id}>: Paused the song!'))

    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.hybrid_command(name='resume', usage="-resume")
    async def resume(self, ctx):
        """Resume the currently paused song"""
        if not ctx.voice_client:
            raise NoConnectedToVoiceChannel("I'm not connected to a Voice Channel")

        vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            raise NoSongPlaying("I'm not currently playing anything!")

        await vc.resume()
        await ctx.send(embed = embed("",f'<@{ctx.author.id}>: Resumed the song!'))
    
    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.hybrid_command(name='skip', usage="-skip", aliases=['s'])
    async def skip(self, ctx):
        """Skip the song"""
        if not ctx.voice_client:
            raise NoConnectedToVoiceChannel("I'm not connected to a Voice Channel")

        vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            raise NoSongPlaying("I'm not currently playing anything!")

        await vc.stop()
        await ctx.send(embed = embed("",f'<@{ctx.author.id}>: Skipped the song!'))

    @commands.cooldown(2,30, commands.BucketType.user)
    @commands.hybrid_command(name='queue', usage="-queue" ,aliases=['q', 'playlist'])
    async def queue(self, ctx):
        """Retrieve a basic queue of upcoming songs"""
        if not ctx.voice_client:
            raise VoiceConnectionError("I'm not currently connected to voice!")

        vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty:
            raise InvalidQueueRequest("The queue is empty.")

        queue = vc.queue.copy()

        string = ""
        for num, song in enumerate(queue):
                string += f"{num+1}) [{song.title}]({song.uri})\n"

        await ctx.send(embed = embed(f'Upcoming - Next {len(queue)}', string, footer=True))
    
    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.hybrid_command(name='volume', usage="-volume [number betwenn 1 and 100]", aliases=['vol'])
    async def volume(self, ctx, amount:int):
        """Change the player volume"""
        if not ctx.voice_client:
            raise VoiceConnectionError("I'm not currently connected to voice!")
        
        if amount > 200 or amount < 0:
            raise VoiceConnectionError("The volume must be between 0 and 200.")

        loading = ''
        not_load = ''
        for i in range(int(amount/10)):
            loading += ':purple_square:' 
            
        for i in range(10-int(amount/10)):
            not_load += ':black_large_square:'

        await ctx.voice_client.set_volume(amount)
        await ctx.send(embed = embed(f'Set the volume to **{int(amount)}%**', f'{loading}{not_load}'))
    
    @commands.cooldown(2,30,commands.BucketType.user)
    @commands.hybrid_command(name="seek", usage="-seek [seconds]")
    async def seek(self, ctx, seconds:int):
        """Change position to seconds givens"""
        if not ctx.voice_client:
            raise NoConnectedToVoiceChannel("I'm not connected to a Voice Channel")

        vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            raise NoSongPlaying("I'm not currently playing anything!")

        await vc.seek(seconds*1000)
        await ctx.send(embed = embed("", f'Set the postion to **{int(seconds)}s**'))

    @commands.cooldown(1,30,commands.BucketType.user)
    @commands.hybrid_command(name='connect', usage='-connect', aliases=['join'])
    async def connect(self, ctx):
        """The bot will enter the voice channel"""
        try:
            await ctx.author.voice.channel.connect(cls=wavelink.Player)
            await ctx.send(embed = embed("", f'Connected to: **{ctx.author.voice.channel}**'))
        except Exception:
            raise InvalidVoiceChannel("There was an error connecting to the Voice Channel")

    @commands.cooldown(1,30,commands.BucketType.user)
    @commands.hybrid_command(name='disconnect', usage="-disconnect", aliases=['leave', 'd'])
    async def disconnect(self, ctx):
        """Stop the currently playing song and destroy the player"""
        if not ctx.voice_client:
            raise NoConnectedToVoiceChannel("I'm not connected to a Voice Channel")

        vc: wavelink.Player = ctx.voice_client

        try:
            await vc.disconnect()
            await ctx.send(embed = embed("", f'<@{ctx.author.id}>: Disconncted the bot!'))
        except Exception:
            raise InvalidVoiceChannel("There was an error disconnecting to the Voice Channel")

async def setup(bot):
    await bot.add_cog(Music(bot))