import asyncio

import discord
from discord.ext import commands
from discord.ext.commands.core import command


class fkbty(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="fkbt", aliases=["fukubutyo"])
    async def _fkbty(self, ctx):
        """All of us loves FUKUBUTYO."""
        print("ふくぶちょーだいすき")
        await ctx.send("ふくぶちょーだいすき")


def setup(bot: commands.Bot):
    bot.add_cog(fkbty(bot))
