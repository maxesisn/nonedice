import re

from hoshino import Service, priv
from aiocqhttp import ActionFailed

from .config_master import GeneralConfig
from .dice import do_basic_dice
from .dice import simple_dice
from . import ob
from .COC import profile_generator as coc_g
from .COC import profile_recorder as coc_r
from .COC import profile_processor as coc_p
from . import player

sv = Service('nonedice', help_='''
[.r] 掷骰子
[.r 3d12] 掷3次12面骰子
[.r 3d7~12] 掷3次7~12面骰子
[.r 3d12-7] 掷3次12面骰子，结果-7
[.r 3#1d3*2 对象]对对象骰3次1d3*2
[.rh *]同上，但是是暗骰模式，结果私聊发送
[.set coc/dnd]切换默认面数
[.ob]进入观察者模式，可以看到暗骰结果
[.ob exit]退出观察者模式
[.ob list]列出本群所有观察者
[.ob clr]清除本群所有观察者
'''.strip())

config = GeneralConfig()
p: str = config.personalization  # 其实是dict，但是我贪语法补全


async def dice_matcher(ev):
    m = str(ev.message)
    dice_config = config.get("dice", ev.group_id)
    times, num, min_, opr, offset, misc = 1, 1, 1, '+', 0, ""

    try:
        max_ = dice_config['default_dice']
    except:
        max_ = 100

    match = re.match(
        r'^\s*(((?P<times>\d{1,4})#)?(?P<num>\d{0,2})d((?P<min>\d{1,4})~)?(?P<max>\d{0,4})((?P<opr>[*x/+-])(?P<offset>\d{0,5}))?)?(?P<misc>.*)?\b', m, re.I)
    if match is not None:  # 判断是否含有掷骰式
        if s := match.group('times'):  # 次数
            times = int(s)
        if s := match.group('num'):  # 颗数
            num = int(s)
        if s := match.group('min'):  # 最小面数(可选)
            min_ = int(s)
        if s := match.group('max'):  # (最大)面数
            max_ = int(s)
        if s := match.group('opr'):  # 运算符
            opr = s
        if s := match.group('offset'):  # 偏移量
            offset = int(s)
        if s := match.group('misc'):  # 原因/玩家姓名
            misc = s
    return times, num, min_, max_, opr, offset, misc


@sv.on_prefix('.r')
# 本部分代码基于Ice-Cirno/HoshinoBot中的dice模块
async def basic_dice(bot, ev, HIDDEN_STATE=False):
    dice_config = config.get("dice", ev.group_id)
    times, num, min_, max_, opr, offset, misc = await dice_matcher(ev)
    if "doc" in dice_config:
        doc = dice_config["doc"]
    else:
        doc = 0
    if times > 1:
        res, msg = 0, ""
        for i in range(times):
            per_res, per_msg = await do_basic_dice(num, min_, max_, opr, offset, misc)
            if per_msg == "null dice":
                await bot.finish(ev, f"")
            res += per_res
            msg += f"第{i+1}次"+per_msg+"\n"

        if msg != "null dice":
            if misc != "":
                msg += await coc_p.comparing(str(ev.group_id), str(ev.user_id), misc, res, doc)
            if HIDDEN_STATE:
                await ob.quit_ob_list(str(ev.group_id), str(ev.user_id))
                await ob.ob_broadcast(bot, ev, msg)
                await bot.send_private_msg(self_id=ev.self_id, user_id=ev.user_id, message="本次暗骰" + msg + f"总计点数：{res}")
            else:
                await bot.send(ev, msg + f"总计点数：{res}", at_sender=True)
        else:
            await bot.finish(ev, p["数值不合法"].replace("{信息}", "骰子数量"))
    else:
        res, msg = await do_basic_dice(num, min_, max_, opr, offset, misc)
        if msg != "null dice":
            if misc != "":
                msg += await coc_p.comparing(str(ev.group_id), str(ev.user_id), misc, res, doc)
            if HIDDEN_STATE:
                await ob.quit_ob_list(str(ev.group_id), str(ev.user_id))
                await ob.ob_broadcast(bot, ev, msg)
                try:
                    await bot.send_private_msg(self_id=ev.self_id, user_id=ev.user_id, message="本次暗骰" + msg)
                except ActionFailed:
                    await bot.finish(ev, p["广播失败"])
            else:
                await bot.send(ev, msg, at_sender=True)
        else:
            await bot.finish(ev, p["数值不合法"].replace("{信息}", "骰子数量"))


# 对啊 我把暗骰判断交给触发器处理不就完事了吗
@sv.on_prefix('.rh')
async def hidden_dice(bot, ev):
    await basic_dice(bot, ev, HIDDEN_STATE=True)


@sv.on_prefix('.set')
async def set_default_dice(bot, ev):
    dice_config = config.get("dice", ev.group_id)
    args = str(ev.message).lower()
    if args == "coc":
        args = 100
    elif args == "dnd":
        args = 20
    else:
        await bot.finish(ev, p["数值不合法"].replace("{信息}", "面数"))
    dice_config['default_dice'] = args
    config.set("dice", dice_config, ev.group_id)
    await bot.send(ev, p["保存信息成功"].replace("{信息}", "默认面数"))


