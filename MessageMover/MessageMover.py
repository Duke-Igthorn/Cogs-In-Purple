import discord
import asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

class MessageMover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    MAX_BATCH_SIZE = 10  # Maximum number of messages to move in one batch
    MAX_EMBED_DESCRIPTION_SIZE = 2048  # Maximum characters for an embed description

    @cog_ext.cog_slash(
        name="move",
        description="Move messages to another channel",
        options=[
            create_option(
                name="channel",
                description="The channel to move messages to",
                option_type=7,  # Channel type
                required=True
            ),
            create_option(
                name="message_ids",
                description="IDs of the messages to move",
                option_type=3,  # String type, as slash commands do not support variadic arguments
                required=True
            ),
        ]
    )
    async def _move_messages(self, ctx: SlashContext, channel: discord.TextChannel, message_ids: str):
        # Parse the message IDs from the string
        try:
            message_ids = [int(id.strip()) for id in message_ids.split(",")]
        except ValueError:
            await ctx.send("Error: Invalid message IDs. Please enter a comma-separated list of IDs.")
            return

        if len(message_ids) > self.MAX_BATCH_SIZE:
            await ctx.send(f'🚨 This command is limited to moving {self.MAX_BATCH_SIZE} messages at a time to avoid rate limiting issues. Please split your request into smaller batches.')
            return

        for message_id in message_ids:
            try:
                message = await ctx.channel.fetch_message(message_id)
                content = message.content
                while content:
                    embed_content = content[:self.MAX_EMBED_DESCRIPTION_SIZE]
                    content = content[self.MAX_EMBED_DESCRIPTION_SIZE:]

                    embed = discord.Embed(description=embed_content, color=0x3498db)
                    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
                    await channel.send(embed=embed)

                await message.delete()
            except discord.NotFound:
                await ctx.send(f'Message with ID {message_id} not found.')
            except discord.Forbidden:
                await ctx.send('I do not have permission to perform this action.')
            except discord.HTTPException as e:
                await ctx.send(f'Failed to move message: {e}')

        completion_message = await channel.send('✅ Move complete. You can now resume posting messages.')
        await asyncio.sleep(20)
        await completion_message.delete()

def setup(bot):
    bot.add_cog(MessageMover(bot))
