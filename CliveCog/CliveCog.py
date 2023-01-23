import datetime
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
        first_message = await ctx.channel.history(limit=1, oldest_first=True).flatten()
        self.memorized_message = first_message[0].content if first_message else None
        if self.memorized_message is None:
            await ctx.send("No message to remember.")
            return
        # Delete all messages in the channel
        await ctx.channel.purge(limit=None)

        # Get the date 7 days from now at midnight
        date = datetime.datetime.now().replace(hour=1, minute=0, second=0, microsecond=0) + datetime.timedelta(days=7)
        
        #Format the timestamp in the desired format
        timestamp = date.timestamp()
        timestamp_str = f"<t:{int(timestamp)}:f>"
        
        # Replace the existing timestamp with the new timestamp
        self.memorized_message = self.memorized_message.replace("<t:*", timestamp_str)
        
        # If the message still doesn't have timestamp, add it to the end
        if "<t:" not in self.memorized_message:
            self.memorized_message += timestamp_str
        
        # Send the memorized message with the new timestamp
        await ctx.send(f"{self.memorized_message}")


def setup(bot):
    bot.add_cog(CliveCog(bot))        
