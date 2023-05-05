import datetime
import re
from redbot.core import commands

class CliveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.memorized_message = None

    @commands.command()
    async def clive(self, ctx):
        if ctx.channel.name.lower() != "live":
            await ctx.send("This command can only be used in the `live` channel.")
            return

        # Get the first message in the channel
        async for message in ctx.channel.history(limit=1, oldest_first=True):
            first_message = message
            break
        self.memorized_message = first_message.content if first_message else None
        if self.memorized_message is None:
            await ctx.send("No message to remember.")
            return

        # Delete all messages in the channel
        await ctx.channel.purge(limit=None)

        # Get the date 7 days from now at 1AM UTC+2
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        days_ahead = 7 - now.weekday()
        next_monday = now + datetime.timedelta(days=days_ahead)
        next_monday = next_monday.replace(hour=1, minute=0, second=0, microsecond=0)

        # Format the timestamp in the desired format
        timestamp = int(next_monday.timestamp())
        timestamp_str = f"<t:{timestamp}:F>"
        
        # Replace the existing timestamp with the new timestamp
        self.memorized_message = re.sub(r"<t:\d+:F>", timestamp_str, self.memorized_message)
        
        # If the message still doesn't have timestamp, add it to the end
        if "<t:" not in self.memorized_message:
            self.memorized_message += timestamp_str
        
        # Send the memorized message with the new timestamp
        await ctx.send(f"{self.memorized_message}")


async def setup(bot):
    await bot.add_cog(CliveCog(bot))
