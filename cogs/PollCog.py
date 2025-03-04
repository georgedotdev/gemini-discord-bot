import discord
from discord.ext import commands,tasks

class PollAgent(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.numbers = ["🐵","🐶","🦍","🐑","🐇","🦊"]
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == "ping poll-agent":
            await msg.channel.send("poll-agent is connected..")
    @commands.command()
    async def poll(self, ctx, minutes:int, title, *options):
        if len(options) == 0:
            pollEmbed = discord.Embed(title=title, description=f"You have **{minutes}** minutes remaining!")
            msg = await ctx.send(embed=pollEmbed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
        else:
            pollEmbed = discord.Embed(title=title, description=f"You have **{minutes}** minutes remaining!")
            for number, option in enumerate(options):
                pollEmbed.add_field(name=f"{self.numbers[number]}", value=f"**{option}**", inline=False)
            msg = await ctx.send(embed=pollEmbed)
            for x in range(len(pollEmbed.fields)):
                await msg.add_reaction(self.numbers[x])
        self.poll_loop.start(ctx, minutes, title, options, msg)

    @tasks.loop(minutes=1)
    async def poll_loop(self, ctx, minutes, title, options, msg):
        count = self.poll_loop.current_loop
        remaining_time = minutes-count
        newEmbed = discord.Embed(title=title, description=f"You have **{remaining_time}** minutes remaining!")
        for number, option in enumerate(options):
            newEmbed.add_field(name=f"{self.numbers[number]}", value=f"**{option}**", inline=False)
        msg = await msg.edit(embed=newEmbed)
        if remaining_time == 0:
            counts = []
            reactions = msg.reactions
            for reaction in reactions:
                counts.append(reaction.count)
            max_value = max(counts)
            # checks to see if there is a draw by seeing if more than on object has the same max value
            i = 0
            for count in counts:
                if count == max_value:
                    i = i+1
            if i > 1:
                await ctx.send("It's a draw.")
            else:
                max_index = counts.index(max_value)
                if len(options) == 0:
                    winneremoji = reactions[max_index]
                    await ctx.send("Times up")
                    if winneremoji.emoji == "👍":
                        await ctx.send("Seems that people think that way.")
                    if winneremoji.emoji == "👎":
                        await ctx.send("Seems that people don't like that.")
                else:
                    winner = options[max_index]
                    winneremoji = reactions[max_index]
                    await ctx.send("Times up")
                    await ctx.send(f"{winneremoji.emoji} **{winner}** has won the poll")
            self.poll_loop.stop()