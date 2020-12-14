from .config_master import GeneralConfig
import traceback
import asyncio
from aiocqhttp.exceptions import ActionFailed

config = GeneralConfig()

ob_config = config.get("ob_config")


async def get_ob_list(group_id):
    try:
        if group_id not in ob_config:
            ob_config[group_id] = []
        if ob_config[group_id] != []:
            msg = "当前群内旁观者有：\n"
            for i in ob_config[group_id]:
                msg += "[CQ:at,qq=" + i + "]"
            return msg
        else:
            return "当前群内没有旁观者"
    except Exception as e:
        print(traceback.format_exc())
        return "在读取ob列表时发生未知错误"


async def join_ob_list(group_id, player_id):
    try:
        if group_id not in ob_config:
            ob_config[group_id] = []
        if player_id in ob_config[group_id]:
            return "额 你已经在旁观者列表里了"
        ob_config[group_id].append(player_id)
        print(ob_config)
        config.saver()
        return "加入旁观者列表成功！"
    except:
        print(traceback.format_exc())
        return "加入列表时发生未知错误"


async def quit_ob_list(group_id, player_id, ALL=False):
    try:
        if ALL:
            ob_config[group_id] = []
            config.saver()
            return "重置本群全部旁观者列表成功"
        if player_id in ob_config[group_id]:
            ob_config[group_id].remove(player_id)
            config.saver()
            return "已成功退出旁观者列表"
        else:
            return "我寻思你也没开旁观啊"
    except:
        print(traceback.format_exc())
        return "删除旁观者时发生未知错误"


async def ob_broadcast(bot, ev, msg):
    try:
        ob_list = ob_config[str(ev.group_id)]
        dicer_info = await bot.get_group_member_info(self_id=ev.self_id, group_id=ev.group_id, user_id=ev.user_id)
        try:
            nickname = dicer_info['card'] or dicer_info['nickname'] or str(
                dicer_info['user_id'])
        except:
            await bot.send(ev, "⚠无法获取旁观者信息")
            return
        for qq in ob_list:
            if int(qq) == int(ev.user_id):  # 怎么会有人开着旁观模式跑团啊？真没劲
                continue
            await bot.send_private_msg(self_id=ev.self_id, user_id=qq, message=f"群{ev.group_id}刚刚进行了一次暗骰，结果为：\n"+nickname+msg)
            await asyncio.sleep(1)
    except ActionFailed as e:
        await bot.send(ev, "⚠广播暗骰结果失败，请向骰娘私发消息建立临时会话")
        print(traceback.format_exc())
