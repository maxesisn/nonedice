import os
import re
import json

from hoshino import Service
from .dice import do_basic_dice

sv = Service('nonedice', help_='''
[.r] 掷骰子
[.r 3d12] 掷3次12面骰子
[.r 3d7~12] 掷3次7~12面骰子
[.r 3d12-7] 掷3次12面骰子，结果-7
[.r 3#1d3*2 对象]对对象骰3次1d3*2
[.rh *]同上，但是是暗骰模式
'''.strip())

dice_config = {}
fd = os.path.dirname(__file__)
try:
    with open(os.path.join(fd, "config/dice.json"), "r") as f:
        dice_config = json.load(f)
except Exception as e:
    pass


@sv.on_prefix('.r')
# 本部分代码基于Ice-Cirno/HoshinoBot中的dice模块
async def basic_dice(bot, ev):
    m = str(ev.message)
    #是否为暗骰模式
    
    HIDDEN_STATE = True if ev.raw_message.startswith(".rh ") else False
        
    misc = None
    times, num, min_, opr, offset = 1, 1, 1, '+', 0
    try:
        max_ = dice_config['default_dice']
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
                await bot.send_private_msg(self_id=ev.self_id, user_id=ev.user_id, message="本次暗骰" + msg + f"总计点数：{res}")
            else:
                await bot.send(ev, msg + f"总计点数：{res}", at_sender=True)
    else:
        res, msg = await do_basic_dice(num, min_, max_, opr, offset, misc)
        if msg != "null dice":
            if HIDDEN_STATE:
                await bot.send_private_msg(self_id=ev.self_id, user_id=ev.user_id, message="本次暗骰" + msg)
            else:
                await bot.send(ev, msg, at_sender=True)
        else:
            await bot.finish(ev, "咦？我骰子呢？")


@sv.on_prefix('.set')
async def set_default_dice(bot, ev):
    if str(ev.message).isdigit == False:
        await bot.finish(ev, "默认骰值必须为正整数!")
    dice_config['default_dice'] = int(str(ev.message))
    try:
        with open(os.path.join(fd, "config/dice.json"), "w") as f:
            json.dump(dice_config, f)
        await bot.send(ev, "保存成功！")
    except Exception as e:
        await bot.finish(ev, "保存失败，请联系维护组！\n"+e)
