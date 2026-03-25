"""
导入小说实体扫描器

用 jieba（已有依赖）做轻量实体扫描，零 LLM 调用、零新依赖。
三信号融合：POS 标注 + 高频词统计 + 对话模式正则。
输出填充 knowledge/index.md 的实体目录，供 Agent 按需深化。
"""

from __future__ import annotations

import logging
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field

import jieba
import jieba.posseg as pseg

logger = logging.getLogger(__name__)

# ── 停用词（高频但非实体的 2-3 字词） ──

_STOPWORDS: frozenset[str] = frozenset({
    # 代词/指示词
    "什么", "这个", "那个", "自己", "我们", "他们", "她们", "你们",
    "这里", "那里", "哪里", "大家", "所有", "任何", "这些", "那些",
    "别人", "对方", "其他", "有些", "一些", "每个", "谁的",
    # 常见动词
    "知道", "以为", "看到", "听到", "感觉", "觉得", "认为", "开始",
    "已经", "可以", "应该", "不是", "没有", "不会", "成为", "变得",
    "出现", "发现", "存在", "需要", "能够", "或者", "如何", "怎么",
    "不能", "不要", "必须", "看着", "说道", "想到", "回到", "来到",
    "走到", "跑到", "飞到", "落到", "拿起", "放下", "站在", "坐在",
    "看向", "望向", "冲向", "走向", "朝着", "拿着", "带着", "跟着",
    # 时间词
    "时候", "现在", "之前", "之后", "今天", "明天", "以前", "以后",
    "突然", "终于", "慢慢", "一直", "马上", "忽然", "然后", "刚才",
    "顿时", "随后", "接着", "紧接", "瞬间", "此时", "此刻", "当时",
    # 常见名词
    "东西", "地方", "事情", "问题", "样子", "声音", "目光", "身体",
    "力量", "气息", "空间", "世界", "身上", "心中", "脸上", "手中",
    "眼中", "面前", "身后", "头上", "身边", "周围", "四周", "上方",
    "下方", "前方", "后方", "左右", "之中", "之上", "之下", "里面",
    "外面", "旁边", "中间", "对面", "一旁", "附近",
    # 副词/连词/助词
    "但是", "如果", "虽然", "因为", "所以", "不过", "而且", "只是",
    "就是", "也是", "还是", "竟然", "居然", "果然", "似乎", "仿佛",
    "简直", "几乎", "根本", "完全", "一定", "绝对", "到底", "究竟",
    "难道", "毕竟", "一般", "原来", "其实", "确实", "真的", "当然",
    # 量词/数词相关
    "一个", "两个", "一些", "一种", "一片", "一道", "一股", "一声",
    "一阵", "一丝", "一点", "一下", "一时", "一步", "这种", "那种",
})

# ── 对话模式正则 ──

_DIALOG_PATTERNS: list[re.Pattern] = [
    # "......"萧炎笑道 / 萧炎说道："......"
    re.compile(
        r'(?:[""「」].*?[""「」])\s{0,2}([\u4e00-\u9fff]{2,4})'
        r'(?:说道|说|道|笑道|问道|叫道|喊道|冷笑道|轻笑道|低声道|沉声道|怒道|惊道|叹道|喃喃道|淡淡道|冷声道|微笑道|大笑道|苦笑道|嘀咕道|低声说|沉声说|冷声说)'
    ),
    re.compile(
        r'([\u4e00-\u9fff]{2,4})'
        r'(?:说道|笑道|问道|叫道|喊道|冷笑道|轻笑道|低声道|沉声道|怒道|惊道|叹道|喃喃道|淡淡道|冷声道|微笑道|大笑道|苦笑道|嘀咕道|低声说|沉声说|冷声说)'
        r'\s{0,2}(?:[：:""「])'
    ),
    # 退化模式：XXX道/说（短匹配，仅作补充）
    re.compile(
        r'([\u4e00-\u9fff]{2,4})(?:说道|笑道|问道|冷笑道|叹道|怒道|惊道)'
    ),
]


@dataclass
class EntityInfo:
    """单个实体的扫描结果。"""
    name: str
    frequency: int = 0
    chapter_count: int = 0
    first_chapter: int = 0
    last_chapter: int = 0


@dataclass
class ScanResult:
    """全部扫描结果。"""
    characters: list[EntityInfo] = field(default_factory=list)
    locations: list[EntityInfo] = field(default_factory=list)
    total_chapters: int = 0
    latest_chapter_title: str = ""


