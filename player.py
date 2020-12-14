import traceback
from .config_master import GeneralConfig

config = GeneralConfig()
player_config = config.get("player_config")


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
        if nickname == "":
            player_config[group_id][player_id].pop("nickname", None)
            config.saver()
            return "删除昵称成功"
        player_config[group_id][player_id]["nickname"] = nickname
        config.saver()
        return f"设置昵称为{nickname}成功"
    except:
        return f"出现未知错误{traceback.format_exc()}"
