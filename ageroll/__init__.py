from redbot.core.bot import Red
from .ageroll import AGERoll


def setup(bot: Red):
    bot.add_cog(AGERoll(bot))
