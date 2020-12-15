import traceback
from .config_master import GeneralConfig

config = GeneralConfig()
player_config = config.get("player_config")
p:str = config.get("personalization_config")


async def get_player_name(group_id, player_id):
    if group_id not in player_config:
        return None
    if player_id not in player_config[group_id]:
        return None
    print(player_config[group_id][player_id])
    if "nickname" in player_config[group_id][player_id]:
        return player_config[group_id][player_id]["nickname"]
    else:
        return None


async def set_player_name(group_id, player_id, nickname):
    try:
        if group_id not in player_config:
            player_config[group_id] = {}
        if player_id not in player_config[group_id]:
            player_config[group_id][player_id] = {}
        if nickname == p["删除信息成功"].replace("{信息}","昵称"):
            player_config[group_id][player_id].pop("nickname", None)
            config.saver()
            return 
        player_config[group_id][player_id]["nickname"] = nickname
        config.saver()
        return p["保存信息成功"].replace("{信息}", f"昵称为{nickname}")
    except:
        print(traceback.format_exc())
        return p["未知错误"]
