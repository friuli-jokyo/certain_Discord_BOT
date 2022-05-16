#!/usr/bin/env python3.10

import logging
import os

import discord
from core.util import ID

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    try:
        bot = discord.Bot(debug_guilds=[ID.GUILD])

        bot.load_extension("core.Cogs.wiki_rss")
        bot.load_extension("core.Cogs.train_info_commands")

        bot.run(os.getenv("BOT_TOKEN"))
    finally:
        pass