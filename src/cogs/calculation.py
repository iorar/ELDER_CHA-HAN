import asyncio
from os import chdir

import discord

# import functionparser as funcps
from discord.ext import commands
from discord.ext.commands.core import command
from lark import Lark

import output
import transformer


class parsetree(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        chdir("../")
        self.bot = bot

        # 文法を読み込む
        with open("grammar.lark", encoding="utf-8") as self.grammar:
            self.LP = Lark(self.grammar.read(), start="program")

        # 保持するenvlistの生成 keyは環境名、valueはEnvironmentクラス
        self.envlist = dict()
        self.envlist["main"] = transformer.Environment(None)

        # 現在使用している環境名
        self.nowenv = "main"

        # 環境に合わせて使うトランスフォーマ
        self.trans = transformer.my_transformer(self.envlist.get(self.nowenv))

    # envの選択を行う関数
    @commands.command(name="environment", aliases=["env"])
    async def chose_env(self, ctx, *arg):
        ret = ""
        if len(arg) == 0:
            ret += "```\nEnvironment list:\n"
            # envlist の一覧を表示
            for key in self.envlist.keys():
                ret += "    " + key + "\n"
            ret += "```"
        else:
            envname = self.envlist.get(arg[0], None)
            if envname is None:
                ret += "```\n There is no such environment.\n If you want to make new environment, pleae use [.newenv] command.\n```"
            else:
                self.nowenv = arg
                ret += "```\nNow environment [ " + arg[0] + " ] is in used.\n```"
        await ctx.send(ret)

    # 新しい環境を生成する関数
    @commands.command(name="newenv", aliases=["ne"])
    async def make_env(self, ctx, arg):
        ret = "```\n"
        if self.envlist.get(arg) is None:
            self.envlist[arg] = transformer.Environment(None)
            ret += "A new environment [ " + arg + " ] is created.\n"
        else:
            ret += "The environment [ " + arg + " ] is already existed.\n"
        self.nowenv = arg
        ret += "Now environment [ " + arg + " ] is in used.\n```"
        await ctx.send(ret)

    @commands.command(name="calculation", aliases=["c"])
    async def calculation(self, ctx, arg):
        # テスト用プログラムを読み込む
        # program = open("dxdice-for-calc.txt").read()
        # トランスフォーマを現在の環境用に変更
        self.trans = transformer.my_transformer(self.envlist.get(self.nowenv))
        # tree = self.LP.parse(program)
        # ret = self.trans.program(tree)
        tree = self.LP.parse(arg)
        ret = self.trans.program(tree)
        ret = "```\n" + self.trans.env.outbuf.printed + "\n```"
        await ctx.send(ret)
        self.trans.env.outbuf.printclear()


def setup(bot: commands.Bot):
    bot.add_cog(parsetree(bot))
