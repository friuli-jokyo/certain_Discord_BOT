import discord
import odpt2jre
import odpttraininfo as odpt
from discord.commands import Option, slash_command
from discord.ext import commands

from ..util import train_info


def get_odpt_line_list():
    info_list = odpt.fetch_info()
    return [ info.get_line() for info in info_list ]

def get_jre_line_list():
    info_list = odpt2jre.fetch_info()
    return [ info["lineName"]["id"] for info in info_list ]

class TrainInfo(commands.Cog):

    def __init__(self, bot:discord.Bot):
        self.bot = bot

    @slash_command(description="公共交通オープンデータセンターの情報をそのまま返します")
    async def odpt_embed(
        self,
        ctx: discord.ApplicationContext,
        line: Option(str, "select line", choices=get_odpt_line_list())
    ):
        for info in odpt.fetch_info():
            if line == info.get_line():
                embed = train_info.build_embed_from_odpt(info)
                await ctx.respond(embed=embed)
                break

    @slash_command(description="JR東日本で使われている運行情報風に変換します")
    async def jre_embed(
        self,
        ctx: discord.ApplicationContext,
        line: Option(str, "select line", choices=get_jre_line_list())
    ):
        for info in odpt2jre.fetch_info():
            if line == info["lineName"]["id"]:
                embed = train_info.build_embed_from_jre(info)
                await ctx.respond(embed=embed)
                break


def setup(bot:discord.Bot):
    bot.add_cog(TrainInfo(bot))