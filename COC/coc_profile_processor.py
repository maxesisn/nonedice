from ..config_master import COCConfig

config = COCConfig()
template_config: dict = config.template
p: dict = config.personalization


async def comparing(group_id, user_id, misc, res):
    misc = misc.strip()
    profile_config = config.get("profile", group_id, user_id)

    # TODO:模糊匹配
    if misc in profile_config:
        record = profile_config[misc]
    elif misc in template_config:
        record = template_config[misc]
    else:
        return ""

    record = int(record)
    res = int(res)
    # TODO:房规功能
    if record >= res:
        status = "成功"
        if 1 <= res <= 5:
            status = "大成功"
        elif res <= record/5:
            status = "极难成功"
        elif res <= record/2:
            status = "困难成功"
    else:
        if 96 <= res <= 100:
            status = "大失败"
        else:
            status = "失败"
    return f"\n判定结果为{status}！"
