import asyncio

import discord
from discord.ext import commands
from discord.ext.commands.core import command


class Yama(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="yama", aliases=["yamabiko"])
    async def _yama(self, ctx, arg):
        """Return your word!"""
        await ctx.send(arg)


def setup(bot: commands.Bot):
    bot.add_cog(Yama(bot))
