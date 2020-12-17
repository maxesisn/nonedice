from .config_master import GeneralConfig
from aiocqhttp.exceptions import ActionFailed

config = GeneralConfig()

p: dict = config.personalization


async def get_ob_list(group_id):
    ob_config = config.get("ob", group_id)
    if ob_config is not None and len(ob_config):
        msg = p["列出信息"].replace("{信息}", "旁观者")
        ob_list = list(ob_config.keys())
        print(ob_list)
        for i in ob_list:
            msg += "[CQ:at,qq="+i+"]"
    else:
        msg = p["没有信息"].replace("{信息}", "旁观者")
    return msg


async def join_ob_list(group_id, player_id):
    ob_config = config.get("ob", group_id, player_id)
    ob_config["status"] = "enabled"
    config.set("ob", ob_config, group_id, player_id)
    return p["加入列表成功"].replace("{信息}", "旁观者列表")


async def quit_ob_list(group_id, player_id, ALL=False):
    if ALL:
        config.clr("ob", group_id)
        return p["重置列表成功"].replace("{信息}", "旁观者列表")
    config.clr("ob", group_id, player_id)
    return p["退出列表成功"].replace("{信息}", "旁观者列表")


async def ob_broadcast(bot, ev, msg):
    ob_config: dict = config.get("ob", ev.group_id)
    dicer_info = await bot.get_group_member_info(self_id=ev.self_id, group_id=ev.group_id, user_id=str(ev.user_id))
    qqname = dicer_info["card"] or dicer_info["nickname"] or str(ev.user_id)
    if len(ob_config.keys()):
        for i in ob_config.keys():
            if ob_config[i]["status"] == "enabled":
                try:
                    await bot.send_private_msg(self_id=ev.self_id, user_id=i, message=f"{qqname}于刚才进行了一次暗骰，其结果为：{msg}")
                except ActionFailed:
                    await bot.send(ev, p["广播失败"])
    else:
        pass
