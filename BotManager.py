import random
import configs.DefaultConfig as defaultConfig
import utils.DiscordUtil as discordUtil
import asyncio #to connect to geminig cog
import discord # importing discord library
from discord.ext import commands # importing commands from discord.ext
from cogs.GeminiCog import GeminiAgent # importing GeminiAgent from GeminiCog
from cogs.PollCog import PollAgent # importing PollAgent from PollCog
from cogs.RemindCog import RemindAgent # importing RemindAgent from RemindCog
from cogs.MusicCog import MusicAgent # importing MusicAgent from MusicCog
#an intent is a goal or aim behind the users message or query and also a way to tell the bot what to do 

intents = discord.Intents.all() # setting the intents to all
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents,help_command=None) # setting the command prefix to ! and the intents to intents	

@bot.event #python decorator, used to register an event handler with the bot
#tells the bot to listen for a specific event 
async def on_ready(): # when the bot is ready
    print("Bot is online...")

@bot.event
async def on_member_join(member):
    print("New member joined")
    guild = member.guild
    guildname = guild.name
    dmchannel = await member.create_dm()
    await dmchannel.send(f"Welcome to {guildname}, {member.name}!")

#help function to display the commands that the bot can use
@bot.command(aliases=["about"])
async def help(ctx):
    MyEmbed = discord.Embed(title="Commands",
                            description="These are the commands you can use with this bot. For commands used in the server, prefix them with '!'",
                            color=discord.Color.dark_purple())
    MyEmbed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYtgw-WuCePwZv602nevcoctjxEyxACf2h3Q&s")
    
    # General Commands
    MyEmbed.add_field(name="!query \"[question]\"", value="Communicate with Gemini AI Bot on the server. Wrap your question in quotes.", inline=False)
    MyEmbed.add_field(name="!pm", value="Start a private message conversation with the Gemini AI Bot.", inline=False)
    MyEmbed.add_field(name="!coinflip", value="Flip a coin. No arguments needed.", inline=False)

    # Reminder Commands
    MyEmbed.add_field(name="!remind [time] [message]", value="Set a reminder with relative time. Example: !remind 2h Take out trash", inline=False)
    MyEmbed.add_field(name="!reminder [YYYY-MM-DD HH:MM] [message]", value="Set a reminder for a specific date and time. Example: !reminder 2023-12-31 23:59 New Year's Eve", inline=False)
    MyEmbed.add_field(name="!list_reminders", value="List all your active reminders. No arguments needed.", inline=False)
    MyEmbed.add_field(name="!delete_reminder [index]", value="Delete a reminder by its index. Example: !delete_reminder 2", inline=False)
    MyEmbed.add_field(name="!modify_reminder [index] [new_time] [new_message]", value="Modify an existing reminder. Example: !modify_reminder 1 2023-12-25 12:00 Christmas lunch", inline=False)

    # Music Commands
    MyEmbed.add_field(name="!play [URL/song name]", value="Play a song or add it to the queue. Example: !play https://youtube.com/watch?v=dQw4w9WgXcQ", inline=False)
    MyEmbed.add_field(name="!pause", value="Pause the currently playing song. No arguments needed.", inline=False)
    MyEmbed.add_field(name="!resume", value="Resume the paused song. No arguments needed.", inline=False)
    MyEmbed.add_field(name="!skip", value="Skip the current song. No arguments needed.", inline=False)
    MyEmbed.add_field(name="!queue", value="Display the current music queue. No arguments needed.", inline=False)
    MyEmbed.add_field(name="!clear", value="Clear the music queue. No arguments needed.", inline=False)
    MyEmbed.add_field(name="!disconnect", value="Disconnect the bot from the voice channel. No arguments needed.", inline=False)

    # Poll Command
    MyEmbed.add_field(name="!poll \"[question]\" \"[option1]\" \"[option2]\" ...", value="Create a poll. Wrap the question and each option in quotes. Example: !poll \"Favorite color?\" \"Red\" \"Blue\" \"Green\"", inline=False)

    await ctx.send(embed=MyEmbed)


@bot.command()
async def coinflip(ctx):
    coin = random.choice(["Heads","Tails"])
    await ctx.send(f"The coin landed on {coin}")

@bot.command()
@commands.check(discordUtil.is_me) #checks if it is the owner because only the owner should be allowed to remove and add cog
async def unloadGemini(ctx): #allows you to remove the cog and reload from the server
    await bot.remove_cog('GeminiAgent')

@bot.command()
@commands.check(discordUtil.is_me)
async def reloadGemini(ctx):
    await bot.add_cog(GeminiAgent(bot))

@bot.command()
@commands.check(discordUtil.is_me)
async def unloadPoll(ctx):
    await bot.remove_cog('PollAgent')

@bot.command()
@commands.check(discordUtil.is_me)
async def reloadPoll(ctx):
    await bot.add_cog(PollAgent(bot))

async def startcogs():
    await bot.add_cog(GeminiAgent(bot))
    await bot.add_cog(PollAgent(bot))
    await bot.add_cog(RemindAgent(bot))
    await bot.add_cog(MusicAgent(bot))
asyncio.run(startcogs())


bot.run(defaultConfig.DISCORD_SDK)



