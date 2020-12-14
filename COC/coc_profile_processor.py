from ..config_master import COCConfig

config = COCConfig()
profile_config = config.get("coc_profile_config")
template_config = config.get("coc_template_config")


async def comparing(group_id, user_id, misc, res):
    misc = misc.strip()
    if misc in profile_config[group_id][user_id].keys():
        # TODO:模糊匹配
        status = "成功" if int(
            profile_config[group_id][user_id][misc]) > res else "失败"
        print(profile_config[group_id][user_id][misc])
        return f"\n已从资料卡读取{misc}值：{profile_config[group_id][user_id][misc]}，判定结果为{status}！"
    elif misc in template_config.keys():
        status = "成功" if int(template_config[misc]) > res else "失败"
        return f"\n以默认角色卡属性值：{template_config[misc]}为判定标准，判定结果为{status}！"
    else:
        return ""
