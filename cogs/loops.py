import discord
import json
import time 
import requests
import mysql.connector
from discord.ext import commands, tasks

import logging

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

class Loops(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.send_ping.start()
        self.send_data.start()

    @tasks.loop(seconds=10)
    async def send_ping(self):

        sp_apihost = config["sp_apihost"]
        sp_apikey = config["sp_apikey"]
        sp_pageid = config["sp_pageid"]
        sp_metricid = config["sp_metricid"]
        metric_value = self.bot.latency * 1000

        request_url = sp_apihost + "/v1/pages/" + sp_pageid + "/metrics/" + sp_metricid + "/data.json"
        payload = {'data': {'timestamp': int(time.time()), 'value': metric_value}}
        headers = {'Authorization': 'OAuth ' + sp_apikey}

        logging.debug("POST {} PAYLOAD: {}".format(request_url, payload))

        if not False:  # Don't send the value if dry-running
            res = requests.post(request_url, json=payload, headers=headers)
            res.raise_for_status()  # If not 200, raise HTTPError Exception

    @tasks.loop(seconds=300)
    async def send_data(self):
        members = 0
        channel = 0

        mydb = mysql.connector.connect( host=config['aws']['host'], user=config['aws']['user'], passwd=config['aws']['password'], database=config['aws']['database'] )
        mycursor = mydb.cursor()

        for guild in self.bot.guilds:
            members += guild.member_count
            channel += len(guild.text_channels)

        mycursor.execute("UPDATE main_data SET value=%s WHERE name=%s", (len(self.bot.guilds), "servers"))
        mydb.commit()
        mycursor.execute("UPDATE main_data SET value=%s WHERE name=%s", (members, "users"))
        mydb.commit()
        mycursor.execute("UPDATE main_data SET value=%s WHERE name=%s", (channel, "channels"))
        mydb.commit()

def setup(bot):
    bot.add_cog(Loops(bot))