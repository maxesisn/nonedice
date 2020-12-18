import traceback
from ..config_master import COCConfig

config = COCConfig()
p: str = config.personalization


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
    try:
        config.clr("profile", group_id, player_id)
        return p["删除信息成功"].replace("{信息}", "玩家档案")
    except:
        return p["未知错误"]


async def delete_profile_element(group_id, player_id, elements):
    profile_config = config.get("profile", group_id, player_id)
    elements_list = elements.split(" ")
    for element in elements_list:
        if profile_config[element] is not None:
            profile_config.pop(element, None)
        else:
            return p["删除信息失败"].replace("{信息}", "属性值").replace("{原因}", "属性不存在于档案")
    config.set("profile", profile_config, group_id, player_id)
    return p["删除信息成功"].replace("{信息}", elements_list)


async def show_profile(group_id, player_id, elements="", ALL=False):
    profile_config = config.get("profile", group_id, player_id)
    if ALL is True:
        try:
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
    profile_config = config.get("profile", group_id, player_id)
    if isinstance(info, str):
        info = await resolve_info(info)
    if info is None:
        return p["数值不合法"].replace("{信息}", "数值表达式")
    try:
        profile_config.update(info)
        config.set("profile", profile_config, group_id, player_id)
        return p["保存信息成功"].replace("{信息}", "属性值")
    except:
        print(traceback.format_exc())
        return p["未知错误"]
