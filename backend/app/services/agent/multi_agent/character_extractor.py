"""角色提取器 v2.0

使用 jieba 分词 + 词性标注进行角色识别，替代硬编码的过滤规则。

策略优先级：
1. 优先从 AI 返回的结构化数据中获取 characters 字段（最可靠）
2. 使用 jieba 词性标注识别人名（nr 标签）
3. 高频专有名词兜底（姓氏开头 + 高频出现）
"""

import re
import logging
from typing import List, Dict, Any
from collections import Counter

logger = logging.getLogger(__name__)

# 尝试导入 jieba，如果失败则使用降级方案
try:
    import jieba
    import jieba.posseg as pseg
    JIEBA_AVAILABLE = True
    # 静默加载，避免日志污染
    jieba.setLogLevel(logging.WARNING)
except ImportError:
    JIEBA_AVAILABLE = False
    logger.warning("[角色提取] jieba 未安装，将使用降级方案")


# 人名上下文模式（正面信号：词语作为人名使用）
NAME_CONTEXT_PATTERNS = [
    r'{name}[说道笑叹问答喊叫想看听]',   # 动作主语：安静说
    r'[给向对跟和与叫让请派]{name}',     # 介词宾语：给安静
    r'[是叫唤名为]"{name}"',             # 引号内的名字
    r'[是叫唤名为]{name}[，。]',         # 称谓语境：叫安静
]

# 非人名上下文模式（负面信号：词语作为形容词/地名使用）
NON_NAME_CONTEXT_PATTERNS = [
    # 形容词/副词用法
    r'{name}[地得]',                      # 安静地、安静得
    r'[很非十分格外特别相当][常分外]?{name}',  # 很安静、非常安静
    r'变[得]?{name}',                     # 变得安静
    r'{name}[了着过](?![来去])',          # 安静了、安静着（但不是"山了"）
    # 地名用法
    r'[在到去往来从离出入进]{name}',      # 在少林寺、到武当山
    r'{name}[里外中内边旁]',              # 寺里、山中
    r'{name}[上下前后左右]',              # 山上、城下
]


# 常见中文姓氏（用于降级方案和辅助判断）
COMMON_SURNAMES = frozenset({
    '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈',
    '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
    '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏',
    '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
    '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦',
    '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
    '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺',
    '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
    '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余',
    '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
    '姚', '邵', '湛', '汪', '祁', '毛', '禹', '狄', '米', '贝',
    '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
    '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '杜', '阮',
    '蓝', '闵', '席', '季', '麻', '强', '贾', '路', '娄', '危',
    '欧阳', '太史', '端木', '上官', '司马', '东方', '独孤', '南宫',
    '万俟', '闻人', '夏侯', '诸葛', '尉迟', '公羊', '赫连', '澹台',
    '皇甫', '宗政', '濮阳', '公冶', '太叔', '申屠', '公孙', '慕容',
    '仲孙', '钟离', '长孙', '宇文', '司徒', '鲜于', '司空', '闾丘',
})


def clean_markdown(text: str) -> str:
    """清理 Markdown 标记"""
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r'^\*+|\*+$', '', text)  # 移除 *
    text = re.sub(r'^_+|_+$', '', text)    # 移除 _
    text = re.sub(r'^#+\s*', '', text)     # 移除 #
    text = re.sub(r'^[-*]\s+', '', text)   # 移除列表标记
    return text.strip()


def _get_context_score(word: str, text: str) -> float:
    """基于上下文计算词作为人名的置信度分数

    纯语法规则判断，无硬编码词汇黑名单：
    - 正面模式（人名用法）：+分
    - 负面模式（形容词/地名用法）：-分

    Args:
        word: 候选词
        text: 原始文本

    Returns:
        置信度分数（可正可负）
    """
    if not word or not text:
        return 0.0

    score = 0.0
    escaped_name = re.escape(word)

    # 正面信号：人名用法模式
    for pattern in NAME_CONTEXT_PATTERNS:
        if re.search(pattern.format(name=escaped_name), text):
            score += 0.4
            break  # 只计一次

    # 负面信号：形容词/地名用法模式
    for pattern in NON_NAME_CONTEXT_PATTERNS:
        if re.search(pattern.format(name=escaped_name), text):
            score -= 0.5
            break  # 只计一次

    # 词频信号：出现多次更可能是角色
    count = len(re.findall(re.escape(word), text))
    if count >= 5:
        score += 0.3
    elif count >= 3:
        score += 0.2
    elif count >= 2:
        score += 0.1

    return score


