import discord
from redbot.core import commands

class MessageMover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="msgmvr")
    async def move_messages(self, ctx):
        await ctx.send("Please provide the message IDs or ranges to move (separated by commas):")
        msg_ids_input = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        msg_ids = []
        for msg_id in msg_ids_input.content.split(','):
            if '-' in msg_id:
                range_start, range_end = map(int, msg_id.split('-'))
                msg_ids += [i for i in range(range_start, range_end+1)]
            else:
                msg_ids.append(int(msg_id))

        await ctx.send("Please provide the destination channel:")
        dest_channel_input = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        dest_channel = discord.utils.get(ctx.guild.channels, name=dest_channel_input.content)

        if dest_channel is None or not isinstance(dest_channel, discord.TextChannel):
            await ctx.send("Invalid channel name. Please try again.")
            return

        for msg_id in msg_ids:
            message = await ctx.channel.fetch_message(msg_id)
            if message is None:
                await ctx.send(f"Message with ID {msg_id} not found.")
                continue

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
