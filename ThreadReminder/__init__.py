from .ThreadReminder import ThreadReminder

async def setup(bot):
    await bot.add_cog(ThreadReminder(bot))
