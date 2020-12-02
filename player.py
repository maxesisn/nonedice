import os
import json
import traceback

fd = os.path.dirname(__file__)
try:
    with open(os.path.join(fd, "config/player.json"), "r") as f:
        player_config = json.load(f)
except:
    player_config = {}


async def save_config(data):
    try:
        with open(os.path.join(fd, "config/player.json"), "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(e)


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
            player_config[group_id][player_id].pop("nickname",None)
            await save_config(player_config)
            return "删除昵称成功"
        player_config[group_id][player_id]["nickname"] = nickname
        await save_config(player_config)
        return f"设置昵称为{nickname}成功"
    except:
        return f"出现未知错误{traceback.format_exc()}"
