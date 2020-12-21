import random
from ..config_master import Config

p: str = Config("static").load("personalization")
template_config: str = Config("static").load("coc_template")


async def comparing(group_id, user_id, misc, res, doc):
    misc = misc.strip()
    profile_config = Config(group_id).load(user_id)["profile"]
    # TODO:模糊匹配
    if misc in profile_config:
        record = profile_config[misc]
    elif misc in template_config:
        record = template_config[misc]
    else:
        return ""

    record = int(record)
    res = int(res)
    # 房规不太好抽象成配置文件，就嗯写
    # 以后一定修！
    if doc == 1:
        status = "大成功" if (record < 50 and res == 1) or (
            record >= 50 and 1 <= res <= 5) else None
        status = "大失败" if (record < 50 and 96 <= res <= 100) or (
            record >= 50 and res == 100) else None
    if doc == 2:
        status = "大成功" if 1 <= res <= 5 and res <= record else None
        status = "大失败" if res == 100 or (
            96 <= res <= 99 and res > record) else None
    if doc == 3:
        status = "大成功" if 1 <= res <= 5 else None
        status = "大失败" if 96 <= res <= 100 else None
    if doc == 4:
        status = "大成功" if 1 <= res <= 5 and res <= record/10 else None
        status = "大失败" if (record < 50 and res >= 96+record /
                           10) or (record >= 50 and res == 100) else None
    if doc == 5:
        status = "大成功" if 1 <= res <= 2 and res < record/5 else None
        status = "大失败" if (record < 50 and 96 <= res <= 100) or (
            record >= 50 and 99 <= res <= 100) else None
    else:
        status = "大成功" if res == 1 else None
        status = "大失败" if (record < 50 and 96 <= res <= 100) or (
            record >= 50 and res == 100) else None

    if status is None:
        if record >= res:
            if res < record/5:
                status = "极难成功"
            elif res < record/2:
                status = "困难成功"
            else:
                status = "成功"
        else:
            status = "失败"

    return f"\n判定结果为{status}！"


async def sanCheck(group_id, user_id, status_dice, misc, res_set):
    misc = misc.strip()
    config=Config(group_id)
    player_config = config.load(user_id)
    if "profile" not in player_config:
        player_config["profile"]=dict()
    if "意志" in player_config["profile"]:
        if "理智" not in player_config["profile"]:
            player_config["profile"]["理智"] = player_config["profile"]["意志"]
    if "理智" in player_config["profile"]:
        record = player_config["profile"]["理智"]
    else:
        if misc.isdigit():
            record = int(misc)
        else:
            return p["获取信息失败"].replace("{信息}", "理智值")

    res = int(res_set[0]) if record >= status_dice else int(res_set[1])
    status = "成功" if res == int(res_set[0]) else "失败"
    record -= res
    player_config["profile"]["理智"] = record
    config.save()
    return f"san check{status}！扣除{res}，当前理智：{record}"


async def temp_insanity(group_id, user_id, show=False):
    config=Config(group_id)
    player_config=config.load(user_id)
    if "profile" not in player_config:
        player_config["profile"]=dict()
    if show:
        if "临时疯狂症状" in player_config["profile"]:
            return "、".join(player_config["profile"]["临时疯狂症状"])
        else:
            return p["没有信息"].replace("{信息}", "临时疯狂症状")
    insanity_list = ["失忆", "假性残疾", "暴力倾向", "偏执",
                     "人际依赖", "昏厥", "逃避行为", "竭嘶底里", "恐惧", "狂躁"]
    insanity_res = insanity_list[random.randint(0, 9)]
    if "临时疯狂症状" not in player_config["profile"]:
        player_config["profile"]["临时疯狂症状"] = list()
    player_config["profile"]["临时疯狂症状"].append(insanity_res)
    config.save()
    last_turns = random.randint(1, 10)
    if insanity_res == ("恐惧" or "狂躁"):
        # 草，100种症状，谁写啊
        pass
    return f"开始疯狂症状：{insanity_res}，持续{last_turns}轮！"


async def del_insanity(group_id, user_id, misc, ALL=False):
    misc = misc.strip()
    config=Config(group_id)
    player_config = config.load(user_id)
    if "profile" not in player_config:
        player_config["profile"]=dict()
    if ALL:
        player_config["profile"].pop("临时疯狂症状", None)
        config.save()
        return p["重置列表成功"].replace("{信息}", "临时疯狂症状")
    if "临时疯狂症状" in player_config["profile"] and misc in player_config["profile"]["临时疯狂症状"]:
        player_config["profile"]["临时疯狂症状"].remove(misc)
        if len(player_config["profile"]["临时疯狂症状"]) ==0:
            player_config["profile"].pop("临时疯狂症状", None)
        config.save()
        return p["删除信息成功"].replace("{信息}", "临时疯狂症状")
    else:
        return p["获取信息失败"].replace("{信息}", "需删除的临时疯狂症状")


async def list_insanity():
    id = random.randint(0, 9)
    insanity_list = ["失忆", "被窃", "遍体鳞伤", "暴力倾向",
                     "极端信念", "重要之人", "被收容", "逃避行为", "恐惧", "狂躁"]
    insanity_res = insanity_list[id]
    if insanity_res == ("恐惧" or "狂躁"):
        # 又来？
        pass
    return f"总结疯狂症状：{insanity_res}"
