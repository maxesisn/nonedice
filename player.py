import traceback
import datetime
import random
from .config_master import Config

p: str = Config("static").load("personalization")


async def get_player_name(group_id, player_id):
    player_config = Config(group_id).load(player_id)
    if "nickname" in player_config:
        return player_config["nickname"]
    else:
        return None


async def set_player_name(group_id, player_id, nickname):
    config = Config(group_id)
    player_config = config.load(player_id)
    try:
        if nickname == "":
            player_config.pop("nickname", None)
            config.save()
            return p["删除信息成功"].replace("{信息}", "昵称")
        player_config["nickname"] = nickname
        config.save()
        return p["保存信息成功"].replace("{信息}", f"昵称为{nickname}")
    except:
        print(traceback.format_exc())
        return p["未知错误"]


async def jrrp(player_id):
    config = Config("global")
    player_id=str(player_id)
    jrrp_config = config.load("jrrp")
    print(player_id, jrrp_config.keys())
    if player_id in jrrp_config.keys():
        if jrrp_config[player_id]["date"] == datetime.date.today().strftime("%d"):
            return jrrp_config[player_id]["value"]
    jrrp_config[player_id]={}
    jrrp_config[player_id]["value"] = random.randint(1, 100)
    jrrp_config[player_id]["date"] = datetime.date.today().strftime("%d")
    config.save()
    return jrrp_config[player_id]["value"]
