# usage: python launcher.py num_shards first_shard_id:last_shard_id

from bot import SiffrediBot
import json

with open('config.json') as config_file:
    config = json.load(config_file)

bot = SiffrediBot(config)
bot.run()