def scan_entities(
    chapters: list[tuple[int, str, str]],
    max_characters: int = 50,
    max_locations: int = 30,
) -> ScanResult:
    """扫描章节文本，提取角色和地点实体。

    Args:
        chapters: [(章节号, 标题, 正文), ...]
        max_characters: 最多返回多少个角色
        max_locations: 最多返回多少个地点

    Returns:
        ScanResult
    """
    if not chapters:
        return ScanResult()

    chapters_sorted = sorted(chapters, key=lambda c: c[0])
    total = len(chapters_sorted)
    latest_num, latest_title, _ = chapters_sorted[-1]

    # ── 累积器 ──
    # name → 总频次
    word_freq: Counter[str] = Counter()
    # name → 出现过的章节号集合
    word_chapters: defaultdict[str, set[int]] = defaultdict(set)
    # 对话模式命中次数
    dialog_hits: Counter[str] = Counter()
    # POS 标注命中（nr / ns）
    pos_nr_hits: set[str] = set()
    pos_ns_hits: set[str] = set()

    for idx, (ch_num, _title, text) in enumerate(chapters_sorted):
        # ── 信号 ②：全量 jieba 分词 + 词频 ──
        words = jieba.lcut(text)
        for w in words:
            if len(w) < 2 or len(w) > 4:
                continue
            if w in _STOPWORDS:
                continue
            # 过滤纯标点/数字/英文
            if not re.search(r'[\u4e00-\u9fff]', w):
                continue
            word_freq[w] += 1
            word_chapters[w].add(ch_num)

        # ── 信号 ①：POS 标注（每 5 章采样 1 章） ──
        if idx % 5 == 0:
            for word, flag in pseg.cut(text):
                if len(word) < 2 or len(word) > 4:
                    continue
                if flag == "nr":
                    pos_nr_hits.add(word)
                elif flag == "ns":
                    pos_ns_hits.add(word)

        # ── 信号 ③：对话模式正则 ──
        for pattern in _DIALOG_PATTERNS:
            for match in pattern.finditer(text):
                name = match.group(1)
                if name and name not in _STOPWORDS and len(name) >= 2:
                    dialog_hits[name] += 1

    # ── 融合：角色候选 ──
    character_candidates: dict[str, float] = {}
    for name in set(dialog_hits.keys()) | pos_nr_hits:
        if name in _STOPWORDS:
            continue
        freq = word_freq.get(name, 0)
        ch_count = len(word_chapters.get(name, set()))
        d_hits = dialog_hits.get(name, 0)
        if freq < 5 and d_hits < 2:
            continue
        # 归一化评分
        freq_score = min(freq / 100, 10.0)
        spread_score = min(ch_count / max(total * 0.1, 1), 10.0)
        dialog_score = min(d_hits / 10, 10.0)
        score = freq_score * 0.5 + spread_score * 0.3 + dialog_score * 0.2
        character_candidates[name] = score

    # 按评分排序，取 top N
    sorted_chars = sorted(character_candidates.items(), key=lambda x: -x[1])[:max_characters]

    characters = []
    for name, _score in sorted_chars:
        chs = word_chapters.get(name, set())
        characters.append(EntityInfo(
            name=name,
            frequency=word_freq.get(name, 0),
            chapter_count=len(chs),
            first_chapter=min(chs) if chs else 0,
            last_chapter=max(chs) if chs else 0,
        ))

    # ── 融合：地点候选 ──
    location_candidates: dict[str, float] = {}
    for name in pos_ns_hits:
        if name in _STOPWORDS:
            continue
        freq = word_freq.get(name, 0)
        ch_count = len(word_chapters.get(name, set()))
        if freq < 3 or ch_count < 2:
            continue
        freq_score = min(freq / 50, 10.0)
        spread_score = min(ch_count / max(total * 0.05, 1), 10.0)
        score = freq_score * 0.6 + spread_score * 0.4
        location_candidates[name] = score

    sorted_locs = sorted(location_candidates.items(), key=lambda x: -x[1])[:max_locations]

    locations = []
    for name, _score in sorted_locs:
        chs = word_chapters.get(name, set())
        locations.append(EntityInfo(
            name=name,
            frequency=word_freq.get(name, 0),
            chapter_count=len(chs),
            first_chapter=min(chs) if chs else 0,
            last_chapter=max(chs) if chs else 0,
        ))

    return ScanResult(
        characters=characters,
        locations=locations,
        total_chapters=total,
        latest_chapter_title=latest_title,
    )


def _format_freq(n: int) -> str:
    """格式化频次显示：12345 → '12000+'。"""
    if n >= 10000:
        return f"{n // 1000 * 1000}+"
    if n >= 1000:
        return f"{n // 100 * 100}+"
    if n >= 100:
        return f"{n // 10 * 10}+"
    return str(n)


