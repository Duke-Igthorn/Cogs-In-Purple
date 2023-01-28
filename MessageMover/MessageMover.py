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
            return await ctx.send("You must specify at least one message ID to move.")
        if not destination:
            return await ctx.send("You must specify a destination channel.")

        messages = []
        for message_id in message_ids:
            message = await ctx.channel.fetch_message(message_id)
            if message:
                messages.append(message)
            else:
                return await ctx.send(f"Could not find message with ID {message_id}.")
        
        messages.sort(key=lambda x: x.created_at)
        
        for message in messages:
            await message.pin()
            await message.unpin()
            await message.delete()
            sent_message = await destination.send(content=message.content,
                                   embed=message.embeds[0] if message.embeds else None,
                                   file=message.attachments[0].url if message.attachments else None,
                                   allowed_mentions=discord.AllowedMentions(users=False, roles=False, everyone=False))
            await sent_message.edit(content=message.content,
                                    embed=message.embeds[0] if message.embeds else None,
                                    file=message.attachments[0].url if message.attachments else None,
                                    allowed_mentions=discord.AllowedMentions(users=False, roles=False, everyone=False),
                                    author=message.author)

def setup(bot):
    bot.add_cog(MessageMover(bot))
