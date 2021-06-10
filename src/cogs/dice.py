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
    async def starter(self, ctx, s):
        self.raw = s.replace(" ", "")
        self.script = self.raw

        self.result = self.calc(s)
        self.script = self.script.replace("*", "\*")
        await ctx.send(s + " -> " + self.script + " -> " + str(self.result))

    def calc(self, s):
        """dices"""
        ret = 0
        if "-" in s:
            a = s.split("-")
            ret += self.calc(a[0])
            for item in a[1:]:
                ret -= self.calc(item)
            return ret
        if "+" in s:
            a = s.split("+")
            for item in a:
                ret += self.term(item)
            return ret
        return self.term(s)

    # 式を部分で処理する関数
    # 乗法と除法を処理
    def term(self, s):
        ret = 1
        if "*" in s:
            a = s.split("*")
            for item in a:
                ret *= self.term(item)
            return ret
        if "/" in s:
            a = s.split("/")
            ret *= a[0]
            for item in a[1:]:
                ret /= self.term(item)
            return ret
        if "d" in s:
            return self.dice(s)
        return int(s)

    # ダイスを振る関数
    # ダイス部分を処理
    def dice(self, s):
        dicenum, sidenum = s.split("d")
        ret = 0
        prscript = []
        for i in range(int(dicenum)):
            a = random.randint(1, int(sidenum))
            prscript.append(a)
            ret += a
        prscript = [str(i) for i in prscript]
        self.script = self.script.replace(s, "(" + ",".join(prscript) + ")", 1)
        return ret


def setup(bot: commands.Bot):
    bot.add_cog(Dice(bot))
