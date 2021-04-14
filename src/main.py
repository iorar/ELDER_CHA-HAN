import asyncio
import logging
import os
import random
from pathlib import Path

import discord
from discord.ext import commands

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


class TestBot(commands.Bot):
    def __init__(self, command_prefix) -> None:
        super().__init__(command_prefix)

        in_cogs_folder = Path(__file__).parent / "cogs"
        # [cogs.ファイル名〜]
        cogs_list = [
            ("cogs." + x.stem) for x in in_cogs_folder.iterdir() if x.is_file()
        ]
        for cog in cogs_list:
            self.load_extension(cog)  # cogのロード

    async def on_ready(self):
        print("Logged in as {}.".format(self.user.name))


if __name__ == "__main__":
    bot = TestBot(command_prefix=".")

    # tokenの読み込みとbotの実行
    discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
    # ブロッキング関数なのでこれ以降に書かれたコードはbotが終了（ログアウト）してから実行される
    bot.run(discord_bot_token)
