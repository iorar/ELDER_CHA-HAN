import asyncio

import discord
from discord.ext import commands
from discord.ext.commands.core import command


class Hello(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="hello", aliases=["hi"])
    async def _hello(self, ctx):
        """Return "hello"!"""
        await ctx.send("hello, Cog!")


def setup(bot: commands.Bot):
    bot.add_cog(Hello(bot))
