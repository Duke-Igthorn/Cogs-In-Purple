import random
from redbot.core import commands

class AGERoll(commands.Cog):
    @staticmethod
    def roll_dice():
        return random.randint(1, 6)
        
    @commands.command()
    async def ageroll(self, ctx, target_number: int = 11, modifier: int = 0):
        if not isinstance(target_number, int) or not isinstance(modifier, int):
            await ctx.send("Both target number and modifier need to be integers.")
            return

        dice = [self.roll_dice(), self.roll_dice(), self.roll_dice()]
        total = sum(dice) + modifier
        stunt_points = None

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

        await ctx.send(f"Target Number: {target_number}\nStunt Die: {dice[0]}\nDie 2    : {dice[1]}\nDie 3    : {dice[2]}\nModifier: {modifier}\nTotal: {total}")
        if stunt_points is not None:
            await ctx.send(f"Stunt Points: {stunt_points}")

def setup(bot):
    bot.add_cog(AGERoll(bot))
