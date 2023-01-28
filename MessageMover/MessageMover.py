import asyncio
import datetime
from redbot.core import commands
import discord

class MessageMover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def msgmvr(self, ctx, destination: discord.TextChannel, *message_ids: int):
        messages = []
        for message_id in message_ids:
            message = await ctx.channel.fetch_message(message_id)
            messages.append(message)
        
        messages.sort(key=lambda x: x.created_at)
        
        for message in messages:
            await message.pin()
            await message.unpin()
            await message.delete()
            
            # Create webhook with name and avatar of original message's author
            webhook = await destination.create_webhook(name=message.author.name, avatar=message.author.avatar_url)
            
            # Send message with webhook
            await webhook.send(content=message.content,
                               embeds=message.embeds,
                               files=[await a.to_file() for a in message.attachments],
                               allowed_mentions=discord.AllowedMentions(users=False, roles=False, everyone=False))
            
            # Delete webhook
            await webhook.delete()

def setup(bot):
    bot.add_cog(MessageMover(bot))
