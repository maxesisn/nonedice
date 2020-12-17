import traceback
from .config_master import GeneralConfig

config = GeneralConfig()
p: dict = config.personalization


async def get_player_name(group_id, player_id):
    player_config = config.get("player", group_id, player_id)
    if "nickname" in player_config:
        return player_config["nickname"]
    else:
        return None


async def set_player_name(group_id, player_id, nickname):
    player_config = config.get("player", group_id, player_id)
    try:
        if nickname == "":
            player_config.pop("nickname", None)
            config.set("player", player_config, group_id, player_id)
            return p["删除信息成功"].replace("{信息}", "昵称")
        player_config["nickname"] = nickname
        config.set("player", player_config, group_id, player_id)
        return p["保存信息成功"].replace("{信息}", f"昵称为{nickname}")
    except:
        print(traceback.format_exc())
        return p["未知错误"]
