import random
from redbot.core import commands

class AGERoll(commands.Cog):
    @commands.command()
    async def ageroll(self, ctx, target_number: int = 11, modifier: int = 0):
        def roll_dice():
            return random.randint(1, 6)
        
        dice = [roll_dice(), roll_dice(), roll_dice()]
        total = sum(dice) + modifier
        if total >= target_number:
            if dice[0] == dice[1] or dice[0] == dice[2] or dice[1] == dice[2]:
                stunt_points = dice[0]
            if dice[0] == 6 and dice[1] == 6 and dice[2] == 6:
                await ctx.send("Legendary Success!")
            else:
                await ctx.send("Success!")
        else:
            if dice[0] == 1 and dice[1] == 1 and dice[2] == 1:
                await ctx.send("Catastrophic Botch!")
            else:
                if dice[0] == dice[1] or dice[0] == dice[2] or dice[1] == dice[2]:
                    await ctx.send("Botch!")
                else:
                    await ctx.send("Failure!")
        await ctx.send(f"Stunt Die: {dice[0]}\nDie 2    : {dice[1]}\nDie 3    : {dice[2]}\nTotal: {total}")
        if "stunt_points" in locals():
            await ctx.send(f"Stunt Points: {stunt_points}")

def setup(bot):
    bot.add_cog(AGERoll())
