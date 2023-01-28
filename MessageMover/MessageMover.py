import asyncio
import datetime
from redbot.core import commands
import discord

class MessageMover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def msgmvr(self, ctx, destination: discord.TextChannel, *message_ids: int):
        if not message_ids:
            return await ctx.send("Please provide at least one message ID to move.")
        
        if not destination:
            return await ctx.send("Please provide a destination channel to move the messages to.")
        
        messages = []
        for message_id in message_ids:
            message = await ctx.channel.fetch_message(message_id)
            if message:
                messages.append(message)
            else:
                return await ctx.send(f"Could not find a message with the ID {message_id}. Please check that the ID is correct.")
        
        messages.sort(key=lambda x: x.created_at)
        
        for message in messages:
            await message.pin()
            await message.unpin()
            await message.delete()
            await destination.send(content=message.content,
                                   embed=message.embeds[0] if message.embeds else None,
                                   files=[discord.File(await message.attachments[0].to_file(), filename=message.attachments[0].filename) ] if message.attachments else None,
                                   allowed_mentions=discord.AllowedMentions(users=False, roles=False, everyone=False),
                                   author=message.author)

def setup(bot):
    bot.add_cog(MessageMover(bot))
