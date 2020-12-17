from ..dice import do_basic_dice as dice


async def gen_coc_profile(times, detail_mode):
    # 后面也许要改成单独的函数获取，所以现在先写成List
    values = ["力量", "体质", "体型", "敏捷", "外貌", "智力", "意志", "教育", "幸运"]
    sum = 0
    msg = "的人物做成：\n"
    if detail_mode is True:
        msg += "暂时不知道详细模式该生成啥……先生成几个普通的吧！\n"
        times = 1
    if times == 0:
        return "？"

    for i in range(times):
        sum = 0
        # 这里能分成3D6*5和(2D6+6)*5两类，但是好像还是不好简化代码
        result, _ = await dice(3, 1, 6, '*', 5)
        sum += result
        msg += values[0]+":"+str(result)+" "  # 力量

        result, _ = await dice(3, 1, 6, '*', 5)
        sum += result
        msg += values[1]+":"+str(result)+" "  # 体质

        result, _ = await dice(2, 1, 6, '+', 6)
        sum += result*5
        msg += values[2]+":"+str(result*5)+" "  # 体型

        result, _ = await dice(3, 1, 6, '*', 5)
        sum += result
        msg += values[3]+":"+str(result)+" "  # 敏捷

        result, _ = await dice(3, 1, 6, '*', 5)
        sum += result
        msg += values[4]+":"+str(result)+" "  # 外貌

        result, _ = await dice(2, 1, 6, '+', 6)
        sum += result*5
        msg += values[5]+":"+str(result*5)+" "  # 智力

        result, _ = await dice(3, 1, 6, '*', 5)
        sum += result
        msg += values[6]+":"+str(result)+" "  # 意志

        result, _ = await dice(2, 1, 6, '+', 6)
        sum += result*5
        msg += values[7]+":"+str(result*5)+" "  # 教育

        result, _ = await dice(1, 1, 20, '*', 5)
        sum_withLuck = sum+result
        msg += values[8]+":"+str(result)+" "  # 幸运
        if detail_mode:
            # 没用过详细模式，不知道该输出什么
            pass
        msg += "共计(不含幸运):"+str(sum)+" "
        msg += "共计(含幸运):"+str(sum_withLuck)+" "+"\n"

    return msg
