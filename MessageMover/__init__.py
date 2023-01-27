from .MessageMover import MessageMover

def setup(bot):
    bot.add_cog(MessageMover(bot))
