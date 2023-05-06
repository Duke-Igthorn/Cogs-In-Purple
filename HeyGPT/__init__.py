from .HeyGPT import HeyGPT

async def setup(bot):
    await bot.add_cog(HeyGPT(bot))
