import discord
from discord.ext import commands, tasks
import datetime
import re
import asyncio

class Reminder:
    def __init__(self, user_id, channel_id, message, time):
        self.user_id = user_id
        self.channel_id = channel_id
        self.message = message
        self.time = time

class RemindAgent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []
        self.check_reminders.start()

    def cog_unload(self):
        self.check_reminders.cancel()

    @commands.command()
    async def remind(self, ctx, *, reminder_text):
        """Set a reminder. Format: !remind YYYY-MM-DD HH:MM Your reminder message"""
        pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) (.+)"
        match = re.match(pattern, reminder_text)
        
        if not match:
            await ctx.send("Invalid format. Use: !remind YYYY-MM-DD HH:MM Your reminder message")
            return

        time_str, message = match.groups()
        try:
            reminder_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
            if reminder_time < datetime.datetime.now():
                await ctx.send("Cannot set reminders in the past.")
                return
        except ValueError:
            await ctx.send("Invalid date/time format. Use YYYY-MM-DD HH:MM")
            return

        reminder = Reminder(ctx.author.id, ctx.channel.id, message, reminder_time)
        self.reminders.append(reminder)
        await ctx.send(f"Reminder set for {time_str}: {message}")

    @commands.command()
    async def list_reminders(self, ctx):
        """List all reminders for the user"""
        user_reminders = [r for r in self.reminders if r.user_id == ctx.author.id]
        if not user_reminders:
            await ctx.send("You have no reminders set.")
            return

        reminder_list = "\n".join([f"{i+1}. {r.time.strftime('%Y-%m-%d %H:%M')} - {r.message}" 
                                   for i, r in enumerate(user_reminders)])
        await ctx.send(f"Your reminders:\n{reminder_list}")

    @commands.command()
    async def delete_reminder(self, ctx, index: int):
        """Delete a reminder by its index"""
        user_reminders = [r for r in self.reminders if r.user_id == ctx.author.id]
        if not user_reminders or index <= 0 or index > len(user_reminders):
            await ctx.send("Invalid reminder index.")
            return

        reminder = user_reminders[index - 1]
        self.reminders.remove(reminder)
        await ctx.send(f"Deleted reminder: {reminder.time.strftime('%Y-%m-%d %H:%M')} - {reminder.message}")

    @commands.command()
    async def modify_reminder(self, ctx, index: int, *, new_reminder_text):
        """Modify a reminder. Format: !modify_reminder <index> YYYY-MM-DD HH:MM New reminder message"""
        user_reminders = [r for r in self.reminders if r.user_id == ctx.author.id]
        if not user_reminders or index <= 0 or index > len(user_reminders):
            await ctx.send("Invalid reminder index.")
            return

        pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) (.+)"
        match = re.match(pattern, new_reminder_text)
        
        if not match:
            await ctx.send("Invalid format. Use: YYYY-MM-DD HH:MM New reminder message")
            return

        time_str, message = match.groups()
        try:
            new_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
            if new_time < datetime.datetime.now():
                await ctx.send("Cannot set reminders in the past.")
                return
        except ValueError:
            await ctx.send("Invalid date/time format. Use YYYY-MM-DD HH:MM")
            return

        reminder = user_reminders[index - 1]
        reminder.time = new_time
        reminder.message = message
        await ctx.send(f"Reminder modified. New reminder: {time_str} - {message}")

    @tasks.loop(seconds=60)
    async def check_reminders(self):
        now = datetime.datetime.now()
        to_remove = []
        for reminder in self.reminders:
            if reminder.time <= now:
                channel = self.bot.get_channel(reminder.channel_id)
                user = self.bot.get_user(reminder.user_id)
                if channel and user:
                    await channel.send(f"{user.mention}, here's your reminder: {reminder.message}")
                to_remove.append(reminder)
        
        for reminder in to_remove:
            self.reminders.remove(reminder)

    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(RemindAgent(bot))
