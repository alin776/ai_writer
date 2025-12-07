"""角色提取器

提供统一的角色名提取逻辑，基于特征过滤而非硬编码跳过词列表。

使用方式：
1. 优先从 AI 返回的结构化数据中获取 characters 字段
2. 兜底使用本模块的特征过滤提取
"""

import re
import logging
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)


# 常见中文姓氏（用于加分判断）
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
    # 复姓
    '欧阳', '太史', '端木', '上官', '司马', '东方', '独孤', '南宫',
    '万俟', '闻人', '夏侯', '诸葛', '尉迟', '公羊', '赫连', '澹台',
    '皇甫', '宗政', '濮阳', '公冶', '太叔', '申屠', '公孙', '慕容',
    '仲孙', '钟离', '长孙', '宇文', '司徒', '鲜于', '司空', '闾丘',
    '子车', '亓官', '司寇', '巫马', '公西', '颛孙', '壤驷', '公良',
    '漆雕', '乐正', '宰父', '谷梁', '拓跋', '夹谷', '轩辕', '令狐',
    '段干', '百里', '呼延', '东郭', '南门', '羊舌', '微生', '公户',
})


def is_likely_character_name(name: str) -> bool:
    """基于特征判断是否可能是角色名

    Args:
        name: 待判断的字符串

    Returns:
        True 如果可能是角色名，False 否则
    """
    if not name:
        return False

    # 1. 长度检查（人名通常2-4字，玄幻名可能更长如"血神宫主"）
    if not (2 <= len(name) <= 6):
        return False

    # 2. 排除纯 Markdown 标记
    if re.match(r'^[\*#\-_`~>]+$', name):
        return False

    # 3. 排除明显的非人名模式
    non_name_patterns = [
        # 以虚词/助词结尾
        r'.*[的地得了着过吗呢吧啊呀哦嘛]$',
        # 以动词后缀结尾
        r'.*[化性度感力]$',
        # 纯数字/序号
        r'^[一二三四五六七八九十百千万亿零\d]+$',
        # 结构性词汇（主题、情节等抽象概念）
        r'^(主题|情节|冲突|发展|背景|开端|高潮|结尾|结局)$',
        # 文档类词汇
        r'^(小说|内容|分析|报告|角色|人物|章节|描写|段落)$',
        # 抽象名词
        r'^(传承|新生|环境|象征|意义|形象|性格|动机|存在|展现|体现)$',
        # 动作/状态词
        r'^(开始|结束|进行|完成|发生|出现|变化|转变)$',
        # 评价类词汇
        r'^(精彩|优秀|出色|重要|关键|核心|主要|次要)$',
    ]

    for pattern in non_name_patterns:
        if re.match(pattern, name):
            return False

    # 4. 检查是否包含常见姓氏（强加分项）
    # 单姓
    if name[0] in COMMON_SURNAMES:
        return True
    # 复姓
    if len(name) >= 3 and name[:2] in COMMON_SURNAMES:
        return True

    # 5. 玄幻/武侠特殊名称模式（如"血神宫主"、"天机老人"）
    fantasy_patterns = [
        r'^.{1,2}(老人|道人|真人|仙子|圣女|魔君|神君|宫主|门主|掌门|长老|尊者|帝君)$',
        r'^(小|老|大|阿).{1,3}$',  # 小明、老张、大虎、阿福
    ]
    for pattern in fantasy_patterns:
        if re.match(pattern, name):
            return True

    # 6. 默认：2-4字的纯中文可能是角色名
    if re.match(r'^[\u4e00-\u9fa5]{2,4}$', name):
        return True

    return False


