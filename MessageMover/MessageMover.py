import discord
from redbot.core import commands

class MessageMover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="msgmvr")
    async def move_messages(self, ctx, dest_channel: discord.TextChannel, start_msg_id: int=None, end_msg_id: int=None, *message_ids: int):
        messages = []
        if start_msg_id is not None and end_msg_id is not None:
            async for message in ctx.channel.history():
                if message.id == start_msg_id:
                    messages.append(message)
                    break
                elif message.id == end_msg_id:
                    messages.append(message)
                    break
                elif start_msg_id < message.id < end_msg_id:
                    messages.append(message)
        elif start_msg_id is not None and end_msg_id is None:
            messages.append(await ctx.channel.fetch_message(start_msg_id))
        elif message_ids:
            for message_id in message_ids:
                message = await ctx.channel.fetch_message(message_id)
                if message is not None:
                    messages.append(message)
                else:
                    await ctx.send(f"Message with ID {message_id} not found.")
        else:
            await ctx.send("Please provide either a single message ID, a start and end message ID, or a comma separated list of message IDs.")

        if len(messages) == 0:
            await ctx.send("No messages found in the specified range.")
            return

        for message in messages:
            embed = discord.Embed(
                description=message.content,
                timestamp=message.created_at
            )
            embed.set_author(
                name=message.author.name,
                icon_url=message.author.avatar_url
            )

            if len(message.attachments) > 0:
                embed.set_image(url=message.attachments[0].url)

            await dest_channel.send(embed=embed)
            await message.delete()

        await ctx.send("Messages moved successfully.")

def setup(bot):
    bot.add_cog(MessageMover(bot))
