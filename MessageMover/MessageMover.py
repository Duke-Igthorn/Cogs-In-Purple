import discord
from redbot.core import commands
from typing import List, Tuple
import asyncio

class MessageMover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="msgmvr")
    async def move_messages(self, ctx, dest_channel: discord.TextChannel, *message_ids: str):
        ranges, singles, invalid = self.parse_message_ids(message_ids)

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

        invalid_messages = []
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

            try:
                new_message = await dest_channel.send(embed=embed)
                await message.delete()
            except discord.errors.NotFound:
                invalid_messages.append(str(message.id))

        if len(invalid_messages) > 0:
            invalid_message = f"The following messages could not be moved: {', '.join(invalid_messages)}"
            await ctx.send(invalid_message)

        confirmation_message = await ctx.send("Messages moved successfully. Remove the command messages?")
        await confirmation_message.add_reaction("✅")
        await confirmation_message.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and reaction.message == confirmation_message

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
            if str(reaction.emoji) == "✅":
                messages_to_delete = [confirmation_message]
                async for message in ctx.channel.history(after=ctx.message):
                    if message.author == self.bot.user and message.id not in messages_to_delete:
                        messages_to_delete.append(message)
                for message in messages_to_delete:
                    try:
                        await message.delete()
                    except discord.errors.NotFound:
                        pass
                await ctx.message.delete()
        except asyncio.TimeoutError:
            pass

    def parse_message_ids(self, message_ids: List[str]) -> Tuple[List[Tuple[int, int]], List[int], List[str]]:
        ranges = []
        singles = []
        invalid = []
        for message_id in message_ids:
            if "-" in message_id:
                try:
                    start_id, end_id = message_id.split("-")
                    start_id = int(start_id)
                    end_id = int(end_id)
                    if start_id > end_id:
                        start_id, end_id = end_id, start_id
                    ranges.append((start_id, end_id))
                except ValueError:
                    invalid.append(message_id)
            else:
                try:
                    singles.append(int(message_id))
                except ValueError:
                    invalid.append(message_id)

        if len(invalid) > 0:
            invalid_message = f"The following message IDs are invalid: {', '.join(invalid)}"
            ctx.send(invalid_message)

        return ranges, singles, invalid

def setup(bot):
    bot.add_cog(MessageMover(bot))
