import discord
from discord.ext import commands, tasks
import logging
import aiohttp
import os
import asyncio
import json
import datetime

from random import choice


#logging.basicConfig(level=logging.INFO)

extensions = (
    "cogs.poll", 
    "cogs.strawpoll",
    "cogs.moderator",
    "cogs.funny",
    "cogs.event",
    "cogs.help",
    "cogs.music",
    "cogs.owner"
    )

def get_prefix(client, message):
    with open("data.json", 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

class SiffrediBot(commands.AutoShardedBot):
    def __init__(self, config):
        super().__init__(
            command_prefix = get_prefix,
            status = discord.Status.online,
            activity=discord.Game('-help | siffredi.vpsgh.it'))
        self.config = config
        self.shard_count = self.config["shards"]["count"]
        shard_ids_list = []
        shard_ids = []
        
        # create list of shard ids
        for i in range(self.config["shards"]["first_shard_id"], self.config["shards"]["last_shard_id"]+1):
            shard_ids_list.append(i)
        self.shard_ids = tuple(shard_ids_list)

        self.remove_command("help")
        
        for extension in extensions:
            self.load_extension(extension)

    async def on_ready(self):
        self.http_session = aiohttp.ClientSession()
        print("============================================================\n")
        print(f"                {self.user.name} IS READY ")
        print(f"               WITH ID = {self.user.id}")
        print(f"                    By Raul Carini")
        print("\n============================================================\n")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


    # @on_message.error
    # async def on_message_error(self, ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send('I could not find that member...')


    def run(self):
        super().run(self.config["discord_token"], reconnect=True)