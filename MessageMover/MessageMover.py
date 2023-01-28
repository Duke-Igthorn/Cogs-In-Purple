import asyncio
import datetime
from redbot.core import commands
import discord
# from discord.ext import commands
from discord import TextChannel

class MessageMover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def msgmvr(self, ctx, destination: discord.TextChannel, *message_ids: int):
        if not message_ids:
            await ctx.send('Please provide at least one message ID')
            return
        messages = []
        for message_id in message_ids:
            try:
                message = await ctx.channel.fetch_message(message_id)
            except discord.NotFound:
                await ctx.send(f"Could not find a message with ID {message_id}")
                continue
            except discord.Forbidden:
                await ctx.send(f"I am not allowed to access message {message_id}")
                continue
            messages.append(message)
        
        messages.sort(key=lambda x: x.created_at)
        
        for message in messages:
            await message.pin()
            await message.unpin()
            await message.delete()
            await destination.send(content=message.content,
                                   embed=message.embeds[0] if message.embeds else None,
                                   file=message.attachments[0].url if message.attachments else None,
                                   allowed_mentions=discord.AllowedMentions(users=False, roles=False, everyone=False))
            

def setup(bot):
    bot.add_cog(MessageMover(bot))
