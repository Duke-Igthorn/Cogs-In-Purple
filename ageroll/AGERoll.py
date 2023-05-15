import random
from discord import Embed, Color
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

        # Create the embed
        embed = Embed(
            title="AGE Roll",
            description=f"**Outcome**       : {outcome}\n"
                        f"**Target Number** : {target_number}\n"
                        f"**Stunt Die**     : {dice[0]}\n"
                        f"**2nd Die**       : {dice[1]}\n"
                        f"**3rd Die**       : {dice[2]}\n"
                        f"**Modifier**      : {modifier}\n"
                        f"**Total**         : {total}",
            color=Color.blue()
        )

        if stunt_points is not None:
            embed.add_field(name="Stunt Points", value=str(stunt_points))

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(AGERoll(bot))
