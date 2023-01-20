import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import json

class ThreadReminder(commands.Cog):
    def init(self, bot):
        self.bot = bot
        self.settings = {}
        self.last_message_timestamp = {}
        try:
            with open('thread_reminder_settings.json', 'r') as f:
                self.settings = json.load(f)
        except:
            pass

    def cog_unload(self):
        with open('thread_reminder_settings.json', 'w') as f:
            json.dump(self.settings, f)

    @commands.command()
    async def threm(self, ctx, action: str, channel: discord.TextChannel = None, thread: str = None, *keywords):
    if action == "set":
        if channel is None or thread is None or len(keywords) == 0:
            await ctx.send("Please provide a channel, thread and at least one keyword.")
            return
        self.settings[channel.id] = {"channel": channel.id, "thread": thread, "keywords": keywords, "active": False}
        await ctx.send("Thread reminder set up for channel {} with thread {} and keywords {}".format(channel.mention, thread, keywords))
        with open('thread_reminder_settings.json', 'w') as f:
            json.dump(self.settings, f)
    elif action == "activate":
        if channel is None or thread is None:
            await ctx.send("Please provide a channel and a thread.")
            return
        if channel.id not in self.settings:
            await ctx.send("This channel has not been set up yet.")
            return
        if thread != self.settings[channel.id]["thread"]:
            await ctx.send("This thread was not set up for this channel.")
            return
        self.settings[channel.id]["active"] = True
        await ctx.send("Thread reminder for thread {} in channel {} is now active.".format(thread, channel.mention))
        with open('thread_reminder_settings.json', 'w') as f:
            json.dump(self.settings, f)
    elif action == "deactivate":
        if channel is None or thread is None:
            await ctx.send("Please provide a channel and a thread.")
            return
        if channel.id not in self.settings:
            await ctx.send("This channel has not been set up yet.")
            return
        if thread != self.settings[channel.id]["thread"]:
            await ctx.send("This thread was not set up for this channel.")
            return
        self.settings[channel.id]["active"] = False
        await ctx.send("Thread reminder for thread {} in channel {} is now inactive.".format(thread, channel.mention))
        with open('thread_reminder_settings.json', 'w') as f:
            json.dump(self.settings, f)
    elif action == "list":
        if len(self.settings) == 0:
            await ctx.send("No thread reminders have been set up yet.")
            return
        message = "Thread Reminders:\n"
        for channel_id in self.settings:
            channel = self.bot.get_channel(int(channel_id))
            if channel is None:
                continue
            message += "- {}: thread {}, keywords {}, active: {}\n".format(channel.mention, self.settings[channel_id]["thread"], self.settings[channel_id]["keywords"], self.settings[channel_id]["active"])
            await ctx.send(message)

@commands.Cog.listener()
async def on_message(self, message):
    if message.author.bot:
        return
    if message.channel.id in self.settings and self.settings[message.channel.id]["active"]:
        for keyword in self.settings[message.channel.id]["keywords"]:
            if keyword.lower() in message.content.lower():
                if message.channel.id not in self.last_message_timestamp or (datetime.now() - self.last_message_timestamp[message.channel.id]).total_seconds() > 600:
                    self.last_message_timestamp[message.channel.id] = datetime.now()
                    await message.channel.send("A thread about this topic already exists: {}\n{}".format(self.settings[message.channel.id]["thread"], self.settings[message.channel.id]["thread"]))
                    break

def setup(bot):
bot.add_cog(ThreadReminder(bot))