def _is_valid_character_name(word: str, text: str = "") -> bool:
    """验证词是否是有效的角色名

    综合判断逻辑：
    1. 姓氏开头 + 无负面上下文 → 通过
    2. 有正面上下文（人名用法） → 通过
    3. 有负面上下文（形容词/地名用法） → 拒绝

    Args:
        word: 候选角色名
        text: 原始文本（用于上下文验证）

    Returns:
        True 如果是有效的角色名
    """
    if not word or len(word) < 2:
        return False

    # 姓氏开头检查
    is_surname_start = (
        word[0] in COMMON_SURNAMES or
        (len(word) >= 3 and word[:2] in COMMON_SURNAMES)
    )

    # 如果没有文本上下文，只依赖姓氏判断
    if not text:
        return is_surname_start

    # 计算上下文分数
    context_score = _get_context_score(word, text)

    # 判断逻辑：
    # 1. 负面分数过低（明显是形容词/地名用法）→ 拒绝
    if context_score < -0.3:
        return False

    # 2. 正面分数较高（明显是人名用法）→ 通过
    if context_score >= 0.3:
        return True

    # 3. 中性情况：姓氏开头则通过
    return is_surname_start


def _is_character_by_context(name: str, text: str) -> bool:
    """通过上下文模式验证候选词是否是真正的角色名

    策略：检查词语是否出现在典型的人名语境中，如 "XXX说"、"给XXX"

    Args:
        name: 候选角色名
        text: 原始文本

    Returns:
        True 如果候选词通过上下文验证
    """
    # 使用置信度分数判断
    return _get_context_score(name, text) >= 0.3


def _extract_by_jieba(text: str, max_count: int = 10) -> List[str]:
    """使用 jieba 词性标注提取人名

    jieba 词性标签：
    - nr: 人名（高优先级，但仍需验证）
    - nrt: 音译人名（高优先级）
    - nrfg: 人名更宽泛（高优先级）

    所有候选词都会通过 _is_valid_character_name 验证，
    排除地名、助词等误识别情况。
    """
    if not JIEBA_AVAILABLE or not text:
        return []

    # 词性标注
    words = pseg.cut(text)

    # 收集候选词
    person_tags = {'nr', 'nrt', 'nrfg'}
    high_priority = []   # nr 标签的词（高优先级）
    low_priority = []    # 其他可能的人名

    for word, flag in words:
        word = word.strip()
        if not word or len(word) < 2:
            continue

        # 人名标签：高优先级
        if flag in person_tags:
            high_priority.append(word)
        # 普通名词/专有名词，以姓氏开头：低优先级
        elif flag in {'n', 'nz'} and word[0] in COMMON_SURNAMES:
            low_priority.append(word)

    # 对所有候选词进行验证
    candidates = []

    # 先处理高优先级（nr 标签）
    for word in high_priority:
        if _is_valid_character_name(word, text):
            candidates.append(word)

    # 再处理低优先级
    for word in low_priority:
        if word not in candidates and _is_valid_character_name(word, text):
            candidates.append(word)

    # 去重并保持顺序
    seen = set()
    unique = []
    for name in candidates:
        if name not in seen:
            seen.add(name)
            unique.append(name)

    return unique[:max_count]


def _extract_by_frequency(text: str, max_count: int = 10, min_freq: int = 2) -> List[str]:
    """降级方案：基于姓氏 + 高频出现识别人名

    逻辑：以常见姓氏开头 + 出现次数 >= min_freq 的2-4字词
    同时排除地名后缀等误识别情况。
    """
    if not text:
        return []

    # 提取所有2-4字的中文词
    all_words = re.findall(r'[\u4e00-\u9fa5]{2,4}', text)

    # 统计词频
    freq = Counter(all_words)

    # 筛选：以姓氏开头 + 高频 + 通过验证
    candidates = []
    for word, count in freq.most_common():
        if count < min_freq:
            break
        # 检查是否以常见姓氏开头
        is_surname_start = word[0] in COMMON_SURNAMES or (len(word) >= 3 and word[:2] in COMMON_SURNAMES)
        if is_surname_start and _is_valid_character_name(word, text):
            candidates.append(word)
            if len(candidates) >= max_count:
                break

    return candidates