@sv.on_prefix('.ob')
async def dice_ob(bot, ev):
    command = str(ev.message)
    group_id, player_id = str(ev.group_id), str(ev.user_id)
    if command == 'exit':
        msg = await ob.quit_ob_list(group_id, player_id)
    elif command == 'list':
        msg = await ob.get_ob_list(group_id)
    elif command == 'clr':
        if not priv.check_priv(ev, priv.ADMIN):
            msg = p["权限不足"]
        else:
            msg = await ob.quit_ob_list(group_id, player_id, ALL=True)
    elif command == 'join':
        msg = await ob.join_ob_list(group_id, player_id)
    elif command != "":
        msg = p["未知指令"]
    else:
        msg = await ob.join_ob_list(group_id, player_id)
    await bot.send(ev, msg)


@sv.on_prefix('.nn')
async def set_nickname(bot, ev):
    command = str(ev.message).lower()
    if command == "show":
        msg = await player.get_player_name(str(ev.group_id), str(ev.user_id))
        if msg is None:
            msg = p["获取信息失败"].replace("{信息}", "您当前的昵称")
    else:
        msg = await player.set_player_name(str(ev.group_id), str(ev.user_id), str(ev.message))
    await bot.send(ev, msg)


@sv.on_prefix('.coc7')
@sv.on_prefix('.coc')
async def coc_profile(bot, ev):
    command = str(ev.message).lower()
    detail_mode = True if "d" in command else False
    command = command[command.find("d"):]
    print(command)
    if command.isdigit() is False:
        command = 1
    msg = await coc_g.gen_coc_profile(int(command), detail_mode)
    await bot.send(ev, msg, at_sender=True)


@sv.on_prefix('.coc6')
async def coc_profile_v6(bot, ev):
    # 摸了
    await bot.send(ev, p["劝退COC6"])


@sv.on_prefix('.st')
async def coc_record_profile(bot, ev):
    command = str(ev.message).lower()
    if command.startswith('clr'):
        msg = await coc_r.clear_profile(str(ev.group_id), str(ev.user_id))
        await bot.finish(ev, msg)
    if command.startswith('del'):
        elements = command[3:].strip()
        print(elements)
        msg = await coc_r.delete_profile_element(str(ev.group_id), str(ev.user_id), elements)
        await bot.finish(ev, msg)
    if command.startswith('show'):
        if command == "show":
            msg = await coc_r.show_profile(str(ev.group_id), str(ev.user_id), ALL=True)
        else:
            element = command[3:]
            msg = await coc_r.show_profile(str(ev.group_id), str(ev.user_id), element=element)
        await bot.finish(ev, msg)
    else:
        msg = await coc_r.add_profile(str(ev.group_id), str(ev.user_id), command)
        await bot.finish(ev, msg)


@sv.on_prefix(".sc")
async def sanCheck(bot, ev):
    _, num, min_, max_, opr, offset, misc = await dice_matcher(ev)
    res_set = []
    command = str(ev.message).lower().split(" ")
    if command != "":
        res_set = command[0].split("/")
        if len(res_set) == 2:
            for i in res_set:
                if "d" in i:
                    i, _ = await do_basic_dice(num, min_, max_, opr, offset, misc)
        else:
            await bot.finish(ev, p["数值不合法"].replace("{信息}", "表达式"))
    if len(command) == 2:
        misc = command[1]
    if len(command) > 2:
        await bot.finish(ev, p["数值不合法"].replace("{信息}", "表达式"))
    status_dice = await simple_dice(max_)
    msg = await coc_p.sanCheck(ev.group_id, ev.user_id, status_dice, misc, res_set)
    await bot.send(ev, msg)


@sv.on_prefix('.jrrp')
async def jrrp(bot, ev):
    msg = await player.jrrp(ev.user_id)
    msg = p["人品值"].replace("{消息}", str(msg))
    await bot.send(ev, msg, at_sender=True)


@sv.on_prefix('.ti')
async def temp_insanity(bot, ev):
    command = str(ev.message).strip().lower()
    if command == "show":
        msg = await coc_p.temp_insanity(ev.group_id, ev.user_id, show=True)
    elif command.startswith("del"):
        msg = await coc_p.del_insanity(ev.group_id, ev.user_id, command[3:])
    elif command == "clr":
        msg = await coc_p.del_insanity(ev.group_id, ev.user_id, "", ALL=True)
    else:
        msg = await coc_p.temp_insanity(ev.group_id, ev.user_id)
    await bot.send(ev, msg)


@sv.on_prefix('.li')
async def list_insanity(bot, ev):
    msg = await coc_p.list_insanity(ev.group_id, ev.user_id)
    await bot.send(ev, msg)


@sv.on_prefix('.setdoc')
async def setdoc(bot, ev):
    dice_config = config.get("dice", ev.group_id)
    arg = str(ev.message).strip().lower()
    if arg.isdigit() or arg == "":
        if arg == "":
            arg = 0
        arg = int(arg)
        if 0 <= arg <= 5:
            dice_config["doc"] = arg
            config.set("dice", dice_config, ev.group_id)
            await bot.finish(ev, p["保存信息成功"].replace("{信息}", "房规"))
    await bot.finish(ev, p["数值不合法"].replace("信息", "房规"))
