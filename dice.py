import random
import operator

# 本部分源码基于 Ice-Cirno/HoshinoBot


async def do_basic_dice(num, min_, max_, opr, offset, misc=""):
    # 本部分源码基于 Ice-Cirno/HoshinoBot
    ops = {'+': operator.add, '-': operator.sub,
           'x': operator.mul, '*': operator.mul, '/': operator.truediv}
    if num == 0:
        return 404, "null dice"
    min_, max_ = min(min_, max_), max(min_, max_)
    rolls = list(map(lambda _: random.randint(min_, max_), range(num)))
    sum_ = sum(rolls)
    rolls_str = '+'.join(map(lambda x: str(x), rolls))
    if len(rolls_str) > 100:
        rolls_str = str(sum_)
    res = int(ops[opr](sum_, offset))
    TIP = "的掷骰结果是："
    if misc != None and len(misc) != 0:
        TIP = f"对{misc}" + TIP
    msg = [
        f'{TIP}\n',
        str(num) if num > 1 else '',
        'D',
        f'{min_}~' if min_ != 1 else '',
        str(max_),
        (opr + str(offset)) if offset else '',
        '=',
        '(' if num > 1 else '',
        rolls_str,
        ')' if num > 1 else '',
        (opr + str(offset)) if offset else '',
        f'={res}' if offset or num > 1 else '',
    ]
    msg = ''.join(msg)
    return res, msg

# 与random.randint()用法类似，但是可以读取群内默认面数
async def simple_dice(max_=100):
    result,_ = await do_basic_dice(1, 1, max_, '+', 0)
    return result 
