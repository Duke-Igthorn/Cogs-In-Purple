import random
from redbot.core import commands

class AGERoll(commands.Cog):
    # Emoji IDs
    emoji_ids = {
        'D6_1': '1178989224226205777',
        'D6_2': '1178989225543221268',
        'D6_3': '1178989227812343808',
        'D6_4': '1178989229360029736',
        'D6_5': '1178989231427821588',
        'D6_6': '1178989232702902303',
        'stunt_D6_1': '1178989234099589200',
        'stunt_D6_2': '1178989236586815538',
        'stunt_D6_3': '1178989237941567550',
        'stunt_D6_4': '1178989239896121354',
        'stunt_D6_5': '1178989506720964649',
        'stunt_D6_6': '1178989241800339516'
    }

    @staticmethod
    def roll_dice():
        return random.randint(1, 6)

    @staticmethod
    def dice_emoji(value, is_stunt=False):
        prefix = "stunt_" if is_stunt else ""
        emoji_name = f"{prefix}D6_{value}"
        emoji_id = AGERoll.emoji_ids[emoji_name]
        return f"<:{emoji_name}:{emoji_id}>"

    @commands.command()
    async def ageroll(self, ctx, target_number: int = 11, modifier: int = 0):
        dice = [self.roll_dice(), self.roll_dice(), self.roll_dice()]
        total = sum(dice) + modifier
        stunt_points = None
        outcome = None

        # Determine the outcome
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

        # Dice emojis
        dice_emojis = f"{self.dice_emoji(dice[0], is_stunt=True)} {self.dice_emoji(dice[1])} {self.dice_emoji(dice[2])}"

        # Result message
        result_message = f"{dice_emojis}\n\n" \
                         f"**Total:** `{total}`\n" \
                         f"**Target Number (TN):** `{target_number}`\n" \
                         f"**Outcome:** {outcome}\n"

        if stunt_points is not None:
            result_message += f"**Stunt Points:** `{stunt_points}`"

        await ctx.send(result_message)

def setup(bot):
    bot.add_cog(AGERoll(bot))
