import configs.DefaultConfig as defaultConfig
import utils.DiscordUtil as discordUtil
from discord.ext import commands
import google.generativeai as genai


genai.configure(api_key=defaultConfig.GEMINI_SDK)
#discord max message length handler
DISCORD_MAX_MESSAGE_LENGTH=2000
PLEASE_TRY_AGAIN_ERROR_MESSAGE='There was an issue with your question please try again.. '

class GeminiAgent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.model = genai.GenerativeModel('gemini-pro')

    @commands.Cog.listener() #this is a listener that listens for a specific event
    async def on_message(self,msg):
        try:
            if msg.content == 'ping gemini-agent':
                await msg.channel.send('Agent is connected...')
        except Exception as e:
            return PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e)
    