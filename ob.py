from .config_master import GeneralConfig
import traceback
import asyncio
from aiocqhttp.exceptions import ActionFailed

config = GeneralConfig()

ob_config = config.get("ob_config")
p:str = config.get("personalization_config")

async def get_ob_list(group_id):
    try:
        if group_id not in ob_config:
            ob_config[group_id] = []
        if ob_config[group_id] != []:
            msg = p["列出信息"].replace("{信息}","群内旁观者")
            for i in ob_config[group_id]:
                msg += "[CQ:at,qq=" + i + "]"
            return msg
        else:
            return p["没有信息"].replace("{信息}","旁观者")
    except:
        print(traceback.format_exc())
        return p["未知错误"]


async def join_ob_list(group_id, player_id):
    try:
        if group_id not in ob_config:
            ob_config[group_id] = []
        if player_id in ob_config[group_id]:
            return p["已在列表"].replace("{信息}","旁观者列表")
        ob_config[group_id].append(player_id)
        print(ob_config)
        config.saver()
        return p["加入列表成功"].replace("{信息}","旁观者列表")
    except:
        print(traceback.format_exc())
        return p["未知错误"]


async def quit_ob_list(group_id, player_id, ALL=False):
    try:
        if ALL:
            ob_config[group_id] = []
            config.saver()
            return p["重置列表成功"].replace("{信息}","观察者列表")
        if player_id in ob_config[group_id]:
            ob_config[group_id].remove(player_id)
            config.saver()
            return p["退出列表成功"].replace("{信息}","观察者列表")
        else:
            return p["未在列表内"].replace("{信息}","旁观者列表")
    except:
        print(traceback.format_exc())
        return p["未知错误"]


async def ob_broadcast(bot, ev, msg):
    try:
        ob_list = ob_config[str(ev.group_id)]
        dicer_info = await bot.get_group_member_info(self_id=ev.self_id, group_id=ev.group_id, user_id=ev.user_id)
        try:
            nickname = dicer_info['card'] or dicer_info['nickname'] or str(
                dicer_info['user_id'])
        except:
            await bot.send(ev, p["获取信息失败"].replace("{信息}","昵称"))
            return
        for qq in ob_list:
            if int(qq) == int(ev.user_id):  # 怎么会有人开着旁观模式跑团啊？真没劲
                continue
            await bot.send_private_msg(self_id=ev.self_id, user_id=qq, message=f"群{ev.group_id}刚刚进行了一次暗骰，结果为：\n"+nickname+msg)
            await asyncio.sleep(1)
    except ActionFailed:
        await bot.send(ev, p["广播失败"])
        print(traceback.format_exc())
