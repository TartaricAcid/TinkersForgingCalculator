#!/usr/bin/python3
import re

# 各个锻造增加的数值
HIT_LIGHT = -3  # 轻击
HIT_MEDIUM = -6  # 击打
HIT_HARD = -9  # 重击
DRAW = -15  # 牵拉
PUNCH = 2  # 冲压
BEND = 7  # 弯曲
UPSET = 13  # 镦锻
SHRINK = 16  # 收缩

# 固定词典
INDEX = {"a": HIT_LIGHT, "b": HIT_MEDIUM, "c": HIT_HARD, "d": DRAW,
         "e": PUNCH, "f": BEND, "g": UPSET, "h": SHRINK}

# 翻译
TRANS = {HIT_LIGHT: "轻击", HIT_MEDIUM: "击打", HIT_HARD: "重击", DRAW: "牵拉",
         PUNCH: "冲压", BEND: "弯曲", UPSET: "镦锻", SHRINK: "收缩"}

# 基本参数
VALUE = 9  # 锻造数值
COUNT = 10  # 锻造总次数

# 最后三次锻造的 list
LAST_THREE_LIST = []

# 颜色代码
ANSI_RESET = "\u001B[0m"
ANSI_RED = "\u001B[31m"
ANSI_CYAN = "\u001B[36m"
ANSI_GREEN = "\u001B[92m"
ANSI_YELLOW = "\u001B[93m"
ANSI_BLUE = "\u001B[94m"


# 求和函数，通过传入 list 和下一步操作数值，求出总和
def get_sum(list_in, get_sum_num=0):
    get_sum_j = 0
    for get_sum_i in list_in:
        get_sum_j = get_sum_j + get_sum_i
    return get_sum_j + get_sum_num


