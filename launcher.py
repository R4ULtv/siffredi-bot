from bot import SiffrediBot
import json

with open('config.json') as config_file:
    config = json.load(config_file)

bot = SiffrediBot(config)
bot.run()