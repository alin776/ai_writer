#!/usr/bin/env python3

"""
创意熵值注入器

从精选列表中随机选取元素，为创作引入创意熵值。
通过强制引入意外组合，打破默认创作模式。

用法:
  python entropy.py lies              # 随机一条角色错误信念
  python entropy.py lies --count 3    # 随机三条错误信念
  python entropy.py --list            # 显示所有可用列表
  python entropy.py --combo           # 生成随机组合
  python entropy.py --file data.json professions  # 使用自定义文件
"""

import sys
import json
import random

# 确保所有平台上使用 UTF-8 输出
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


# 内置列表，可直接使用
BUILT_IN_LISTS: dict[str, list[str]] = {
    # 角色错误信念（用于 character-arc 技能）
    'lies': [
        "只有变强才能保护重要的人",
        "感情只会成为修炼的阻碍",
        "信任别人就会被背叛",
        "我的价值取决于修为境界",
        "弱者不配拥有任何东西",
        "血脉决定一切，努力无用",
        "孤身一人才是最安全的",
        "为达目的可以不择手段",
        "权力是解决一切问题的答案",
        "我永远无法超越师兄/前辈",
        "背负命运就必须放弃自我",
        "仇恨是唯一的生存动力",
        "弱肉强食是天道法则",
        "我不配被爱/被拯救",
        "过去的罪孽永远无法赎清",
    ],

    # 角色伤痛/心魔（角色背景中的创伤，催生错误信念）
    'ghosts': [
        "宗门灭亡，独自逃生",
        "被至亲之人背叛/暗算",
        "亲眼目睹师父/亲人惨死",
        "关键时刻实力不足，无法救人",
        "被冤枉逐出师门",
        "幼时被遗弃，不知亲生父母",
        "信任之人原来是卧底/内鬼",
        "为了活命做了不可饶恕之事",
        "修炼走火入魔，差点失去一切",
        "被强者羞辱碾压，尊严尽失",
        "曾经的挚爱死在自己怀中",
        "逃离灾难时抛下了同伴",
        "发现敬仰的师尊实为伪善之人",
        "被当作实验体/棋子利用",
        "亲手杀死了被魔化的亲人",
    ],

    # 场景灾难/转折（用于 scene-sequencing 技能）
    'disasters': [
        "突破成功，但引来了强敌注意",
        "逃脱失败，而且暴露了同伴位置",
        "获得宝物，但触发了禁制机关",
        "击败对手，却发现这只是替身",
        "找到线索，但时间已经来不及了",
        "救出了人，代价是暴露自己的秘密",
        "成功了，但最信任的人背叛了",
        "计划失败，而且对方知道了你的弱点",
        "达成了目标，但用了不该用的手段",
        "没能阻止，而且局势进一步恶化",
        "突围成功，但受了重伤",
        "获得了力量，代价是失去部分记忆",
        "赢得了战斗，却输掉了人心",
        "解开了谜团，但真相比想象更可怕",
        "化解了危机，但埋下了更大的隐患",
    ],

    # 两难抉择（用于 scene-sequencing 技能）
    'dilemmas': [
        "救同伴 vs 完成任务",
        "说出真相 vs 保护某人",
        "个人利益 vs 团队大局",
        "冒险快速通关 vs 稳扎稳打",
        "修炼突破 vs 救治同伴",
        "坚持原则 vs 务实妥协",
        "信任新盟友 vs 独自行动",
        "暴露秘密 vs 维持伪装",
        "立即反击 vs 隐忍蛰伏",
        "仁慈放人 vs 斩草除根",
        "忠于旧主 vs 顺应大势",
        "牺牲自己 vs 牺牲他人",
        "报仇 vs 活下去",
        "使用禁术 vs 正道手段",
        "守护一人 vs 守护苍生",
    ],

    # 非典型身份/职业（用于打破角色刻板印象）
    'professions': [
        "灵兽粪便清理工",
        "传送阵报站员",
        "丹炉裂缝修补匠",
        "仙城下水道管理员",
        "灵石品鉴师",
        "飞剑保养师",
        "渡劫场地租赁商",
        "天劫观测员",
        "宗门伙食堂大厨",
        "妖兽标本制作师",
        "阵法拆除专家",
        "功法盗版识别官",
        "境界鉴定黄牛",
        "秘境导游",
        "战后遗骸收集者",
    ],

    # 非典型场景（用于打破场景刻板印象）
    'locations': [
        "宗门杂物房深夜",
        "灵兽粪坑旁的枯树下",
        "废弃传送阵的裂缝里",
        "藏经阁最底层的灰尘角落",
        "丹炉爆炸后的废墟",
        "灵泉枯竭后的干涸池底",
        "凡人城镇的路边摊",
        "飞行法器维修停泊场",
        "仙城公共茅厕",
        "妖兽养殖场",
        "被遗忘的上古战场遗迹",
        "宗门禁地外围的围墙下",
        "坊市关门后的空巷",
        "渡劫失败者的坟场",
        "灵脉断裂带的废矿",
    ],

    # 正交碰撞（用于 cliche-transcendence 技能）
    'collisions': [
        "他调查的案子偶然牵扯到主角的秘密身世",
        "她在追查完全不同的事，但用到了同一条线索",
        "他的日常工作让他反复出现在主角的路线上",
        "他在找的人恰好和主角同行",
        "她的私人恩怨针对的是主角需要的人",
        "他掌握了一个自己不知道价值的情报",
        "她目睹了一件事但完全误解了含义",
        "他的修炼功法和主角的秘密产生了共鸣",
        "她执行门规恰好阻拦了主角",
        "他想要同一种资源但理由完全不同",
        "她在清理别人留下的烂摊子，主角是'证据'之一",
        "他在测试新法器，无意中探测到主角的隐藏",
        "她在收集素材写游记，调查到了主角的处境",
        "他曾经历过和主角类似的遭遇",
        "他制造的骗局意外模仿了真正的阴谋",
    ],

    # 场景开头（用于 drafting 提示）
    'openings': [
        "一场已经持续数个时辰的争吵中间",
        "有人出现在不该出现的地方",
        "两个人假装互不认识",
        "暴力之后的善后现场，而非暴力本身",
        "一个即将被打破的日常",
        "一边干活一边消化坏消息",
        "仇人之间被迫的客套",
        "揭秘前的最后一刻",
        "因为分心而把手头的事搞砸",
        "两场对话同时进行",
        "等待中试图掩饰焦躁",
        "一次可能是永别的告别",
        "发现了改变一切的东西",
        "变故来临前最后的平静时刻",
        "表面镇定内心已经崩溃",
    ],

}