if __name__ == '__main__':
    # CMD 界面书写
    print(ANSI_GREEN + "╭====================================╮" + ANSI_RESET)
    print(ANSI_YELLOW + "             MIT License              ")
    print("    Copyright (c) 2018 TartaricAcid    ")
    print("    Tinker's Forging 模组锻造计算器     " + ANSI_RESET)
    print(ANSI_GREEN + "╰====================================╯" + ANSI_RESET)

    # 开始进行输入
    last_one = input(ANSI_BLUE + "请输入最后一次锻造操作（不区分大小写）\n" + ANSI_CYAN
                     + "轻击：a\t\t" + "击打：b\t\t" + "重击：c\t\t" + "牵拉：d\t\t\n"
                     + "冲压：e\t\t" + "弯曲：f\t\t" + "镦锻：g\t\t" + "收缩：h\t\t\n"
                     + ANSI_BLUE + "请输入你的操作：" + ANSI_RESET)
    while not re.findall("^[a-h]$", last_one):
        last_one = input(ANSI_BLUE + "你输入的操作不对，请重新输入：" + ANSI_RESET)

    last_two = input(ANSI_BLUE + "请输入倒数第二次锻造操作（不区分大小写）\n" + ANSI_CYAN
                     + "轻击：a\t\t" + "击打：b\t\t" + "重击：c\t\t" + "牵拉：d\t\t\n"
                     + "冲压：e\t\t" + "弯曲：f\t\t" + "镦锻：g\t\t" + "收缩：h\t\t\n"
                     + ANSI_BLUE + "请输入你的操作：" + ANSI_RESET)
    while not re.findall("^[a-h]$", last_two):
        last_two = input(ANSI_BLUE + "你输入的操作不对，请重新输入：" + ANSI_RESET)

    last_three = input(ANSI_BLUE + "请输入倒数第三次锻造操作（不区分大小写，如果为空请直接摁回车）\n" + ANSI_CYAN
                       + "轻击：a\t\t" + "击打：b\t\t" + "重击：c\t\t" + "牵拉：d\t\t\n"
                       + "冲压：e\t\t" + "弯曲：f\t\t" + "镦锻：g\t\t" + "收缩：h\t\t\n"
                       + ANSI_BLUE + "请输入你的操作：" + ANSI_RESET)
    while not (last_three == "" or re.findall("^[a-h]$", last_three)):
        last_three = input(ANSI_BLUE + "你输入的操作不对，请重新输入：" + ANSI_RESET)

    # 输入锻造总数值
    VALUE = input(ANSI_BLUE + "\n红色-绿色箭头差值，数值介于 -150 ~ 150 之间（不含）\n" + ANSI_RESET
                  + ANSI_BLUE + "请输入你的数值：" + ANSI_RESET)
    while not re.findall("^(-?(1[0-4]\d|[1-9]\d|[1-9])|0)$", VALUE):
        VALUE = input(ANSI_BLUE + "输入只能为数字且介于 -150 ~ 150 之间，请重新输入：" + ANSI_RESET)

    # 将结果存入 List
    if last_three != "":
        # 第三步可能为空，所以如果真为空，就不计入
        LAST_THREE_LIST.append(INDEX.get(last_three.lower()))
    LAST_THREE_LIST.append(INDEX.get(last_two.lower()))
    LAST_THREE_LIST.append(INDEX.get(last_one.lower()))

    # 最后的转换
    VALUE = int(VALUE)  # 转换为数字
    VALUE = VALUE - get_sum(LAST_THREE_LIST)  # 获取剔除最后三步后的锻造数值

    # 待用变量
    total = [[0]]  # 存储合法的总步骤
    tmp = []  # 存储每次锻造遍历的临时步骤
    result = [[]]  # 存储能够符合标准的结果

    # 锻造次数遍历
    for i in range(COUNT):
        # 继承上一个锻造结果，进行下一次锻造尝试
        for j in total:
            # 如果和在 -150-150 之间才可以进行存储，否则抛弃
            if -150 < get_sum(j, SHRINK) < 150:

                # 因为 Python 的原因，需要进行一次 copy
                tmp_j = j.copy()  # 复制
                tmp_j.append(SHRINK)  # 存入下一步数值

                # 符合指定结果的，存入 result 中
                if get_sum(j, SHRINK) == VALUE:
                    result.append(tmp_j)
                # 否则，存入临时变量中
                else:
                    tmp.append(tmp_j)

            if -150 < get_sum(j, UPSET) < 150:
                tmp_j = j.copy()
                tmp_j.append(UPSET)
                if get_sum(j, UPSET) == VALUE:
                    result.append(tmp_j)
                else:
                    tmp.append(tmp_j)

            if -150 < get_sum(j, BEND) < 150:
                tmp_j = j.copy()
                tmp_j.append(BEND)
                if get_sum(j, BEND) == VALUE:
                    result.append(tmp_j)
                else:
                    tmp.append(tmp_j)

            if -150 < get_sum(j, PUNCH) < 150:
                tmp_j = j.copy()
                tmp_j.append(PUNCH)
                if get_sum(j, PUNCH) == VALUE:
                    result.append(tmp_j)
                else:
                    tmp.append(tmp_j)

            if -150 < get_sum(j, DRAW) < 150:
                tmp_j = j.copy()
                tmp_j.append(DRAW)
                if get_sum(j, DRAW) == VALUE:
                    result.append(tmp_j)
                else:
                    tmp.append(tmp_j)

            if -150 < get_sum(j, HIT_HARD) < 150:
                tmp_j = j.copy()
                tmp_j.append(HIT_HARD)
                if get_sum(j, HIT_HARD) == VALUE:
                    result.append(tmp_j)
                else:
                    tmp.append(tmp_j)

            if -150 < get_sum(j, HIT_MEDIUM) < 150:
                tmp_j = j.copy()
                tmp_j.append(HIT_MEDIUM)
                if get_sum(j, HIT_MEDIUM) == VALUE:
                    result.append(tmp_j)
                else:
                    tmp.append(tmp_j)

            if -150 < get_sum(j, HIT_LIGHT) < 150:
                tmp_j = j.copy()
                tmp_j.append(HIT_LIGHT)
                if get_sum(j, HIT_LIGHT) == VALUE:
                    result.append(tmp_j)
                else:
                    tmp.append(tmp_j)

        # 锻造次数一次遍历结束
        # 装填到 total 里面，同时清空 tmp
        total = tmp.copy()
        tmp.clear()

        # 如果这时候 result 已经有值，则无需遍历费事了
        if len(result) > 1:
            break

    # 打印输出
    print("\n───────────────────────────────────────")
    num = 1  # 计数用工具
    for k in result:
        # 遍历输出结果
        if k:  # 此判定为剔除空值
            # 输出标题
            print(ANSI_YELLOW + "方案" + str(num) + ANSI_RESET)

            # 剔除首位的 0
            for l in k[1:]:
                print(ANSI_CYAN + TRANS.get(l), end=ANSI_RESET + " -> " + ANSI_CYAN)

            # 不要忘记最后固定的三步
            for m in LAST_THREE_LIST:
                print(ANSI_CYAN + TRANS.get(m), end=ANSI_RESET + " -> " + ANSI_CYAN)
            # 补位用的
            print(ANSI_RED + "【成功】" + ANSI_RESET)

            # 自加
            num = num + 1
    print("───────────────────────────────────────")
