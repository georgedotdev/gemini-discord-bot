import random
import configs.DefaultConfig as defaultConfig
import utils.DiscordUtil as discordUtil
import asyncio #to connect to geminig cog
import discord # importing discord library
from discord.ext import commands # importing commands from discord.ext
from cogs.GeminiCog import GeminiAgent # importing GeminiAgent from GeminiCog
from cogs.PollCog import PollAgent # importing PollAgent from PollCog
from cogs.RemindCog import RemindAgent # importing RemindAgent from RemindCog

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
@bot.command(aliases = ["about"])
async def help(ctx):
    MyEmbed = discord.Embed(title = "Commands",
                            description = "These are the Commands that you can use for this bot. Once you are in a private message with the bot you can interact with it normally without issuing commands",
                            color = discord.Color.dark_purple())
    MyEmbed.set_thumbnail(url = "https://th.bing.com/th/id/OIG.UmTcTiD5tJbm7V26YTp.?w=270&h=270&c=6&r=0&o=5&pid=ImgGn")
    MyEmbed.add_field(name = "!query", value = "This command allows you to communicate with Gemini AI Bot on the Server. Please wrap your questions with quotation marks.", inline = False)
    MyEmbed.add_field(name = "!pm", value = "This command allows you to private message the Gemini AI Bot.", inline = False)
    await ctx.send(embed = MyEmbed)

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

asyncio.run(startcogs())


bot.run(defaultConfig.DISCORD_SDK)