def random_from(arr: list, count: int = 1) -> list:
    shuffled = arr[:]
    random.shuffle(shuffled)
    return shuffled[:min(count, len(arr))]


def generate_combo(lists: dict[str, list[str]]) -> dict[str, str]:
    combo: dict[str, str] = {}
    for name, items in lists.items():
        combo[name] = random_from(items, 1)[0]
    return combo


def load_external_lists(filepath: str) -> dict[str, list[str]]:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f'加载文件 {filepath} 失败: {e}', file=sys.stderr)
        sys.exit(1)


def main() -> None:
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print("""
创意熵值注入器 - 随机元素灵感激发

用法:
  python entropy.py <列表名>           # 随机一条元素
  python entropy.py <列表名> --count N # 随机 N 条元素
  python entropy.py --list                # 显示所有可用列表
  python entropy.py --combo               # 每个列表各取一条
  python entropy.py --combo-small         # 精简组合
  python entropy.py --file custom.json <列表名>  # 使用自定义列表

内置列表:
  lies        - 角色错误信念（用于角色弧线）
  ghosts      - 角色伤痛/心魔（背景创伤）
  disasters   - 场景灾难/转折
  dilemmas    - 两难抉择
  professions - 非典型身份/职业
  locations   - 非典型场景
  collisions  - 正交碰撞
  openings    - 场景开头

选项:
  --count N   返回 N 条随机结果
  --json      以 JSON 格式输出
  --list      显示所有可用列表
  --combo     从每个列表各生成一条
  --file F    从 JSON 文件加载额外列表
""")
        sys.exit(0)

    lists = {**BUILT_IN_LISTS}

    # 加载外部文件（如指定）
    file_index = args.index('--file') if '--file' in args else -1
    if file_index != -1 and file_index + 1 < len(args):
        external = load_external_lists(args[file_index + 1])
        lists = {**lists, **external}

    json_output = '--json' in args

    # 显示可用列表
    if '--list' in args:
        print('可用列表:' + '\n')
        for name, items in lists.items():
            print(f'  {name:<15} ({len(items)} 条)')
        sys.exit(0)

    # 从全部或部分列表生成组合
    if '--combo' in args:
        combo = generate_combo(lists)
        if json_output:
            print(json.dumps(combo, indent=2, ensure_ascii=False))
        else:
            print('随机组合:' + '\n')
            for name, value in combo.items():
                print(f'  {name}: {value}')
        sys.exit(0)

    if '--combo-small' in args:
        small = {
            'lies': lists['lies'],
            'disasters': lists['disasters'],
            'locations': lists['locations'],
        }
        combo = generate_combo(small)
        if json_output:
            print(json.dumps(combo, indent=2, ensure_ascii=False))
        else:
            print('随机种子:' + '\n')
            for name, value in combo.items():
                print(f'  {name}: {value}')
        sys.exit(0)

    # 获取数量参数
    count_index = args.index('--count') if '--count' in args else -1
    count = 1
    if count_index != -1 and count_index + 1 < len(args):
        try:
            count = int(args[count_index + 1])
        except ValueError:
            count = 1

    # 构建需要跳过的参数索引集合
    skip_indices: set[int] = set()
    if file_index != -1:
        skip_indices.add(file_index)
        skip_indices.add(file_index + 1)
    if count_index != -1:
        skip_indices.add(count_index)
        skip_indices.add(count_index + 1)

    # 获取指定的列表名
    list_name = None
    for i in range(len(args)):
        if not args[i].startswith('--') and i not in skip_indices:
            list_name = args[i]
            break

    if not list_name:
        print('错误: 未指定列表名。使用 --list 查看可用选项。', file=sys.stderr)
        sys.exit(1)

    if list_name not in lists:
        print(f'错误: 未知列表 "{list_name}"。使用 --list 查看可用选项。', file=sys.stderr)
        sys.exit(1)

    selected = random_from(lists[list_name], count)

    if json_output:
        print(json.dumps(selected, indent=2, ensure_ascii=False))
    else:
        if count == 1:
            print(selected[0])
        else:
            for item in selected:
                print(f'• {item}')


if __name__ == '__main__':
    main()