def clean_markdown(text: str) -> str:
    """清理 Markdown 标记

    Args:
        text: 可能包含 Markdown 标记的文本

    Returns:
        清理后的纯文本
    """
    if not text:
        return ""

    text = text.strip()
    # 移除首尾的 * （粗体/斜体）
    text = re.sub(r'^\*+|\*+$', '', text)
    # 移除首尾的 _ （斜体）
    text = re.sub(r'^_+|_+$', '', text)
    # 移除开头的 # （标题）
    text = re.sub(r'^#+\s*', '', text)
    # 移除开头的 - 或 * （列表项）
    text = re.sub(r'^[-*]\s+', '', text)

    return text.strip()


def extract_characters_from_text(
    text: str,
    max_count: int = 10,
    min_frequency: int = 2
) -> List[str]:
    """从文本中提取角色名（基于特征过滤）

    Args:
        text: 待提取的文本
        max_count: 最大返回数量
        min_frequency: 最小出现频率

    Returns:
        提取到的角色名列表
    """
    if not text:
        return []

    characters = []

    # 方法1：匹配编号列表格式，如 "1. 张三丰"、"2. 觉远"
    numbered_pattern = re.findall(
        r'\d+[\.、]\s*([^\n\d]{2,10}?)(?=\n|$|[：:])',
        text
    )
    for name in numbered_pattern:
        name = clean_markdown(name)
        if name and is_likely_character_name(name) and name not in characters:
            characters.append(name)

    # 方法2：查找"人物"或"角色"相关段落中的名字
    char_sections = re.findall(
        r'(?:人物|角色|主角|配角|登场人物)[：:]*\s*\n?([\s\S]{0,1500}?)(?=\n[一二三四五六七八九十]+[、\.：:]|\n##|\n\n|$)',
        text
    )
    for section in char_sections:
        # 提取可能的名字
        names = re.findall(r'[\u4e00-\u9fa5]{2,6}', section)
        for name in names:
            name = clean_markdown(name)
            if name and is_likely_character_name(name) and name not in characters:
                characters.append(name)

    # 方法3：高频词统计（出现 min_frequency 次以上的2-4字中文词）
    if len(characters) < max_count // 2:
        all_names = re.findall(r'[\u4e00-\u9fa5]{2,4}', text)
        name_freq = {}
        for name in all_names:
            name = clean_markdown(name)
            if name and is_likely_character_name(name):
                name_freq[name] = name_freq.get(name, 0) + 1

        # 按频率排序，添加高频名字
        for name, freq in sorted(name_freq.items(), key=lambda x: -x[1]):
            if freq >= min_frequency and name not in characters:
                characters.append(name)
                if len(characters) >= max_count:
                    break

    # 去重并限制数量
    unique_chars = list(dict.fromkeys(characters))[:max_count]

    if unique_chars:
        logger.debug(f"[角色提取] 从文本中提取到 {len(unique_chars)} 个角色: {unique_chars}")

    return unique_chars


def extract_characters_from_structured_data(
    data: Dict[str, Any],
    fallback_text: str = ""
) -> List[str]:
    """从结构化数据中提取角色（优先使用 characters 字段）

    这是推荐的主入口函数，实现了"结构化优先，特征过滤兜底"的策略。

    Args:
        data: AI 返回的结构化数据（可能包含 characters 字段）
        fallback_text: 当没有 characters 字段时，用于特征提取的文本

    Returns:
        角色名列表
    """
    # 优先：直接使用 AI 返回的 characters 字段
    if "characters" in data:
        chars = data["characters"]
        if isinstance(chars, list) and chars:
            # 清理并验证
            cleaned = []
            for c in chars:
                if isinstance(c, str):
                    c = clean_markdown(c)
                    if c and is_likely_character_name(c):
                        cleaned.append(c)
                elif isinstance(c, dict) and "name" in c:
                    name = clean_markdown(str(c["name"]))
                    if name and is_likely_character_name(name):
                        cleaned.append(name)

            if cleaned:
                logger.info(f"[角色提取] 从结构化数据中获取 {len(cleaned)} 个角色: {cleaned}")
                return cleaned

    # 兜底：从文本中特征提取
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
