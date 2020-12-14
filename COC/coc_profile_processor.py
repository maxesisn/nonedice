from ..config_master import COCConfig

config = COCConfig()
profile_config = config.get("coc_profile_config")
template_config = config.get("coc_template_config")


async def comparing(group_id, user_id, misc, res):
    misc = misc.strip()
    config.loader()
    profile_config = config.get("coc_profile_config") # 困了，明天再寻思为什么要重载
    
    # TODO:模糊匹配
    if misc in profile_config[group_id][user_id].keys():
        record=int(profile_config[group_id][user_id][misc])
    elif misc in template_config.keys():
        record=template_config[misc]
    else:
        return ""
    if record >= res:
        if 1 <= res <= 5:
            status = "大成功"
        elif res <= record/2:
            status = "困难成功"
        elif res <= record/5:
            status = "极难成功"
        else:
            status = "成功"
    else:
        if 96 <= res <= 100:
            status = "大失败"
        else:
            status = "失败"
    return f"\n判定结果为{status}！"


# 大成功：1-5
# 困难成功：1/2
# 极难成功 1/5
# 大失败 96-100