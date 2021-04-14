import asyncio
import random
import string

import discord
from discord.ext import commands
from discord.ext.commands.core import command


class Dice(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="dice", aliases=["d"])
    async def _hello(self, ctx, arg):
        """dices"""
        dicenum = arg.split("d")
        # ダイスを振る
        # dicenum[0]:振るダイスの数 dicenum[1]:何面ダイスを振るか
        dicecon = []
        for i in range(int(dicenum[0])):
            dicecon.append(random.randint(1, int(dicenum[1])))
        dicecon_str = [str(n) for n in dicecon]
        await ctx.send(
            "dice -> (" + ",".join(dicecon_str) + ") -> " + str(sum(dicecon))
        )


def setup(bot: commands.Bot):
    bot.add_cog(Dice(bot))
