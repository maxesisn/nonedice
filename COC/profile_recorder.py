import traceback
from ..config_master import Config

p: str = Config("static").load("personalization")


async def resolve_info(info):
    info_set = info.split(" ")
    new_info_dict = {}
    for per_info in info_set:
        per_info = per_info.replace('：', ':')
        per_info_list = per_info.split(':')
        try:
            new_info_dict[per_info_list[0]] = int(per_info_list[1])
        except:
            return None
    return new_info_dict


async def clear_profile(group_id, player_id):
    config = Config(group_id)
    player_config=config.load(player_id)
    if "profile" not in player_config:
        player_config["profile"]=dict()
    try:
        player_config.pop("profile", None)
        config.save()
        return p["删除信息成功"].replace("{信息}", "玩家档案")
    except:
        return p["未知错误"]


async def delete_profile_element(group_id, player_id, elements):
    config = Config(group_id)
    player_config = config.load(player_id)
    if "profile" not in player_config:
        player_config["profile"]=dict()
    elements_list = elements.split(" ")
    for element in elements_list:
        if player_config["profile"][element] is not None:
            player_config["profile"].pop(element, None)
        else:
            return p["删除信息失败"].replace("{信息}", "属性值").replace("{原因}", "属性不存在于档案")
    config.save()
    return p["删除信息成功"].replace("{信息}", "、".join(elements_list))


async def show_profile(group_id, player_id, elements="", ALL=False):
    profile_config=Config(group_id).load(player_id)["profile"]
    if ALL is True:
        try:
            # 暴力输出
            msg = str(profile_config).replace(
                '{', '').replace('}', '').replace('\'', '')
            return msg
        except:
            return p["获取信息失败"].replace("{信息}", "玩家档案")
    else:
        try:
            elements_list = elements.split(' ')
            msg = ""
            for element in elements_list:
                msg += element
                msg += ':'
                msg += profile_config[element]
                msg += ' '
            return msg
        except:
            return p["获取信息失败"].replace("{信息}", "已记录的属性")


async def add_profile(group_id, player_id, info):
    config = Config(group_id)
    player_config=config.load(player_id)
    if "profile" not in player_config:
        player_config["profile"]=dict()
    if isinstance(info, str):
        info = await resolve_info(info)
    if info is None:
        return p["数值不合法"].replace("{信息}", "数值表达式")
    try:
        player_config["profile"].update(info)
        config.save()
        return p["保存信息成功"].replace("{信息}", "属性值")
    except:
        print(traceback.format_exc())
        return p["未知错误"]