def _extract_from_structured_text(text: str, max_count: int = 10) -> List[str]:
    """从结构化文本中提取角色（如编号列表、角色段落）"""
    if not text:
        return []

    characters = []

    # 方法1：匹配编号列表格式，如 "1. 张三丰"、"- 觉远"
    patterns = [
        r'\d+[\.、）)]\s*[【\[]?([^\n\d【\]]{2,8}?)[】\]]?(?=\n|$|[：:，,])',  # 1. 张三丰
        r'[-•]\s*[【\[]?([^\n\-•【\]]{2,8}?)[】\]]?(?=\n|$|[：:，,])',          # - 张三丰
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for name in matches:
            name = clean_markdown(name).strip()
            if name and 2 <= len(name) <= 6 and name not in characters:
                # 验证：纯中文（结构化列表中的名字通常是可信的）
                if re.match(r'^[\u4e00-\u9fa5]+$', name):
                    characters.append(name)

    # 方法2：查找"人物"或"角色"段落
    char_section = re.search(
        r'(?:人物|角色|主角|配角|登场人物)[：:]*\s*\n?([\s\S]{0,500}?)(?=\n\n|\n[一二三四五六七八九十]|$)',
        text
    )
    if char_section:
        section_text = char_section.group(1)
        # 使用 jieba 或降级方案提取
        if JIEBA_AVAILABLE:
            names = _extract_by_jieba(section_text, max_count=5)
        else:
            names = _extract_by_frequency(section_text, max_count=5)
        for name in names:
            if name not in characters:
                characters.append(name)

    return characters[:max_count]


def extract_characters_from_text(
    text: str,
    max_count: int = 10,
    min_frequency: int = 2
) -> List[str]:
    """从文本中提取角色名（主入口）

    策略：
    1. 先从结构化格式中提取（编号列表、角色段落）
    2. 使用 jieba 词性标注识别人名
    3. 高频姓氏词兜底

    Args:
        text: 待提取的文本
        max_count: 最大返回数量
        min_frequency: 高频词最小出现次数

    Returns:
        提取到的角色名列表
    """
    if not text:
        return []

    characters = []

    # Step 1: 从结构化文本提取
    structured_chars = _extract_from_structured_text(text, max_count)
    characters.extend(structured_chars)

    # Step 2: jieba 词性标注提取
    if len(characters) < max_count and JIEBA_AVAILABLE:
        jieba_chars = _extract_by_jieba(text, max_count)
        for name in jieba_chars:
            if name not in characters:
                characters.append(name)

    # Step 3: 高频词兜底
    if len(characters) < max_count // 2:
        freq_chars = _extract_by_frequency(text, max_count, min_frequency)
        for name in freq_chars:
            if name not in characters:
                characters.append(name)

    # 去重并限制数量
    result = list(dict.fromkeys(characters))[:max_count]

    if result:
        logger.info(f"[角色提取] 提取到 {len(result)} 个角色: {result}")

    return result


def extract_characters_from_structured_data(
    data: Dict[str, Any],
    fallback_text: str = ""
) -> List[str]:
    """从结构化数据中提取角色（优先使用 characters 字段）

    这是推荐的主入口函数，实现了"结构化优先，NLP 兜底"的策略。
    """
    # 优先：直接使用 AI 返回的 characters 字段
    if "characters" in data:
        chars = data["characters"]
        if isinstance(chars, list) and chars:
            cleaned = []
            for c in chars:
                if isinstance(c, str):
                    c = clean_markdown(c)
                    if c and 2 <= len(c) <= 10:
                        cleaned.append(c)
                elif isinstance(c, dict) and "name" in c:
                    name = clean_markdown(str(c["name"]))
                    if name and 2 <= len(name) <= 10:
                        cleaned.append(name)

            if cleaned:
                logger.info(f"[角色提取] 从结构化数据获取 {len(cleaned)} 个角色: {cleaned}")
                return cleaned

    # 兜底：从文本中提取
    if fallback_text:
        return extract_characters_from_text(fallback_text)

    # 尝试从 data 中找可用的文本字段
    for key in ["analysis_result", "previous_summary", "content", "text"]:
        if key in data and isinstance(data[key], str) and data[key]:
            return extract_characters_from_text(data[key])

    return []


def check_character_presence(
    content: str,
    expected_chars: List[str],
    threshold: float = 0.2
) -> Dict[str, Any]:
    """检查内容中角色的出现情况

    Args:
        content: 待检查的内容
        expected_chars: 预期应该出现的角色
        threshold: 判定为"跑题"的阈值（低于此比例视为跑题）

    Returns:
        检查结果字典
    """
    if not expected_chars:
        return {
            "match_count": 0,
            "total": 0,
            "found": [],
            "missing": [],
            "match_ratio": 1.0,
            "is_off_topic": False
        }

    found = [c for c in expected_chars if c in content]
    missing = [c for c in expected_chars if c not in content]
    match_ratio = len(found) / len(expected_chars)

    return {
        "match_count": len(found),
        "total": len(expected_chars),
        "found": found,
        "missing": missing,
        "match_ratio": match_ratio,
        "is_off_topic": match_ratio < threshold
    }
