import traceback
from ..config_master import COCConfig

config=COCConfig()
profile_config=config.get("coc_profile_config")
p:str = config.get("personalization_config")

async def resolve_info(info):
    info_set = info.split(" ")
    new_info_dict = {}
    for per_info in info_set:
        per_info = per_info.replace('：', ':')
        per_info_list = per_info.split(':')
        new_info_dict[per_info_list[0]] = per_info_list[1]
        if len(per_info_list) != 2:
            return None
    return new_info_dict


async def clear_profile(group_id, player_id):
    if group_id not in profile_config or player_id not in profile_config[group_id]:
        return p["获取信息失败"].replace("{信息}","个人昵称")

    try:
        profile_config[group_id][player_id] = None
        config.saver()
        return p["删除信息成功"].replace("{信息}","玩家档案")
    except:
        return p["未知错误"]


async def delete_profile_element(group_id, player_id, elements):
    elements_list = elements.split(" ")
    for element in elements_list:
        if profile_config[group_id][player_id][element] is not None:
            profile_config[group_id][player_id].pop(element,None)
        else:
            return p["删除信息失败"].replace("{信息}","属性值").replace("{原因}","属性不存在于档案")
    config.saver()
    return p["删除信息成功"].replace("{信息}",elements_list)


async def show_profile(group_id, player_id, elements="", ALL=False):
    if ALL is True:
        try:
            msg = str(profile_config[group_id][player_id]).replace(
                '{', '').replace('}', '').replace('\'', '')
            return msg
        except:
            return p["获取信息失败"].replace("{信息}","玩家档案")
    else:
        try:
            elements_list = elements.split(' ')
            msg = ""
            for element in elements_list:
                msg += element
                msg += ':'
                msg += profile_config[group_id][player_id][element]
                msg += ' '
            return msg
        except:
            return p["获取信息失败"].replace("{信息}","已记录的属性")


async def add_profile(group_id, player_id, info):
    info = await resolve_info(info)
    if info is None:
        return p["未知指令"]
    try:
        try:
            profile_config[group_id][player_id].update(info)
        except:
            profile_config[group_id]={}
            profile_config[group_id][player_id]={}
            profile_config[group_id][player_id].update(info)
        config.saver()
        return p["保存信息成功"].replace("{信息}","属性值")
    except:
        print(traceback.format_exc())
        return p["未知错误"]