def format_index_md(result: ScanResult) -> str:
    """根据扫描结果生成完整的 index.md 内容。"""
    lines = [
        "# 作品知识索引",
        "",
        "> 全局速查表。写作前先看这里，了解故事当前全貌。有重要变化时随手更新。",
        "",
        "## 进度",
        f"- 当前章节：第{result.total_chapters}章",
        "- 当前阶段：（待 Agent 补充）",
        "- 主线推进：（待 Agent 补充）",
        "",
    ]

    # 人物速查
    if result.characters:
        lines.append("## 人物速查（自动扫描，待 Agent 补充详细档案）")
        lines.append("> 每个角色一行。详细档案见 characters/ 目录。")
        lines.append("")
        for c in result.characters:
            ch_range = f"Ch.{c.first_chapter}-{c.last_chapter}" if c.first_chapter != c.last_chapter else f"Ch.{c.first_chapter}"
            lines.append(f"- {c.name} | 频次 {_format_freq(c.frequency)} | {ch_range}")
        lines.append("")
    else:
        lines.append("## 人物速查")
        lines.append("> 每个角色一行：名字 | 身份 | 当前状态 | 当前位置。详细档案见 characters/ 目录。")
        lines.append("")
        lines.append("（暂无角色）")
        lines.append("")

    # 地点速查
    if result.locations:
        lines.append("## 地点速查（自动扫描）")
        lines.append("> 每个地点一行。详细档案见 locations/ 目录。")
        lines.append("")
        for loc in result.locations:
            ch_range = f"Ch.{loc.first_chapter}-{loc.last_chapter}" if loc.first_chapter != loc.last_chapter else f"Ch.{loc.first_chapter}"
            lines.append(f"- {loc.name} | 频次 {_format_freq(loc.frequency)} | {ch_range}")
        lines.append("")
    else:
        lines.append("## 地点速查")
        lines.append("> 每个地点一行：名字 | 类型 | 当前状态。详细档案见 locations/ 目录。")
        lines.append("")
        lines.append("（暂无地点）")
        lines.append("")

    # 保留占位符段落
    lines.extend([
        "## 活跃支线",
        "> 正在推进的剧情线。停滞超过 20 章的支线标记 [停滞]。",
        "",
        "（待 Agent 补充）",
        "",
        "## 待兑现伏笔",
        "> 已埋下但尚未揭示的伏笔。格式：[埋设章节] 内容 → 预计揭示时机",
        "",
        "（待 Agent 补充）",
        "",
    ])

    return "\n".join(lines)


def merge_scan_into_index(existing_content: str, result: ScanResult) -> str:
    """将扫描结果合并到已有的 index.md 中。

    策略：
    - 如果"人物速查"段含"自动扫描"标记 → 替换该段
    - 否则 → 保持不动（Agent 可能已手动编辑）
    - "进度"段始终更新章节数
    - 其他段落保持不动
    """
    # 如果已有内容含"自动扫描"标记，说明是上一次扫描的结果，直接用新结果覆盖
    if "自动扫描" in existing_content:
        return format_index_md(result)

    # 已有内容不含"自动扫描"（可能是空模板或 Agent 编辑过的）
    # 尝试更新"进度"段和"人物速查"段中的占位符
    updated = existing_content

    # 更新章节进度
    updated = re.sub(
        r'(- 当前章节：).*',
        rf'\g<1>第{result.total_chapters}章',
        updated,
    )

    # 替换"（暂无角色）"占位符
    if "（暂无角色）" in updated and result.characters:
        char_lines = []
        for c in result.characters:
            ch_range = f"Ch.{c.first_chapter}-{c.last_chapter}" if c.first_chapter != c.last_chapter else f"Ch.{c.first_chapter}"
            char_lines.append(f"- {c.name} | 频次 {_format_freq(c.frequency)} | {ch_range}")
        # 替换占位符，同时更新段标题
        updated = updated.replace(
            "## 人物速查\n> 每个角色一行：名字 | 身份 | 当前状态 | 当前位置。详细档案见 characters/ 目录。\n\n（暂无角色）",
            "## 人物速查（自动扫描，待 Agent 补充详细档案）\n> 每个角色一行。详细档案见 characters/ 目录。\n\n" + "\n".join(char_lines),
        )

    # 替换"（暂无地点）"占位符
    if "（暂无地点）" in updated and result.locations:
        loc_lines = []
        for loc in result.locations:
            ch_range = f"Ch.{loc.first_chapter}-{loc.last_chapter}" if loc.first_chapter != loc.last_chapter else f"Ch.{loc.first_chapter}"
            loc_lines.append(f"- {loc.name} | 频次 {_format_freq(loc.frequency)} | {ch_range}")
        updated = updated.replace(
            "## 地点速查\n> 每个地点一行：名字 | 类型 | 当前状态。详细档案见 locations/ 目录。\n\n（暂无地点）",
            "## 地点速查（自动扫描）\n> 每个地点一行。详细档案见 locations/ 目录。\n\n" + "\n".join(loc_lines),
        )

    return updated
