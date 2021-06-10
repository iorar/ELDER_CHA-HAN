import asyncio
import os
import random
from pathlib import Path

import discord
from discord.ext import commands


class ReloadCogs(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="reloadallcog", aliases=["rac"])
    async def reloadcog(self, ctx):
        """Reload all Cogs"""

        in_cogs_folder = Path(__file__).parent
        # [cogs.ファイル名〜]
        cogs_list = [
            ("cogs." + x.stem) for x in in_cogs_folder.iterdir() if x.is_file()
        ]
        embed = discord.Embed(title="Reload cogs")
        for cog in cogs_list:
            try:
                self.bot.reload_extension(cog)  # cogのリロード

                embed.add_field(name=f"ok: {cog}", value="done.", inline=False)
                await asyncio.sleep(0.5)
            except Exception as e:
                embed.add_field(name="ok: {cog}", value=e, inline=False)

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(ReloadCogs(bot))
