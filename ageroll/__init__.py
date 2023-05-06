from .AGERoll import AGERoll

async def setup(bot):
    await bot.add_cog(AGERoll())
