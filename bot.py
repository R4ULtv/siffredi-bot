import discord
import os
import asyncio
import json
import datetime

from fun import *

from discord.ext import commands, tasks
from random import choice

# Read the Data files and store them in a variable
TokenFile = open("./data/Token.txt", "r") # Make sure to paste the token in the txt file
TOKEN = TokenFile.read()

fun_guild_id = 550034941279469648

OWNERID = 495542366598594560

# Define "bot"
def get_prefix(client, message):
	with open('./data/prefixes.json', 'r') as f:
		prefixes = json.load(f)
	return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix = ".")
bot.remove_command('help')

# Let us Know when the bot is ready and has started
@bot.event
async def on_ready():
  print("============================================================\n")
  print(f"                {bot.user} IS READY ")
  print(f"               WITH ID = {bot.user.id}")
  print(f"                    By Raul Carini")
  print("\n============================================================\n")
  change_status.start()

@tasks.loop(seconds=20)
async def change_status():
  await bot.change_presence(activity=discord.Game(choice(['-help','-prefix [es. !]',f'on {len(list(bot.guilds))} server'])))

# Prefixes

# Comandi MOD


bot.help_pages = [page1, page2, page3, page4]

@bot.command()
async def fun(ctx):
    if (ctx.guild.id == fun_guild_id):
        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
        current = 0
        msg = await ctx.send(embed=bot.help_pages[current])
        for button in buttons:
            await msg.add_reaction(button)
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)
            except asyncio.TimeoutError:
                return print(" - finito il tempo - ")
            else:
                previous_page = current
                if reaction.emoji == u"\u23EA":
                    current = 0
                elif reaction.emoji == u"\u2B05":
                    if current > 0:
                        current -= 1
                elif reaction.emoji == u"\u27A1":
                    if current < len(bot.help_pages)-1:
                        current += 1
                elif reaction.emoji == u"\u23E9":
                    current = len(bot.help_pages)-1
                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)
                if current != previous_page:
                    await msg.edit(embed=bot.help_pages[current])

# A simple and small ERROR handler
@bot.event 
async def on_command_error(ctx,error):
    embed = discord.Embed(
    title='',
    color=discord.Color.red())
    if isinstance(error, commands.CommandNotFound):
        pass
    if isinstance(error, commands.MissingPermissions):
        embed.add_field(name=f'Invalid Permissions', value=f'You dont have {error.missing_perms} permissions.')
        await ctx.send(embed=embed)
    else:
        if ctx.author.id == OWNERID:
            embed.add_field(name = f':x: Terminal Error', value = f"```{error}```")
            await ctx.send(embed = embed)
        raise error
# Load command to manage our "Cogs" or extensions
@bot.command()
async def load(ctx, extension):
    # Check if the user running the command is actually the owner of the bot 
    if ctx.author.id == OWNERID:
        bot.load_extension(f'Cogs.{extension}')
        await ctx.send(f"Enabled the Cog!")
    else:
        await ctx.send(f"You are not cool enough to use this command")

# Unload command to manage our "Cogs" or extensions
@bot.command()
async def unload(ctx, extension):
    # Check if the user running the command is actually the owner of the bot 
    if ctx.author.id == OWNERID:
        bot.unload_extension(f'Cogs.{extension}')
        await ctx.send(f"Disabled the Cog!")
    else:
        await ctx.send(f"You are not cool enough to use this command")

# Reload command to manage our "Cogs" or extensions
@bot.command(name = "reload")
async def reload_(ctx, extension):
    # Check if the user running the command is actually the owner of the bot 
    if ctx.author.id == OWNERID:
        bot.reload_extension(f'Cogs.{extension}')
        await ctx.send(f"Reloaded the Cog!") 
    else:
        await ctx.send(f"You are not cool enough to use this command")

# Automatically load all the .py files in the Cogs folder
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'Cogs.{filename[:-3]}')
            print(f"Loaded Cog: {filename}")
        except Exception:
            raise Exception
        
# Run our bot
bot.run(str(TOKEN)) # Make sure you paste the CORRECT token in the "./data/Token.txt" file