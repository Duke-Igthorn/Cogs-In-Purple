from .MessageMover import MessageMover

async def setup(bot):
    await bot.add_cog(MessageMover(bot))
