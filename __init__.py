from logging import root
import os
import re
import json

from hoshino import Service
from aiocqhttp.exceptions import ActionFailed

from .dice import do_basic_dice
from . import ob

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

fd = os.path.dirname(__file__)
try:
    with open(os.path.join(fd, "config/dice.json"), "r") as f:
        dice_config = json.load(f)
except:
    dice_config = {}


@sv.on_prefix('.r')
# 本部分代码基于Ice-Cirno/HoshinoBot中的dice模块
async def basic_dice(bot, ev):
    m = str(ev.message)
    # 是否为暗骰模式

    HIDDEN_STATE = True if ev.raw_message.startswith(".rh") else False

    misc = None
    times, num, min_, opr, offset = 1, 1, 1, '+', 0
    try:
        max_ = dice_config[str(ev.group_id)]['default_dice']
    except:
        max_ = 100
    match = re.match(
        r'^(h)?\s*(((?P<times>\d{1,4})#)?(?P<num>\d{0,2})d((?P<min>\d{1,4})~)?(?P<max>\d{0,4})((?P<opr>[*x/+-])(?P<offset>\d{0,5}))?)?(?P<misc>.*)?\b', m, re.I)
    print(match)
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
    if times > 1:
        res, msg = 0, ""
        for i in range(times):
            per_res, per_msg = await do_basic_dice(num, min_, max_, opr, offset, misc)
            if per_msg == "null dice":
                await bot.finish(ev, f"？虚空骰子还要扔{times}遍有意义吗")
            res += per_res
            msg += f"第{i+1}次"+per_msg+"\n"
        if msg != "null dice":
            if HIDDEN_STATE:
                await ob.ob_broadcast(bot,ev,msg)
                await bot.send_private_msg(self_id=ev.self_id, user_id=ev.user_id, message="本次暗骰" + msg + f"总计点数：{res}")
            else:
                await bot.send(ev, msg + f"总计点数：{res}", at_sender=True)
        else:
            await bot.finish(ev, "咦？我骰子呢？")
    else:
        res, msg = await do_basic_dice(num, min_, max_, opr, offset, misc)
        if msg != "null dice":
            if HIDDEN_STATE:
                await ob.ob_broadcast(bot,ev, msg)
                await bot.send_private_msg(self_id=ev.self_id, user_id=ev.user_id, message="本次暗骰" + msg)
            else:
                await bot.send(ev, msg, at_sender=True)
        else:
            await bot.finish(ev, "咦？我骰子呢？")


@sv.on_prefix('.set')
async def set_default_dice(bot, ev):
    group_id=str(ev.group_id)
    args=str(ev.message).lower()
    if args == ("coc" or 100):
        args = 100
    elif args == ("dnd" or 20):
        args = 20
    else:
        await bot.finish(ev,"面数必须为正整数！")
    if group_id not in dice_config:
        dice_config[group_id]={}
    dice_config[group_id]['default_dice'] = args
    try:
        with open(os.path.join(fd, "config/dice.json"), "w") as f:
            json.dump(dice_config, f, indent=4)
        await bot.send(ev, "保存成功！")
    except Exception as e:
        await bot.finish(ev, "保存失败，请联系维护组！\n"+e)


@sv.on_prefix('.ob')
async def dice_ob(bot, ev):
    command = str(ev.message)
    group_id, player_id = str(ev.group_id), str(ev.user_id)
    if command == 'exit':
        msg = await ob.quit_ob_list(group_id, player_id)
    elif command == 'list':
        msg = await ob.get_ob_list(group_id)
    elif command == 'clr':
        msg = await ob.quit_ob_list(group_id, player_id, ALL=True)
    elif command == 'join':
        msg = await ob.join_ob_list(group_id, player_id)
    elif command !="":
        msg = "？你这是什么指令"
    else:
        msg = await ob.join_ob_list(group_id, player_id)
    try:
        await bot.send(ev, msg)
    except ActionFailed as e:
        await bot.send(ev,"⚠发送暗骰结果失败，请所有旁观者先向骰娘私发消息建立临时会话")
        pass