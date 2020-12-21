from .config_master import Config
from aiocqhttp.exceptions import ActionFailed

p: str = Config("static").load("personalization")


async def get_ob_list(group_id):
    ob_config = Config(group_id).load("ob")
    if "list" in ob_config and len(ob_config["list"]):
        msg = p["列出信息"].replace("{信息}", "旁观者")
        ob_list = ob_config["list"]
        for i in ob_list:
            msg += "[CQ:at,qq="+i+"]"
    else:
        msg = p["没有信息"].replace("{信息}", "旁观者")
    return msg


async def join_ob_list(group_id, player_id):
    config = Config(group_id)
    ob_config = config.load("ob")
    if "list" not in ob_config:
        ob_config["list"] = list()
    if player_id in ob_config["list"]:
        return p["已在列表"].replace("{信息}", "旁观者列表")
    ob_config["list"].append(player_id)
    config.save()
    return p["加入列表成功"].replace("{信息}", "旁观者列表")


async def quit_ob_list(group_id, player_id, ALL=False):
    config = Config(group_id)
    ob_config = config.load("ob")
    try:
        if ALL:
            ob_config.pop("list", None)
            config.save()
            return p["重置列表成功"].replace("{信息}", "旁观者列表")
        ob_config["list"].remove(player_id)
    except KeyError:
        pass
    config.save()
    return p["退出列表成功"].replace("{信息}", "旁观者列表")


async def ob_broadcast(bot, ev, msg):
    ob_config = Config(ev.group_id).load("ob")
    dicer_info = await bot.get_group_member_info(self_id=ev.self_id, group_id=ev.group_id, user_id=str(ev.user_id))
    qqname = dicer_info["card"] or dicer_info["nickname"] or str(ev.user_id)
    if "list" in ob_config and len(ob_config["list"]) > 0:
        for i in ob_config["list"]:
            try:
                await bot.send_private_msg(self_id=ev.self_id, user_id=i, message=f"{qqname}于刚才进行了一次暗骰，其结果为：{msg}")
            except ActionFailed:
                await bot.send(ev, p["广播失败"])
    else:
        pass
