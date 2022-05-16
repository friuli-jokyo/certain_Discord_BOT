import copy
import json
import os
import discord

import odpttraininfo as odpt

from odpt2jre.intermediate_components.output_dict import TrainInformationDict


with open( "./static/color.json" ) as f:
	_colorDict:dict[str,str] = json.load(f)

def get_line_color(line: str) -> int|None:

    try:
        return int( _colorDict[ line ].replace("#","") ,16 )
    except:
        return None

_extra_keys = {
    "odpt:trainInformationStatus": "状況",
    "odpt:trainInformationCause": "原因",
    "odpt:railDirection": "方向",
    "odpt:trainInformationArea": "エリア",
    "odpt:trainInformationKind": "種類",
    "odpt:stationFrom": "起点",
    "odpt:stationTo": "終点",
    "odpt:trainInformationRange": "区間",
    "odpt:trainInformationCause": "原因",
    "odpt:transferRailways": "振替",
    "odpt:resumeEstimate": "復旧見込み"
}

def build_embed_from_jre(info_raw:TrainInformationDict) -> discord.Embed:

    info = copy.deepcopy(info_raw)

    color:int|None = get_line_color( info["lineName"]["id"] )
    description:str = "\n".join(list(info["infoText"].values()))

    if color:
        embed = discord.Embed( description=description, color=color )
    else:
        embed = discord.Embed( description=description )

    embed.set_author(name=info["lineName"]["ja"],icon_url="{}/LINEicon/{}.png".format(os.getenv("IMG_URL"),info["lineName"]["id"]))
    embed.set_thumbnail(
					url="{}/status/{}.png".format(os.getenv("IMG_URL"),info["infoStatusIcon"])
	)

    try:
        info["infoStatus"].pop("id",None)
        if not str.isspace(" ".join(info["infoStatus"].values())):
            embed.add_field( name="状況", value=" ".join(info["infoStatus"].values()), inline=True )
    except:
        pass

    try:
        info["cause"].pop("id",None)
        if not str.isspace(" ".join(info["cause"].values())):
            embed.add_field( name="原因", value=" ".join(info["cause"].values()), inline=True )
    except:
        pass

    return embed


def build_embed_from_odpt(info: odpt.TrainInformation) -> discord.Embed:

    info_dict = info.to_dict()

    line: str = info.get_line()
    color:int|None = get_line_color( line )
    description:str = "\n".join(list(info_dict["odpt:trainInformationText"].values()))

    if color:
        embed = discord.Embed( description=description, color=color )
    else:
        embed = discord.Embed( description=description )

    embed.set_author(name=line)

    for key in _extra_keys:
        if key in info_dict:
            if type(info_dict[key]) == str:
                value = info_dict[key]
            else:
                try:
                    value = " ".join(list(info_dict[key].values()))
                except:
                    try:
                        value = " ".join(info_dict[key])
                    except:
                        value = str(info_dict[key])
            embed.add_field( name=_extra_keys[key], value=value )

    return embed

if __name__ == "__main__":
    print(_colorDict)