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
        outcome = None

        if total >= target_number:
            if dice[0] == dice[1] or dice[0] == dice[2] or dice[1] == dice[2]:
                stunt_points = dice[0]
            if dice[0] == 6 and dice[1] == 6 and dice[2] == 6:
                outcome = "Legendary Success!"
            else:
                outcome = "Success!"
        else:
            if dice[0] == 1 and dice[1] == 1 and dice[2] == 1:
                outcome = "Catastrophic Botch!"
            else:
                if dice[0] == dice[1] or dice[0] == dice[2] or dice[1] == dice[2]:
                    outcome = "Botch!"
                else:
                    outcome = "Failure!"

        # Create the table
        table = f"```\n" \
                 f"{'Outcome':<15}: {outcome}\n" \
                 f"{'Target Number':<15}: {target_number}\n" \
                 f"{'Stunt Die':<15}: {dice[0]}\n" \
                 f"{'2nd Die':<15}: {dice[1]}\n" \
                 f"{'3rd Die':<15}: {dice[2]}\n" \
                 f"{'Modifier':<15}: {modifier}\n" \
                 f"{'Total':<15}: {total}\n" \
                 f"```"

        await ctx.send(table)

        if stunt_points is not None:
            await ctx.send(f"Stunt Points: {stunt_points}")

def setup(bot):
    bot.add_cog(AGERoll(bot))
