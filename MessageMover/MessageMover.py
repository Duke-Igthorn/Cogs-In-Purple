import discord
from redbot.core import commands

class MessageMover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="msgmvr")
    async def move_messages(self, ctx, dest_channel: discord.TextChannel, *message_ids: str):
        ranges = []
        singles = []
        for message_id in message_ids:
            if "-" in message_id:
                start_id, end_id = message_id.split("-")
                ranges.append((int(start_id), int(end_id)))
            else:
                singles.append(int(message_id))

        messages = []
        async for message in ctx.channel.history():
            for start_id, end_id in ranges:
                if start_id <= message.id <= end_id:
                    messages.insert(0, message)
                    break
            if message.id in singles:
                messages.insert(0, message)

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
