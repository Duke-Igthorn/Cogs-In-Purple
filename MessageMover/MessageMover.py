import discord
from redbot.core import commands
from typing import List, Tuple
import asyncio

class MessageMover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def msgmvr(self, ctx, dest_channel: discord.TextChannel, *message_ids: str):
        ranges, singles, invalid = self.parse_message_ids(ctx, message_ids)
        messages_to_delete = []
        messages_to_send = []
        for single in singles:
            try:
                message = await ctx.channel.fetch_message(single)
                messages_to_delete.append(message)
                messages_to_send.append(message)
            except discord.NotFound:
                invalid.append(str(single))
        for start, end in ranges:
            messages = await ctx.channel.history(limit=500).flatten()
            messages_to_move = []
            for message in messages:
                if message.id >= start and message.id <= end:
                    messages_to_move.append(message)
                    messages_to_delete.append(message)
                    messages_to_send.append(message)
            messages_to_move.reverse()
            await dest_channel.send(f"{len(messages_to_move)} messages being moved.")
            for message in messages_to_move:
                embed = discord.Embed(description=message.content, timestamp=message.created_at)
                embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
                await dest_channel.send(embed=embed)

        if len(invalid) > 0:
            invalid_message = f"The following message IDs are invalid: {', '.join(invalid)}"
            await ctx.send(invalid_message)
        else:
            await ctx.message.add_reaction("\u2705") # green checkmark
            await ctx.message.add_reaction("\u274C") # red X

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ['\u2705', '\u274C']
            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
            except asyncio.TimeoutError:
                pass
            else:
                if str(reaction.emoji) == '\u2705':
                    await dest_channel.delete_messages(messages_to_send)
                    await ctx.channel.delete_messages(messages_to_delete + [ctx.message])
                elif str(reaction.emoji) == '\u274C':
                    await ctx.message.clear_reactions()

    def parse_message_ids(self, ctx, message_ids: List[str]) -> Tuple[List[Tuple[int, int]], List[int], List[str]]:
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
