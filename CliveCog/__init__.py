from .CliveCog import CliveCog

async def setup(bot):
    await bot.add_cog(CliveCog(bot))
