import discord
from discord.ext import commands

import aiohttp
import os
import json
import time
import mysql.connector
from rich.progress import track

from logs import DiscordLogs

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

def get_prefix(client, message):
    mydb = mysql.connector.connect( host=config['aws']['host'], user=config['aws']['user'], passwd=config['aws']['password'], database=config['aws']['database'] )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT prefix FROM main_guilds WHERE guild_id=%s", (str(message.guild.id),))
    prefix = mycursor.fetchall()
    return prefix[0]

class SiffrediBot(commands.AutoShardedBot):
    def __init__(self, config):
        super().__init__(
            command_prefix = get_prefix,
            status = discord.Status.online,
            activity = discord.Game('-help'))
        self.config = config
        self.shard_count = self.config["shards"]["count"]
        shard_ids_list = []
        shard_ids = []
        
        # create list of shard ids
        for i in range(self.config["shards"]["first_shard_id"], self.config["shards"]["last_shard_id"]+1):
            shard_ids_list.append(i)
        self.shard_ids = tuple(shard_ids_list)

        self.remove_command("help")
        
        for filename in track(os.listdir('./cogs'), description=f"Loading..."):
            if filename.endswith('.py'):
                try:
                    super().load_extension(f'cogs.{filename[:-3]}')
                    print(f"Loaded Cog: {filename}")
                    time.sleep(0.05)
                    
                except Exception:
                    raise Exception

    async def on_ready(self):
        self.http_session = aiohttp.ClientSession()
        print("========================================================================================================================\n")
        print(f"                                                   {self.user.name} IS READY ")
        print(f"                                               WITH ID = {self.user.id}" )
        print(f"                                                    By Raul Carini")
        print("\n========================================================================================================================\n")

        logger = DiscordLogs().logger
        logger.info(f'{self.user.name} is online. With id : {self.user.id}.')


    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


    def run(self):
        super().run(self.config["discord_token"], reconnect=True)