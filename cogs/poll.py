import discord
from discord.ext import commands
import json
from discord.ext.commands.cooldowns import BucketType

# CONFIG FILE
with open('config.json') as config_file:
    config = json.load(config_file)

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.emojiLetters = [
            "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER E}", 
            "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"
        ]

    # parses the title, which should be in between curly brackets ('{ title }')
    def find_title(self, message):
        # this is the index of the first character of the title
        first = message.find('{') + 1
        # index of the last character of the title
        last = message.find('}')
        if first == 0 or last == -1:
            return "Not using the command correctly"
        return message[first:last]
    # parses the options (recursively), which should be in between square brackets ('[ option n ]')
    def find_options(self, message, options):
        # first index of the first character of the option
        first = message.find('[') + 1
        # index of the last character of the title
        last = message.find(']')
        if (first == 0 or last == -1):
            if len(options) < 2:
                return "Not using the command correctly"
            else:
                return options
        options.append(message[first:last])
        message = message[last+1:]
        return self.find_options(message, options) 

   
    
    #@commands.Cog.listener()
    @commands.cooldown(2,60,BucketType.user) 
    @commands.hybrid_command(name="poll", usage="-poll {title} Optional[Optiona1] Optional[Optiona2]")
    # Limit how often a command can be used, (num per, seconds, BucketType.default/user/member/guild/channel/role)
    async def poll(self, ctx):
        """You can create a poll"""
        message = ctx.message
        if not message.author.bot:
            
                messageContent = message.clean_content
                if messageContent.find("{") == -1:
                    await message.add_reaction('👍')
                    await message.add_reaction('👎')
                    await message.add_reaction('🤷')
                else:
                    title = self.find_title(messageContent)
                    options = self.find_options(messageContent, [])

                    try:
                        pollMessage = ""
                        i = 0
                        for choice in options:
                            if not options[i] == "":
                                if len(options) > 21:
                                    await message.channel.send("Please make sure you are using the command correctly and have less than 21 options.")
                                    return
                                elif not i == len(options):
                                    pollMessage = pollMessage + "\n\n" + self.emojiLetters[i] + " " + choice
                            i += 1

                        e = discord.Embed(title="**" + title + "**",
                                description=pollMessage ,
                                          colour= discord.Color.purple())
                        e.set_footer(text=config["siffredi_footer"])
                        await ctx.channel.purge(limit=1)
                        pollMessage = await message.channel.send(embed=e)
                        i = 0
                        final_options = []  # There is a better way to do this for sure, but it also works that way
                        for choice in options:
                            if not i == len(options) and not options[i] == "":
                                final_options.append(choice)
                                await pollMessage.add_reaction(self.emojiLetters[i])
                            i += 1
                    except KeyError:
                        return "Please make sure you are using the format 'poll: {title} [Option1] [Option2] [Option 3]'"


async def setup(bot):
    await bot.add_cog(Poll(bot))
