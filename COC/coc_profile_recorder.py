import traceback
from ..config_master import COCConfig

config=COCConfig()
profile_config=config.get("coc_profile_config")

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
    if group_id not in profile_config:
        return "本群未存储任何玩家档案！"
    if player_id not in profile_config[group_id]:
        return "您尚未在本群建立档案！"
    try:
        profile_config[group_id][player_id] = None
        config.saver()
        return "已成功删除档案"
    except:
        return "删除玩家档案时发生未知错误"


async def delete_profile_element(group_id, player_id, elements):
    elements_list = elements.split(" ")
    for element in elements_list:
        if profile_config[group_id][player_id][element] is not None:
            profile_config[group_id][player_id].pop(element,None)
        else:
            return f"删除至{element}时发生错误：属性不存在。命令未生效"
    config.saver()
    return f"已成功移除：{elements_list}"


async def show_profile(group_id, player_id, elements="", ALL=False):
    if ALL is True:
        try:
            msg = str(profile_config[group_id][player_id]).replace(
                '{', '').replace('}', '').replace('\'', '')
            return msg
        except:
            return "未读取到玩家档案"
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
            return "读取属性时发生未知错误"


async def add_profile(group_id, player_id, info):
    info = await resolve_info(info)
    if info is None:
        return "你在录什么？"
    try:
        try:
            profile_config[group_id][player_id].update(info)
        except:
            profile_config[group_id][player_id]={}
            profile_config[group_id][player_id].update(info)
        config.saver()
        return "已成功添加属性！"
    except:
        print(traceback.format_exc())
        return "录入玩家信息时发生未知错误！"
