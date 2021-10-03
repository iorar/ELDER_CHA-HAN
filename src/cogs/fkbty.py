import asyncio

import discord
from discord.ext import commands
from discord.ext.commands.core import command


class fkbty(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="fkbt", aliases=["fukubutyo"])
    async def _fkbty(self, ctx, arg):
        """Return your word!"""
        print("ふくぶちょーだいすき")
        await ctx.send(arg)


def setup(bot: commands.Bot):
    bot.add_cog(fkbty(bot))
