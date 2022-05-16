import json
import os
from datetime import datetime

import discord
import feedparser
from discord.ext import commands, tasks
from ..util import ID

c_sandbox: discord.TextChannel

class WikiRss(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        global c_sandbox
        c_sandbox = self.bot.get_channel(ID.SANDBOX)

        if not self.check_wiki.is_running():
            self.check_wiki.start()

    @tasks.loop(minutes=5)
    async def check_wiki(self):

        with open("./last_info/wiki_rss.json", encoding="utf-8") as f:
            last_json = json.load(f)

        feed = feedparser.parse(os.getenv("WIKI_RSS_URL"))

        for item in reversed(feed.entries):
            last_mod = datetime.strptime(
                last_json["last_modified"], "%a, %d %b %Y %X JST")
            time_mod = datetime.strptime(
                item.description, "%a, %d %b %Y %X JST")
            if last_mod < time_mod:
                last_json["last_modified"] = item.description
                await c_sandbox.send(
                    time_mod.strftime("%Y/%m/%d %A %H:%M:%S")+"に「" +
                    item.title.replace("_", "\\_")+"」が編集されました。\n"+item.link
                )

        with open("./last_info/wiki_rss.json", mode="w", encoding="utf-8") as f:
            f.write(json.dumps(last_json, ensure_ascii=False))


def setup(bot: discord.Bot):
    bot.add_cog(WikiRss(bot))
