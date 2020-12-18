import random
from ..config_master import COCConfig

config = COCConfig()
template_config: dict = config.template
p: str = config.personalization


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


async def sanCheck(group_id, user_id, status_dice, misc, res_set):
    misc = misc.strip()
    profile_config = config.get("profile", group_id, user_id)
    if "意志" in profile_config:
        if "理智" not in profile_config:
            profile_config["理智"] = profile_config["意志"]
    if "理智" in profile_config:
        record = profile_config["理智"]
    else:
        if misc.isdigit():
            record = int(misc)
        else:
            return p["获取信息失败"].replace("{信息}", "理智值")

    res = int(res_set[0]) if record >= status_dice else int(res_set[1])
    status = "成功" if res == int(res_set[0]) else "失败"
    record -= res
    profile_config["理智"] = record
    config.set("profile", profile_config, group_id, user_id)
    return f"san check{status}！扣除{res}，当前理智：{record}"


async def temp_insanity(group_id, user_id, show=False):
    profile_config = config.get("profile", group_id, user_id)
    if show:
        if "临时疯狂症状" in profile_config:
            return "、".join(profile_config["临时疯狂症状"])
        else:
            return p["没有信息"].replace("{信息}", "临时疯狂症状")
    id = random.randint(0, 9)
    insanity_list = ["失忆", "假性残疾", "暴力倾向", "偏执",
                     "人际依赖", "昏厥", "逃避行为", "竭嘶底里", "恐惧", "狂躁"]
    insanity_res = insanity_list[id]
    if "临时疯狂症状" not in profile_config:
        profile_config["临时疯狂症状"] = []
    profile_config["临时疯狂症状"].append(insanity_res)
    config.set("profile", profile_config, group_id, user_id)
    last_turns = random.randint(1, 10)
    if insanity_res == ("恐惧" or "狂躁"):
        # 草，100种症状，谁写啊
        pass
    return f"开始疯狂症状：{insanity_res}，持续{last_turns}轮！"


async def del_insanity(group_id, user_id, misc, ALL=False):
    misc = misc.strip()
    profile_config = config.get("profile", group_id, user_id)
    if ALL:
        profile_config.pop("临时疯狂症状", None)
        config.set("profile", profile_config, group_id, user_id)
        return p["重置列表成功"].replace("{信息}", "临时疯狂症状")
    if "临时疯狂症状" in profile_config and misc in profile_config["临时疯狂症状"]:
        profile_config["临时疯狂症状"].remove(misc)
        config.set("profile", profile_config, group_id, user_id)
        return p["删除信息成功"].replace("{信息}", "临时疯狂症状")
    else:
        return p["获取信息失败"].replace("{信息}", "需删除的临时疯狂症状")


async def list_insanity(group_id, user_id):
    id = random.randint(0, 9)
    insanity_list = ["失忆", "被窃", "遍体鳞伤", "暴力倾向",
                     "极端信念", "重要之人", "被收容", "逃避行为", "恐惧", "狂躁"]
    insanity_res = insanity_list[id]
    if insanity_res == ("恐惧" or "狂躁"):
        # 又来？
        pass
    return f"总结疯狂症状：{insanity_res}"
