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
        if not message_ids or not destination:
            return await ctx.send("Please provide a destination channel and at least one message ID.")
        
        messages = []
        for message_id in message_ids:
            try:
                message = await ctx.channel.fetch_message(message_id)
                messages.append(message)
            except discord.NotFound:
                return await ctx.send(f"Message with ID {message_id} not found.")
            except discord.Forbidden:
                return await ctx.send(f"I don't have permission to access message with ID {message_id}.")
        
        messages.sort(key=lambda x: x.created_at)
        
        for message in messages:
            await message.pin()
            await message.unpin()
            await message.delete()
            await destination.send(content=message.content,
                                   embed=message.embeds[0] if message.embeds else None,
                                   file=message.attachments[0].url if message.attachments else None,
                                   allowed_mentions=discord.AllowedMentions(users=False, roles=False, everyone=False),
                                   author=message.author)

def setup(bot):
    bot.add_cog(MessageMover(bot))
