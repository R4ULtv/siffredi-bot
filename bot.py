import discord
from discord.ext import commands

import aiohttp
import os
import json
import mysql.connector

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
            activity = discord.Game('/help | v3.0'),
            intents= discord.Intents.all(),
            case_insensitive=True
        )
        self.config = config
        self.shard_count = self.config["shards"]["count"]
        shard_ids_list = []
        self.shard_ids = []
        
        # create list of shard ids
        for i in range(self.config["shards"]["first_shard_id"], self.config["shards"]["last_shard_id"]+1):
            shard_ids_list.append(i)
        self.shard_ids = tuple(shard_ids_list)

        self.remove_command("help")

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await super().load_extension(f'cogs.{filename[:-3]}')           
                except Exception:
                    raise Exception
        print('==> All Cogs Loaded')

        mydb = mysql.connector.connect( host=config['aws']['host'], user=config['aws']['user'], passwd=config['aws']['password'], database=config['aws']['database'] )
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM commands_command")
        for cmd in self.commands:
            sql = "INSERT INTO commands_command (name, description, syntax, type, aliases) VALUES (%s, %s, %s, %s, %s)"
            val = (str(cmd.name), str(cmd.help), str(cmd.usage), str(cmd.cog_name), str(cmd.aliases))
            mycursor.execute(sql, val)
            mydb.commit()
        print('==> All Commands Loaded')
        mycursor.close()
        mydb.close()

    async def on_ready(self):
        await self.tree.sync()
        self.http_session = aiohttp.ClientSession()
        print("===============================================================================================\n")
        print(f'\t\tLogged in as: {self.user.name} | {self.user.id} | Version: {discord.__version__}')
        print(f'\t\t\t\tShard count: {self.shard_count} | Shard ids: {self.shard_ids}')
        print(f"\t\t\t\t\tBy Raul Carini")
        print("\n===============================================================================================\n")

        logger = DiscordLogs().logger
        logger.info(f'{self.user.name} is online. With id : {self.user.id}.')

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


    def run(self):
        super().run(self.config["discord_token"], reconnect=True, log_handler= None)