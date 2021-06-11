import asyncio
import random
import string

import discord
from discord.ext import commands
from discord.ext.commands.core import command


class dxdice(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="dxdice", aliases=["dx"])
    async def starter(self, ctx, s):
        self.raw = s.replace(" ", "")
        self.script = self.raw
        self.diceresult = []

        ret = self.calc(self.raw)
        self.script = self.script + " -> " + str(ret)
        for item in self.diceresult:
            await ctx.send(item)
        await ctx.send(self.script)

    # 式全体を処理する関数
    # 加法と減法を処理
    def calc(self, s):
        """dxdices"""
        ret = 0
        if "-" in s:
            a = s.split("-")
            ret += self.calc(a[0])
            for item in a[1:]:
                ret -= self.calc(item)
            self.result = ret
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
        # if "*" in s :
        #   a = s.split("*")
        #   for item in a :
        #     ret *= self.term(item)
        #   return ret
        # if "/" in s :
        #   a = s.split("/")
        #   ret += a[0]
        #   for item in a[1:] :
        #     ret /= self.term(item)
        #   return ret
        if "c" in s:
            a = self.critical(s, 0)
            self.script = self.script.replace("add", str(a))
            return a
        return int(s)

    # ダイスを振る関数
    # ダイス部分を処理
    def critical(self, s, rn):
        dicenum, crnum = s.split("c")
        dicenum = int(dicenum)
        crnum = int(crnum)
        roll = 0
        ret = 0
        prscript = []
        prstr = []
        for i in range(dicenum):
            a = random.randint(1, 10)
            prscript.append(a)
            if a >= ret:
                ret = a
            if a >= crnum:
                roll += 1
        for item in prscript:
            if item >= crnum:
                prstr.append("**" + str(item) + "**")
            else:
                prstr.append(str(item))
        if roll > 0:
            self.diceresult.append(
                "->"
                + "{:3d}".format(rn * 10)
                + " + ("
                + ",".join(prstr)
                + ")"
                + self.script.replace(s, "", 1)
            )
            self.script = self.script.replace(s, str(roll) + "c" + str(crnum), 1)
            return 10 + self.critical(str(roll) + "c" + str(crnum), rn + 1)
        self.script = self.script.replace(
            s,
            "->"
            + "{:3d}".format(rn * 10)
            + " + ("
            + ",".join(prstr)
            + ") "
            + self.script.replace(s, "", 1)
            + " -> add",
            1,
        )
        return ret


def setup(bot: commands.Bot):
    bot.add_cog(dxdice(bot))
