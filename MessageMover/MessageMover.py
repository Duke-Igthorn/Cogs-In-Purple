import asyncio
import datetime
from redbot.core import commands

class MessageMover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def msgmove(self, ctx, message_id: int, destination: discord.TextChannel, *message_ids: int):
        # Fetch the original message by ID
        message = await ctx.channel.fetch_message(message_id)

        # Add the original message to the destination channel
        await destination.send(f"{message.author.mention} said at {message.created_at}:\n{message.content}")

        # Delete the original message
        await message.delete()

        if message_ids:
            # Fetch all additional messages by ID
            messages = await ctx.channel.fetch_messages(message_ids)

            # Sort messages by their creation time
            messages = sorted(messages, key=lambda m: m.created_at)

            # Add all additional messages to the destination channel
            for message in messages:
                await destination.send(f"{message.author.mention} said at {message.created_at}:\n{message.content}")

            # Delete all additional messages
            await ctx.channel.delete_messages(messages)


def setup(bot):
    bot.add_cog(MessageMover(bot))
