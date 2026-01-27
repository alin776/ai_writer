# -*- coding: utf-8 -*-
"""
Explore 内容探索工具（AI 驱动版本）

实现深度内容探索的核心逻辑：
1. AI 理解任务，生成探索计划
2. AI 每轮决定搜索策略
3. AI 判断信息充足性
4. 流式事件支持前端展示

Version: 2.0 - AI 驱动的 SubAgent 模式
"""

import json
import logging
import re
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Any, Optional, Callable, Awaitable
from datetime import datetime

from langchain_core.tools import tool
from .tool_registry import register_as_tool
from app.utils.datetime_utils import get_utc_now
from app.services.agent.utils.tool_context import get_stream_event_handler, get_explore_step_id
from app.services.agent.utils.performance import MemoryCache
from app.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)

MIN_EVIDENCE_SIMILARITY = 0.35
AUTO_LOCATE_LIMIT = 3
AUTO_READ_LIMIT = 3
AUTO_LOCATE_LIMIT_STRICT = 12
AUTO_READ_LIMIT_STRICT = 12
LOCATE_QUERY_MAX_LEN = 200

TOOL_LOOP_MAX_CALLS_DEFAULT = 200
TOOL_LOOP_MAX_READS_DEFAULT = 60
TOOL_LOOP_RESULT_PREVIEW_LIMIT = 1200
TOOL_LOOP_ALLOWED_TOOLS = (
    "list_chapters",
    "list_paragraphs",
    "exact_search_paragraphs",
    "read_paragraph",
    "read_paragraphs"
)

EXPLORE_SHARED_TTL_SECONDS = 20 * 60
_EXPLORE_SHARED_CACHE = MemoryCache(max_size=50, default_ttl=EXPLORE_SHARED_TTL_SECONDS)

PARAGRAPH_REQUIRED_KEYWORDS = (
    "段落号",
    "章节号+段落号",
    "章节号＋段落号",
    "章节号及段落号",
    "段落编号",
    "段落索引",
    "只允许精确段落读取",
    "只读段落",
    "仅段落",
)

UNREACHABLE_MISSING_KEYWORDS = (
    "作者",
    "首发平台",
    "正版平台",
    "阅读平台",
    "阅读渠道",
    "官方网站",
    "官网",
    "网站",
)

FULL_CHAPTER_REQUIRED_KEYWORDS = (
    "全部原文",
    "完整原文",
    "原文全文",
    "全文",
    "全章",
    "整章",
    "完整章节",
    "章节原文",
    "章节全文",
    "章原文",
)

FULL_CHAPTER_FORBIDDEN_KEYWORDS = (
    "不要整章",
    "不要整章阅读",
    "不读整章",
    "禁止整章",
    "避免整章",
    "不要全文",
    "不读全文",
    "不要全章",
    "不读全章",
    "仅段落",
    "只读段落",
    "只允许段落",
    "只允许精确段落",
    "只允许精确段落读取",
)

CHINESE_NUM_MAP = {
    "零": 0,
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}


def _truncate_text(text: str, max_len: int = 500) -> str:
    if not text:
        return ""
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


def _normalize_locate_query(query: str, max_len: int = LOCATE_QUERY_MAX_LEN) -> str:
    text = " ".join((query or "").split())
    if len(text) > max_len:
        text = text[:max_len]
    return text


def _requires_paragraph_index(target_task: str) -> bool:
    if not target_task:
        return False
    return any(keyword in target_task for keyword in PARAGRAPH_REQUIRED_KEYWORDS)


def _requires_unreachable_items(target_task: str) -> bool:
    if not target_task:
        return False
    return any(keyword in target_task for keyword in UNREACHABLE_MISSING_KEYWORDS)


def _requires_full_chapter(target_task: str) -> bool:
    if not target_task:
        return False
    if _forbid_full_chapter(target_task):
        return False
    return any(keyword in target_task for keyword in FULL_CHAPTER_REQUIRED_KEYWORDS)


def _forbid_full_chapter(target_task: str) -> bool:
    if not target_task:
        return False
    return any(keyword in target_task for keyword in FULL_CHAPTER_FORBIDDEN_KEYWORDS)


def _extract_keywords_for_search(target_task: str) -> List[str]:
    """
    从任务描述中提取搜索关键词（确定性，不用 AI）

    策略：
    1. 提取引号内的短语（用户明确指定）
    2. 提取中文书名号内的内容
    3. 使用 jieba 提取关键词
    4. 保留原始短语，不拆分

    Returns:
        List[str]: 去重后的关键词列表，按重要性排序
    """
    if not target_task:
        return []

    keywords = []
    seen = set()

    def add_keyword(kw: str):
        """添加关键词（去重）"""
        kw = kw.strip()
        if kw and len(kw) >= 2 and kw.lower() not in seen:
            seen.add(kw.lower())
            keywords.append(kw)

    # 1. 提取引号内的内容（最高优先级）
    # 支持中英文引号
    quote_patterns = [
        r'"([^"]+)"',      # 中文双引号
        r"'([^']+)'",      # 中文单引号
        r'"([^"]+)"',      # 英文双引号
        r"'([^']+)'",      # 英文单引号
    ]
    for pattern in quote_patterns:
        for match in re.findall(pattern, target_task):
            add_keyword(match)

    # 2. 提取书名号内的内容
    book_pattern = r'《([^》]+)》|〈([^〉]+)〉'
    for match in re.findall(book_pattern, target_task):
        for m in match:
            if m:
                add_keyword(m)

    # 3. 提取特定模式的关键词
    # 如：器灵等阶、吞噬要求、吞噬效果
    specific_patterns = [
        r'[\u4e00-\u9fa5]{2,6}(?:等阶|要求|效果|机制|规律|代价|副作用)',
        r'(?:关于|找到|搜索|检索)[\u4e00-\u9fa5"「『]{2,10}',
    ]
    for pattern in specific_patterns:
        for match in re.findall(pattern, target_task):
            # 清理匹配结果
            cleaned = re.sub(r'^(?:关于|找到|搜索|检索)', '', match)
            cleaned = re.sub(r'[「『""]', '', cleaned)
            add_keyword(cleaned)

    # 4. 使用 jieba 提取关键词（补充）
    try:
        import jieba.analyse
        # TF-IDF 提取
        jieba_keywords = jieba.analyse.extract_tags(target_task, topK=10)
        for kw in jieba_keywords:
            if len(kw) >= 2:  # 过滤单字
                add_keyword(kw)
    except Exception as e:
        logger.warning(f"[_extract_keywords] jieba 提取失败: {e}")

    # 5. 提取任务中的关键实体（中文名词短语）
    # 匹配 2-6 个连续汉字
    entity_pattern = r'[\u4e00-\u9fa5]{2,6}'
    entities = re.findall(entity_pattern, target_task)
    # 过滤常见停用词
    stopwords = {
        "需要", "找到", "搜索", "检索", "什么", "怎么", "如何", "哪些",
        "以及", "还有", "包括", "例如", "比如", "其中", "之间", "关系",
        "具体", "详细", "相关", "所有", "任务", "问题", "回答", "说明",
        "证据", "原文", "描述", "内容", "信息", "要求", "约束", "格式",
        "章节", "段落", "范围", "输出", "以下", "上述"
    }
    for entity in entities:
        if entity not in stopwords:
            add_keyword(entity)

    logger.info(f"[_extract_keywords] 提取关键词: {keywords[:10]}...")
    return keywords


def _chinese_to_int(text: str) -> Optional[int]:
    text = (text or "").strip()
    if not text:
        return None
    if text.isdigit():
        return int(text)
    if text in CHINESE_NUM_MAP:
        return CHINESE_NUM_MAP[text]
    if "十" in text:
        parts = text.split("十")
        tens_raw = parts[0]
        ones_raw = parts[1] if len(parts) > 1 else ""
        tens = CHINESE_NUM_MAP.get(tens_raw, 1 if tens_raw == "" else None)
        ones = CHINESE_NUM_MAP.get(ones_raw, 0 if ones_raw == "" else None)
        if tens is None or ones is None:
            return None
        return tens * 10 + ones
    return None


def _parse_chapter_scope(target_task: str) -> Optional[Tuple[int, int]]:
    if not target_task:
        return None
    text = target_task

    # 兼容 “第5章至第20章 / 第5章到第20章 / 第5-第20章”
    range_match = re.search(r"第\s*(\d+)\s*(?:章)?\s*[到至\-~—～–]\s*第?\s*(\d+)\s*章", text)
    if range_match:
        start = int(range_match.group(1))
        end = int(range_match.group(2))
        return (min(start, end), max(start, end))

    range_cn_match = re.search(r"第\s*([一二两三四五六七八九十]+)\s*章?\s*[到至\-~—～–]\s*第?\s*([一二两三四五六七八九十]+)\s*章", text)
    if range_cn_match:
        start = _chinese_to_int(range_cn_match.group(1))
        end = _chinese_to_int(range_cn_match.group(2))
        if isinstance(start, int) and isinstance(end, int):
            return (min(start, end), max(start, end))

    front_match = re.search(r"前\s*([\d一二两三四五六七八九十]+)\s*章", text)
    if front_match:
        count = _chinese_to_int(front_match.group(1))
        if isinstance(count, int) and count > 0:
            return (1, count)

    single_matches = re.findall(r"第\s*(\d+)\s*章", text)
    if single_matches:
        orders = sorted(int(v) for v in single_matches)
        return (orders[0], orders[-1])

    single_cn_matches = re.findall(r"第\s*([一二两三四五六七八九十]+)\s*章", text)
    if single_cn_matches:
        orders = sorted(v for v in (_chinese_to_int(v) for v in single_cn_matches) if isinstance(v, int))
        if orders:
            return (orders[0], orders[-1])

    return None


def _parse_chapter_scopes(target_task: str) -> List[Tuple[int, int]]:
    if not target_task:
        return []
    text = target_task
    scopes: List[Tuple[int, int]] = []

    # 2026-01-21: 先处理排除性描述，如"禁止使用第6章及以后的内容"
    # 这种情况下，用户想要的是第1章到第5章（排除第6章及以后）
    exclude_pattern = r"(?:禁止|不得|排除|不要|不可|勿|别)[^第]*第\s*(\d+)\s*章\s*(?:及|和)?(?:以后|之后|后面|往后)"
    exclude_cn_pattern = r"(?:禁止|不得|排除|不要|不可|勿|别)[^第]*第\s*([一二两三四五六七八九十]+)\s*章\s*(?:及|和)?(?:以后|之后|后面|往后)"

    exclude_match = re.search(exclude_pattern, text)
    if exclude_match:
        exclude_from = int(exclude_match.group(1))
        if exclude_from > 1:
            # 返回第1章到排除章节的前一章
            return [(1, exclude_from - 1)]
        else:
            # 禁止第1章及以后 = 无法搜索，返回空
            return []

    exclude_cn_match = re.search(exclude_cn_pattern, text)
    if exclude_cn_match:
        exclude_from = _chinese_to_int(exclude_cn_match.group(1))
        if isinstance(exclude_from, int) and exclude_from > 1:
            return [(1, exclude_from - 1)]
        elif isinstance(exclude_from, int):
            return []

    for match in re.finditer(r"第\s*(\d+)\s*(?:章)?\s*[到至\-~—～–]\s*第?\s*(\d+)\s*章", text):
        start = int(match.group(1))
        end = int(match.group(2))
        scopes.append((min(start, end), max(start, end)))

    for match in re.finditer(r"第\s*([一二两三四五六七八九十]+)\s*章?\s*[到至\-~—～–]\s*第?\s*([一二两三四五六七八九十]+)\s*章", text):
        start = _chinese_to_int(match.group(1))
        end = _chinese_to_int(match.group(2))
        if isinstance(start, int) and isinstance(end, int):
            scopes.append((min(start, end), max(start, end)))

    # 兼容"章节1-2""章节(1-2, 34-35)"等写法
    if "章节" in text:
        for match in re.finditer(r"章节\s*\(?\s*(\d+)\s*[到至\-~—～–]\s*(\d+)", text):
            start = int(match.group(1))
            end = int(match.group(2))
            scopes.append((min(start, end), max(start, end)))
        for match in re.finditer(r"章节\s*\(?\s*([一二两三四五六七八九十]+)\s*[到至\-~—～–]\s*([一二两三四五六七八九十]+)", text):
            start = _chinese_to_int(match.group(1))
            end = _chinese_to_int(match.group(2))
            if isinstance(start, int) and isinstance(end, int):
                scopes.append((min(start, end), max(start, end)))
        # 2026-01-27: 移除贪心正则，避免误匹配 UUID 中的数字
        # 原来的正则 r"(\d+)\s*[到至\-~—～]\s*(\d+)" 会匹配任何数字范围
        # 改为只匹配紧跟在"章节"后面、且范围合理（<=1000）的数字
        for match in re.finditer(r"章节[^第]*?(\d{1,3})\s*[到至\-~—～–]\s*(\d{1,3})(?!\s*章)", text):
            start = int(match.group(1))
            end = int(match.group(2))
            # 额外校验：范围不超过 1000 章，避免误匹配大数字
            if start <= 1000 and end <= 1000:
                scopes.append((min(start, end), max(start, end)))

    # 兼容“1-2章”写法
    for match in re.finditer(r"(\d+)\s*[到至\-~—～–]\s*(\d+)\s*章", text):
        start = int(match.group(1))
        end = int(match.group(2))
        scopes.append((min(start, end), max(start, end)))

    front_match = re.search(r"前\s*([\d一二两三四五六七八九十]+)\s*章", text)
    if front_match:
        count = _chinese_to_int(front_match.group(1))
        if isinstance(count, int) and count > 0:
            scopes.append((1, count))

    single_matches = re.findall(r"第\s*(\d+)\s*章", text)
    for value in single_matches:
        order = int(value)
        scopes.append((order, order))

    single_cn_matches = re.findall(r"第\s*([一二两三四五六七八九十]+)\s*章", text)
    for value in single_cn_matches:
        order = _chinese_to_int(value)
        if isinstance(order, int):
            scopes.append((order, order))

    if not scopes:
        return []

    scopes.sort(key=lambda item: (item[0], item[1]))
    merged: List[Tuple[int, int]] = []
    for start, end in scopes:
        if not merged:
            merged.append((start, end))
            continue
        prev_start, prev_end = merged[-1]
        if start <= prev_end + 1:
            merged[-1] = (prev_start, max(prev_end, end))
        else:
            merged.append((start, end))
    return merged


def _extract_title_chapter_number(title: str) -> Optional[int]:
    if not title:
        return None
    match = re.search(r"第\s*([0-9一二两三四五六七八九十]+)\s*章", title)
    if not match:
        return None
    return _chinese_to_int(match.group(1))


def _map_scopes_to_orders(
    scopes: List[Tuple[int, int]],
    title_order_map: Dict[int, int],
    total_chapters: int = 0
) -> List[Tuple[int, int]]:
    """将标题号范围映射到实际序号。

    2026-01-27 改进：映射失败时返回合理的默认范围，而非空列表。
    """
    if not scopes:
        return []

    if not title_order_map:
        # 无映射表时，如果有总章节数，限制范围；否则返回原始范围
        if total_chapters > 0:
            return [(max(1, s), min(e, total_chapters)) for s, e in scopes if s <= total_chapters]
        return scopes  # 保留原始范围

    mapped: List[Tuple[int, int]] = []
    for start, end in scopes:
        orders = [
            order for title_no, order in title_order_map.items()
            if start <= title_no <= end
        ]
        if not orders:
            # 2026-01-27: 映射失败时，尝试使用原始范围（限制在合理范围内）
            max_order = max(title_order_map.values()) if title_order_map else total_chapters
            if max_order > 0 and start <= max_order:
                # 原始范围有效，限制上界
                mapped.append((start, min(end, max_order)))
            continue
        mapped.append((min(orders), max(orders)))

    if not mapped:
        # 所有范围都映射失败，返回原始范围（限制在合理范围内）
        max_order = max(title_order_map.values()) if title_order_map else total_chapters
        if max_order > 0:
            return [(max(1, s), min(e, max_order)) for s, e in scopes if s <= max_order]
        return scopes  # 最后兜底：返回原始范围

    mapped.sort(key=lambda item: (item[0], item[1]))
    merged: List[Tuple[int, int]] = []
    for start, end in mapped:
        if not merged:
            merged.append((start, end))
            continue
        prev_start, prev_end = merged[-1]
        if start <= prev_end + 1:
            merged[-1] = (prev_start, max(prev_end, end))
        else:
            merged.append((start, end))
    return merged


def _extract_read_paragraph(result_data: Dict[str, Any]) -> Tuple[str, List[str], List[str]]:
    paragraphs = result_data.get("paragraphs", [])
    if not isinstance(paragraphs, list) or not paragraphs:
        return "", [], []

    target_index = result_data.get("target_index")
    target_text = ""
    context_before = []
    context_after = []

    for para in paragraphs:
        if not isinstance(para, dict):
            continue
        text = para.get("text", "")
        if para.get("is_target"):
            target_text = text
            continue
        para_index = para.get("index")
        if isinstance(target_index, int) and isinstance(para_index, int):
            if para_index < target_index:
                context_before.append(text)
            elif para_index > target_index:
                context_after.append(text)

    return target_text, context_before, context_after


# ==================== AI 服务 ====================

_ai_service = None

def _get_ai_service():
    """获取 AI 服务实例（懒初始化）"""
    global _ai_service
    if _ai_service is None:
        from app.services.ai.http_ai_service import HTTPAIService
        _ai_service = HTTPAIService()
    return _ai_service


# ==================== AI 决策数据结构 ====================

@dataclass
class RoundPlan:
    """AI 生成的单轮行动计划（V3：区分精确搜索和语义搜索）"""
    exact_keywords: List[str]         # 精确搜索关键词（找具体实体：人名、地名）
    semantic_queries: List[str]       # 语义搜索 query（找抽象概念：性格、关系）
    chapters_to_read: List[int]       # 本轮要读的章节
    paragraphs_to_read: List[Dict]    # 本轮要读的段落 [{"chapter": 3, "paragraph": 15}]
    reason: str                       # AI 决策理由


@dataclass
class SelfCheckDecision:
    """LLM 自检结果（是否继续 + 下一轮搜索方向）"""
    continue_search: bool
    next_queries: List[str]
    reason: str = ""


@dataclass
class ToolLoopDecision:
    """LLM 工具循环决策结果"""
    action: str
    tool: str = ""
    args: Dict[str, Any] = field(default_factory=dict)
    reason: str = ""


# ==================== 数据结构 ====================

@dataclass
class Evidence:
    """搜索到的证据片段"""
    text: str                    # 原文片段
    chapter_order: int           # 章节序号
    paragraph_index: Optional[int]  # 段落索引（可能为空）
    similarity: float            # 相似度
    source_type: str             # 来源类型
    query: str                   # 触发此结果的搜索词
    round_idx: int               # 第几轮搜索到的
    chapter_id: str = ""         # 章节ID（可选）
    chapter_title: str = ""      # 章节标题（可选）
    node_id: str = ""            # 节点ID（可选）


@dataclass
class ParagraphRead:
    """读取的段落原文"""
    chapter_order: int
    chapter_title: str
    paragraph_index: int
    text: str                    # 目标段落原文
    context_before: List[str]    # 前文段落
    context_after: List[str]     # 后文段落
    round_idx: int               # 第几轮读取的
    node_id: str = ""            # 节点ID（如果解析到）


@dataclass
class ChapterRead:
    """读取的章节原文"""
    id: str                      # 章节ID（2026-01-18 新增）
    order: int
    title: str
    content: str                 # 完整原文
    word_count: int
    round_idx: int               # 第几轮读取的


@dataclass
class WorldviewItem:
    """世界观条目"""
    id: str
    name: str
    category: str
    description: str
    attributes: Dict[str, Any]


@dataclass
class ToolCall:
    """单次工具调用"""
    tool_name: str
    params: Dict[str, Any]
    result: Any
    duration_ms: int


@dataclass
class ExploreRound:
    """单轮探索记录"""
    round_idx: int
    title: str                   # 轮次标题（固定简短标题）
    tool_calls: List[ToolCall]   # 本轮执行的工具
    new_evidences_count: int     # 本轮新增证据数
    new_paragraphs_count: int    # 本轮新增段落数
    missing_items: List[str]     # 缺失项
    sufficient: bool             # AI 判断是否充足
    reason: str = ""             # AI 生成的决策理由（完整）
    coverage: str = ""           # AI 覆盖度描述
    summary: str = ""            # AI 生成的探索总结
    next_action: str = ""        # AI 生成的下一步行动
    timestamp: datetime = field(default_factory=get_utc_now)


@dataclass
class ExploreState:
    """Explore 内部状态"""

    # ========== 收集到的内容（原样保留，不压缩）==========

    evidences: List[Evidence] = field(default_factory=list)
    # 读取原文得到的证据片段（只读原文入证据）

    search_hits: List[Evidence] = field(default_factory=list)
    # 搜索/精确匹配得到的候选片段（非证据）

    paragraphs: List[ParagraphRead] = field(default_factory=list)
    # 精确读取的段落原文

    chapters: Dict[int, ChapterRead] = field(default_factory=dict)
    # 读取的完整章节，key = chapter_order

    worldview: Dict[str, List[WorldviewItem]] = field(default_factory=dict)
    # 世界观条目，key = category

    # ========== 去重记录（仅用于判断是否重复调用）==========

    searched_queries: Set[str] = field(default_factory=set)
    # 已搜索过的 query

    evidence_keys: Set[str] = field(default_factory=set)
    # 证据去重指纹

    search_hit_keys: Set[str] = field(default_factory=set)
    # 搜索候选去重指纹

    skipped_evidences_strict: int = 0
    # 严格模式下无段落号的证据数（保留待补齐）

    read_paragraph_positions: Set[Tuple[int, int]] = field(default_factory=set)
    # 已读取的段落位置 (chapter_order, paragraph_index)

    read_chapter_orders: Set[int] = field(default_factory=set)
    # 已读取完整原文的章节序号

    read_worldview_categories: Set[str] = field(default_factory=set)
    # 已读取的世界观分类

    # ========== 轮次记录（给前端展示）==========

    rounds: List[ExploreRound] = field(default_factory=list)
    # 每轮的执行记录

    # ========== 去重方法 ==========

    def _is_query_similar(self, query: str, existing: str, threshold: float = 0.6) -> bool:
        """判断两个搜索词是否高度相似

        使用简单的包含关系和长度比较来判断：
        - 如果一个是另一个的子串，且长度差距不大，认为相似
        - 避免重复搜索如"器灵吞噬"和"器灵吞噬机制"

        阈值说明：
        - 0.6 可以匹配 "器灵吞噬"(4字) 和 "器灵吞噬机制"(6字): 4/6=0.67 >= 0.6
        - 0.6 不会误匹配 "器灵"(2字) 和 "器灵吞噬机制"(6字): 2/6=0.33 < 0.6
        """
        if not query or not existing:
            return False

        # 规范化：去除空格
        q = query.replace(" ", "")
        e = existing.replace(" ", "")

        # 完全相同
        if q == e:
            return True

        # 一个是另一个的子串
        if q in e or e in q:
            # 计算重叠比例
            shorter = min(len(q), len(e))
            longer = max(len(q), len(e))
            overlap_ratio = shorter / longer
            if overlap_ratio >= threshold:
                return True

        return False

    def should_search(self, query: str) -> bool:
        """判断是否应该执行搜索（包含相似度检查）"""
        if query in self.searched_queries:
            return False

        # 检查是否与已搜索的词高度相似
        for existing in self.searched_queries:
            if self._is_query_similar(query, existing):
                logger.info(
                    "[ExploreState] 搜索词与已有词相似，跳过: '%s' ~ '%s'",
                    query[:30], existing[:30]
                )
                return False

        return True

    def record_search(self, query: str):
        """记录已搜索的 query"""
        self.searched_queries.add(query)

    def should_read_paragraph(self, chapter_order: int, paragraph_index: int) -> bool:
        """判断是否应该读取段落"""
        position = (chapter_order, paragraph_index)
        if position not in self.read_paragraph_positions:
            return True
        for p in self.paragraphs:
            if p.chapter_order == chapter_order and p.paragraph_index == paragraph_index:
                return False
        return True

    def record_paragraph_read(self, chapter_order: int, paragraph_index: int):
        """记录已读取的段落"""
        self.read_paragraph_positions.add((chapter_order, paragraph_index))

    def should_read_chapter(self, chapter_order: int) -> bool:
        """判断是否应该读取章节"""
        if chapter_order not in self.read_chapter_orders:
            return True
        chapter = self.chapters.get(chapter_order)
        return not (chapter and chapter.content)

    def record_chapter_read(self, chapter_order: int):
        """记录已读取的章节"""
        self.read_chapter_orders.add(chapter_order)

    def should_read_worldview(self, category: str) -> bool:
        """判断是否应该读取世界观分类"""
        if category not in self.read_worldview_categories:
            return True
        return not self.worldview.get(category)

    def record_worldview_read(self, category: str):
        """记录已读取的世界观分类"""
        self.read_worldview_categories.add(category)

    # ========== 内容存储方法 ==========

    def _build_evidence_key(self, result: Dict, query: str) -> str:
        text = result.get("snippet", result.get("content", "")) or ""
        text = " ".join(str(text).split())
        chapter_order = result.get("chapter_order", 0)
        paragraph_index = result.get("paragraph_index")
        if isinstance(paragraph_index, str) and paragraph_index.isdigit():
            paragraph_index = int(paragraph_index)
        paragraph_key = "" if paragraph_index is None else str(paragraph_index)
        source_type = result.get("source", "")
        key_parts = [str(chapter_order), paragraph_key, source_type, text[:80]]
        if (not chapter_order and not paragraph_index) and query:
            key_parts.append(query[:30])
        return ":".join(key_parts)

    def add_search_hit(
        self,
        result: Dict,
        query: str,
        round_idx: int,
        chapter_scope_filter: Optional[Callable[[Optional[int]], bool]] = None
    ) -> bool:
        """添加搜索候选（不作为证据，仅用于定位/展示）"""
        chapter_order = result.get("chapter_order")
        if isinstance(chapter_order, str) and chapter_order.isdigit():
            chapter_order = int(chapter_order)
            result["chapter_order"] = chapter_order
        if chapter_scope_filter and not chapter_scope_filter(chapter_order):
            return False

        paragraph_index = result.get("paragraph_index")
        if isinstance(paragraph_index, str) and paragraph_index.isdigit():
            paragraph_index = int(paragraph_index)
            result["paragraph_index"] = paragraph_index

        hit_key = self._build_evidence_key(result, query)
        if hit_key in self.search_hit_keys:
            return False
        self.search_hit_keys.add(hit_key)

        chapter_id = result.get("chapter_id") or ""
        chapter_title = result.get("chapter_title") or ""
        node_id = result.get("node_id") or ""
        hit = Evidence(
            text=result.get("snippet", result.get("content", ""))[:500],
            chapter_order=result.get("chapter_order", 0),
            paragraph_index=paragraph_index,
            similarity=result.get("similarity", 0),
            source_type=result.get("source", "search"),
            query=query,
            round_idx=round_idx,
            chapter_id=chapter_id,
            chapter_title=chapter_title,
            node_id=node_id
        )
        self.search_hits.append(hit)
        return True

    def add_evidence(
        self,
        result: Dict,
        query: str,
        round_idx: int,
        require_paragraph_index: bool = False,
        chapter_scope_filter: Optional[Callable[[Optional[int]], bool]] = None
    ) -> bool:
        """添加搜索结果（去重 + 相似度过滤 + 章节范围过滤）

        Args:
            result: 搜索结果
            query: 搜索词
            round_idx: 轮次索引
            require_paragraph_index: 是否要求段落索引
            chapter_scope_filter: 章节范围过滤函数，返回 True 表示在范围内
        """
        # 章节范围检查
        chapter_order = result.get("chapter_order")
        if isinstance(chapter_order, str) and chapter_order.isdigit():
            chapter_order = int(chapter_order)
            result["chapter_order"] = chapter_order
        if chapter_scope_filter and not chapter_scope_filter(chapter_order):
            logger.debug(
                "[ExploreState] 证据超出章节范围，已过滤: chapter_order=%s",
                chapter_order
            )
            return False

        paragraph_index = result.get("paragraph_index")
        if isinstance(paragraph_index, str) and paragraph_index.isdigit():
            paragraph_index = int(paragraph_index)
            result["paragraph_index"] = paragraph_index
        source_type = result.get("source", "")
        if source_type not in ("paragraph", "read_paragraph"):
            return False
        if require_paragraph_index:
            if paragraph_index is None:
                text_preview = result.get("snippet", result.get("content", "")) or ""
                logger.info(
                    "[ContentExplorer] 严格段落号模式发现无段落号证据: query=%s, preview=%s",
                    query,
                    _truncate_text(text_preview, 80)
                )
                self.skipped_evidences_strict += 1
                return False
        similarity = result.get("similarity")
        if isinstance(similarity, (int, float)) and 0 < similarity <= 1:
            if similarity < MIN_EVIDENCE_SIMILARITY:
                return False

        evidence_key = self._build_evidence_key(result, query)
        if evidence_key in self.evidence_keys:
            return False
        self.evidence_keys.add(evidence_key)

        chapter_id = result.get("chapter_id") or ""
        chapter_title = result.get("chapter_title") or ""
        node_id = result.get("node_id") or ""
        evidence = Evidence(
            # 🔧 2026-01-21: 增加单条证据文本长度 200→500，保留更多上下文
            text=result.get("snippet", result.get("content", ""))[:500],
            chapter_order=result.get("chapter_order", 0),
            paragraph_index=paragraph_index,
            similarity=result.get("similarity", 0),
            source_type=source_type or "hybrid",
            query=query,
            round_idx=round_idx,
            chapter_id=chapter_id,
            chapter_title=chapter_title,
            node_id=node_id
        )
        self.evidences.append(evidence)
        return True

    def add_paragraph(self, data: Dict, round_idx: int):
        """添加段落原文"""
        paragraph_read = ParagraphRead(
            chapter_order=data.get("chapter_order", 0),
            chapter_title=data.get("chapter_title", ""),
            paragraph_index=data.get("paragraph_index", 0),
            text=data.get("text", ""),
            context_before=data.get("context_before", []),
            context_after=data.get("context_after", []),
            round_idx=round_idx,
            node_id=data.get("node_id", "") or ""
        )
        self.paragraphs.append(paragraph_read)

    def add_chapter(self, chapter: Dict, round_idx: int):
        """添加章节原文（覆盖式，同一章节只保留一份）"""
        order = chapter.get("order", chapter.get("chapter_order", 0))
        raw_id = chapter.get("id") or chapter.get("chapter_id") or ""
        chapter_id = str(raw_id) if raw_id else ""
        self.chapters[order] = ChapterRead(
            id=chapter_id,  # 2026-01-18: 添加章节ID
            order=order,
            title=chapter.get("title", chapter.get("chapter_title", "")),
            content=chapter.get("content", ""),
            word_count=len(chapter.get("content", "")),
            round_idx=round_idx
        )

    def add_worldview_items(self, items: List[Dict], category: str):
        """添加世界观条目"""
        if category not in self.worldview:
            self.worldview[category] = []
        for item in items:
            self.worldview[category].append(WorldviewItem(
                id=item.get("id", ""),
                name=item.get("name", ""),
                category=category,
                description=item.get("description", ""),
                attributes=item.get("attributes", {})
            ))

    # ========== 统计和收敛 ==========

    def check_convergence(self, window: int = 2) -> bool:
        """
        检测是否收敛（连续 N 轮没有新增信息）
        """
        if len(self.rounds) < window:
            return False

        recent_rounds = self.rounds[-window:]
        for round_data in recent_rounds:
            if round_data.new_evidences_count > 0 or round_data.new_paragraphs_count > 0:
                return False

        return True

    def get_stats(self) -> Dict[str, Any]:
        """获取当前状态统计"""
        return {
            "total_evidences": len(self.evidences),
            "total_paragraphs": len(self.paragraphs),
            "total_chapters": len(self.chapters),
            "total_worldview_items": sum(len(items) for items in self.worldview.values()),
            "searched_queries_count": len(self.searched_queries),
            "rounds_count": len(self.rounds)
        }


# ==================== 输出结果 ====================

@dataclass
class ExploreResult:
    """Explore 工具的最终输出"""

    # 原文内容
    evidences: List[Evidence]
    search_hits: List[Evidence]
    paragraphs: List[ParagraphRead]
    chapters: Dict[int, ChapterRead]
    worldview: Dict[str, List[WorldviewItem]]

    # AI 分析
    analysis: str

    # 统计信息
    stats: Dict[str, Any]

    # 轨迹信息
    rounds: List[ExploreRound]
    stop_reason: str
    total_duration_ms: int


# ==================== 辅助函数 ====================

def _get_round_title(round_idx: int) -> str:
    """生成轮次标题"""
    titles = {
        1: "初次检索与定位",
        2: "补漏检索与二次定位",
        3: "交叉验证与收敛",
    }
    return titles.get(round_idx, f"深度探索（第{round_idx}轮）")


def _get_review_status(round_data: ExploreRound) -> str:
    """获取审查状态"""
    return "停止" if round_data.sufficient else "继续检索"


def _get_status_text(round_data: ExploreRound) -> str:
    """获取状态文本（灰色显示）"""
    return "停止检索" if round_data.sufficient else ""


def _scopes_cache_key(scopes: List[Tuple[int, int]]) -> str:
    if not scopes:
        return "all"
    return ",".join(f"{start}-{end}" for start, end in scopes)


def _build_explore_shared_key(
    work_id: str,
    user_id: Optional[str],
    conversation_id: Optional[str],
    chapter_scopes: List[Tuple[int, int]]
) -> str:
    work_id = str(work_id or "").strip()
    if not work_id:
        return ""
    user_part = str(user_id or "anonymous").strip() or "anonymous"
    convo_part = str(conversation_id or "default").strip() or "default"
    scope_part = _scopes_cache_key(chapter_scopes)
    return f"{work_id}:{user_part}:{convo_part}:{scope_part}"


def _clone_explore_state(state: ExploreState) -> ExploreState:
    return ExploreState(
        evidences=[],
        search_hits=[],
        paragraphs=[],
        chapters={},
        worldview={},
        searched_queries=set(state.searched_queries),
        evidence_keys=set(),
        search_hit_keys=set(),
        skipped_evidences_strict=0,
        read_paragraph_positions=set(state.read_paragraph_positions),
        read_chapter_orders=set(state.read_chapter_orders),
        read_worldview_categories=set(),
        rounds=[],
    )


def _merge_explore_states(base: ExploreState, incoming: ExploreState) -> ExploreState:
    merged = _clone_explore_state(base)
    merged.searched_queries |= incoming.searched_queries
    merged.read_paragraph_positions |= incoming.read_paragraph_positions
    merged.read_chapter_orders |= incoming.read_chapter_orders
    return merged

def build_context_for_task(result: ExploreResult) -> str:
    """
    将 ExploreResult 转换为后续任务可用的上下文字符串

    注意：原文内容原样传递，不压缩
    """
    sections = []

    # 1. 世界观设定
    if result.worldview:
        sections.append("## 世界观设定\n")
        for category, items in result.worldview.items():
            sections.append(f"### {category}\n")
            for item in items:
                sections.append(f"- **{item.name}**: {item.description}\n")
                if item.attributes:
                    for key, value in item.attributes.items():
                        sections.append(f"  - {key}: {value}\n")

    # 2. 章节原文
    if result.chapters:
        sections.append("\n## 已读取的章节原文\n")
        for order, chapter in sorted(result.chapters.items()):
            sections.append(f"### 第{chapter.order}章：{chapter.title}\n")
            sections.append(f"{chapter.content}\n")

    # 3. 精确读取的段落（如果没有读取整章）
    if result.paragraphs:
        read_chapter_orders = set(result.chapters.keys())
        paragraphs_to_show = [
            p for p in result.paragraphs
            if p.chapter_order not in read_chapter_orders
        ]
        if paragraphs_to_show:
            sections.append("\n## 精确读取的段落\n")
            for p in paragraphs_to_show:
                sections.append(f"### 第{p.chapter_order}章《{p.chapter_title}》第{p.paragraph_index}段\n")
                if p.context_before:
                    sections.append("【前文】\n" + "\n".join(p.context_before) + "\n")
                sections.append(f"【目标段落】\n{p.text}\n")
                if p.context_after:
                    sections.append("【后文】\n" + "\n".join(p.context_after) + "\n")

    # 4. 搜索证据（作为补充）
    if result.evidences:
        shown_positions = set()
        for p in result.paragraphs:
            shown_positions.add((p.chapter_order, p.paragraph_index))

        evidences_to_show = [
            e for e in result.evidences
            if (e.chapter_order, e.paragraph_index) not in shown_positions
        ]

        if evidences_to_show:
            sections.append("\n## 相关片段\n")
            # 🔧 2026-01-21: 移除条数限制，由 context_builder.py 的 20000 字符上限控制
            for e in evidences_to_show:
                para_label = f"{e.paragraph_index}段" if isinstance(e.paragraph_index, int) else "段落未知"
                sections.append(f"- [{e.chapter_order}章{para_label}] {e.text}\n")

    # 5. AI 分析
    if result.analysis:
        sections.append(f"\n## AI 分析\n{result.analysis}\n")

    return "".join(sections)


def _build_explore_summary(result: ExploreResult) -> str:
    """
    构建探索结果摘要，供后续工具（如 analyze_content）使用

    这个摘要包含所有收集到的关键信息，格式化为易于分析的文本
    """
    summary_parts = []

    # 1. 统计信息
    stats = result.stats
    summary_parts.append(f"【探索统计】")
    summary_parts.append(f"- 探索轮次: {stats.get('rounds_count', 0)} 轮")
    summary_parts.append(f"- 收集证据: {stats.get('total_evidences', 0)} 条")

    # 🔧 2026-01-21: 修改统计展示，避免"读取章节: 0 章"误导AI
    # 显示证据覆盖的章节范围，而不是整章阅读的数量
    if result.evidences:
        chapter_orders = sorted(set(e.chapter_order for e in result.evidences if e.chapter_order))
        if chapter_orders:
            min_ch, max_ch = min(chapter_orders), max(chapter_orders)
            summary_parts.append(f"- 证据覆盖: 第{min_ch}-{max_ch}章 ({len(chapter_orders)}个章节)")
        else:
            summary_parts.append(f"- 证据覆盖: 未知")
    elif stats.get('total_chapters', 0) > 0:
        summary_parts.append(f"- 整章阅读: {stats.get('total_chapters', 0)} 章")

    summary_parts.append(f"- 世界观条目: {stats.get('total_worldview_items', 0)} 个")
    summary_parts.append(f"- 结束原因: {result.stop_reason}")
    summary_parts.append("")

    # 2. 世界观设定
    if result.worldview:
        summary_parts.append("【世界观设定】")
        for category, items in result.worldview.items():
            for item in items[:5]:  # 每类最多 5 个
                summary_parts.append(f"- {item.name}: {item.description[:100]}...")
        summary_parts.append("")

    # 3. 章节内容摘要
    if result.chapters:
        summary_parts.append("【章节内容】")
        for order, chapter in sorted(result.chapters.items()):
            content_preview = chapter.content[:500] if chapter.content else ""
            summary_parts.append(f"第{chapter.order}章《{chapter.title}》:")
            summary_parts.append(f"  {content_preview}...")
        summary_parts.append("")

    # 4. 证据片段
    if result.evidences:
        summary_parts.append("【相关证据片段】")
        # 按章节分组
        by_chapter = {}
        for e in result.evidences:
            key = e.chapter_order
            if key not in by_chapter:
                by_chapter[key] = []
            by_chapter[key].append(e)

        for chapter_order in sorted(by_chapter.keys()):
            evidences = by_chapter[chapter_order]
            summary_parts.append(f"第{chapter_order}章:")
            # 🔧 2026-01-21: 增加每章证据数量限制 3→10，配合 context_builder 的 20000 字符上限
            for e in evidences[:10]:
                # 🔧 2026-01-21: 增加证据文本预览长度 200→400，与存储层保持一致
                text_preview = e.text[:400] + "..." if len(e.text) > 400 else e.text
                para_label = f"{e.paragraph_index}段" if isinstance(e.paragraph_index, int) else "段落未知"
                summary_parts.append(f"  - [{para_label}] {text_preview}")
        summary_parts.append("")

    # 5. AI 分析
    if result.analysis:
        summary_parts.append("【AI 分析】")
        summary_parts.append(result.analysis)

    return "\n".join(summary_parts)


def _build_search_results(
    result: ExploreResult,
    limit: int = 10,
    node_id_map: Optional[Dict[Tuple[int, int], str]] = None
) -> List[Dict[str, Any]]:
    """构建兼容 frontend_display.search_results 的精简列表"""
    results: List[Dict[str, Any]] = []
    seen = set()
    if node_id_map is None:
        node_id_map = _build_node_id_map(result)
    candidates = result.search_hits if getattr(result, "search_hits", None) else result.evidences
    candidates = sorted(candidates, key=lambda e: e.similarity or 0, reverse=True)
    for e in candidates:
        text = _truncate_text(e.text or "", 400)
        if not text:
            continue
        key = (e.chapter_order, e.paragraph_index, text[:80])
        if key in seen:
            continue
        seen.add(key)
        results.append({
            "chapter_id": e.chapter_id or "",
            "chapter_order": e.chapter_order,
            "chapter_title": e.chapter_title or "",
            "paragraph_index": e.paragraph_index,
            "node_id": node_id_map.get((e.chapter_order, e.paragraph_index), ""),
            "text": text,
            "paragraphs": [
                {
                    "text": text,
                    "paragraph_index": e.paragraph_index
                }
            ],
            "similarity": e.similarity,
            "source": e.source_type,
            "round_idx": e.round_idx,
        })
        if len(results) >= limit:
            break
    return results


def _build_node_id_map(result: ExploreResult) -> Dict[Tuple[int, int], str]:
    """构建 (chapter_order, paragraph_index) -> node_id 映射"""
    node_id_map: Dict[Tuple[int, int], str] = {}

    for p in result.paragraphs:
        if isinstance(p.chapter_order, int) and isinstance(p.paragraph_index, int) and p.node_id:
            node_id_map[(p.chapter_order, p.paragraph_index)] = p.node_id

    for e in result.evidences:
        if isinstance(e.chapter_order, int) and isinstance(e.paragraph_index, int) and e.node_id:
            node_id_map.setdefault((e.chapter_order, e.paragraph_index), e.node_id)

    if getattr(result, "search_hits", None):
        for h in result.search_hits:
            if isinstance(h.chapter_order, int) and isinstance(h.paragraph_index, int) and h.node_id:
                node_id_map.setdefault((h.chapter_order, h.paragraph_index), h.node_id)

    for order, ch in result.chapters.items():
        if not ch.content:
            continue
        try:
            from app.services.agent.tools.locate_tools import _split_paragraphs
            parsed = _split_paragraphs(ch.content)
            for para in parsed:
                idx = para.get("index")
                node_id = para.get("node_id")
                if isinstance(idx, int) and node_id:
                    node_id_map.setdefault((order, idx), node_id)
        except Exception:
            continue

    return node_id_map


def _build_locate_targets(
    result: ExploreResult,
    chapters_by_order: Dict[int, Dict[str, Any]],
    node_id_map: Optional[Dict[Tuple[int, int], str]] = None,
    candidates: Optional[List[Evidence]] = None
) -> List[Dict[str, Any]]:
    """构建 locate_content 需要的明确定位目标"""
    targets: List[Dict[str, Any]] = []
    seen = set()
    if node_id_map is None:
        node_id_map = _build_node_id_map(result)

    def _add_target(
        chapter_order: int,
        paragraph_index: Optional[int],
        chapter_id: str,
        query: str,
        reason: str,
        node_id: str = ""
    ) -> None:
        query_text = (query or "").strip()
        if not query_text or not chapter_id:
            return
        query_text = query_text[:200]
        key = (chapter_id, paragraph_index, query_text[:80])
        if key in seen:
            return
        seen.add(key)
        targets.append({
            "chapter_id": chapter_id,
            "query": query_text,
            "paragraph_index": paragraph_index,
            "node_id": node_id or "",
            "reason": reason,
            "allow_global_fallback": False
        })

    # 优先使用已读取段落（原文）
    for p in result.paragraphs:
        chapter_id = ""
        entry = chapters_by_order.get(p.chapter_order, {})
        if entry:
            chapter_id = entry.get("id") or entry.get("chapter_id") or ""
        _add_target(
            chapter_order=p.chapter_order,
            paragraph_index=p.paragraph_index,
            chapter_id=chapter_id,
            query=p.text,
            reason="已读取原文段落",
            node_id=p.node_id or node_id_map.get((p.chapter_order, p.paragraph_index), "")
        )

    # 兜底：用证据片段生成定位目标
    fallback_items = candidates
    if fallback_items is None:
        fallback_items = result.search_hits if getattr(result, "search_hits", None) else result.evidences
    for e in fallback_items:
        chapter_id = e.chapter_id or ""
        if not chapter_id:
            entry = chapters_by_order.get(e.chapter_order, {})
            chapter_id = entry.get("id") or entry.get("chapter_id") or ""
        _add_target(
            chapter_order=e.chapter_order,
            paragraph_index=e.paragraph_index,
            chapter_id=chapter_id,
            query=e.text,
            reason="检索片段需定位",
            node_id=node_id_map.get((e.chapter_order, e.paragraph_index), "")
        )

    return targets


def _build_evidences_output(
    result: ExploreResult,
    node_id_map: Optional[Dict[Tuple[int, int], str]] = None
) -> List[Dict[str, Any]]:
    """构建对外输出的证据列表（含定位元数据）"""
    if node_id_map is None:
        node_id_map = _build_node_id_map(result)
    items: List[Dict[str, Any]] = []
    for e in result.evidences:
        items.append({
            "text": e.text,
            "chapter_id": e.chapter_id,
            "chapter_order": e.chapter_order,
            "chapter_title": e.chapter_title,
            "paragraph_index": e.paragraph_index,
            "node_id": node_id_map.get((e.chapter_order, e.paragraph_index), ""),
            "source": e.source_type,
            "query": e.query,
            "round_idx": e.round_idx
        })
    return items


def _build_chapter_paragraphs(
    result: ExploreResult,
    chapter_order: int,
    chapter_content: str,
    limit: int = 3
) -> List[Dict[str, Any]]:
    """为 chapters 输出补齐可用段落（优先已读段落，其次章节原文，再次证据片段）"""
    paragraphs: List[Dict[str, Any]] = []
    seen = set()
    node_id_by_index: Dict[int, str] = {}
    parsed_chapter = None

    if chapter_content:
        try:
            from app.services.agent.tools.locate_tools import _split_paragraphs
            parsed_chapter = _split_paragraphs(chapter_content)
            for para in parsed_chapter:
                idx = para.get("index")
                node_id = para.get("node_id")
                if isinstance(idx, int) and node_id:
                    node_id_by_index[idx] = node_id
        except Exception:
            parsed_chapter = None

    for p in result.paragraphs:
        if p.chapter_order != chapter_order:
            continue
        text = (p.text or "").strip()
        if not text:
            continue
        key = (p.paragraph_index, text[:80])
        if key in seen:
            continue
        seen.add(key)
        paragraphs.append({
            "text": text,
            "paragraph_index": p.paragraph_index,
            "node_id": p.node_id or node_id_by_index.get(p.paragraph_index)
        })

    if paragraphs:
        return paragraphs[:limit]

    if parsed_chapter:
        for para in parsed_chapter[:limit]:
            text = (para.get("text") or "").strip()
            if not text:
                continue
            key = (para.get("index"), text[:80])
            if key in seen:
                continue
            seen.add(key)
            paragraphs.append({
                "text": text,
                "paragraph_index": para.get("index"),
                "node_id": para.get("node_id")
            })

    if paragraphs:
        return paragraphs[:limit]

    evidences = [
        e for e in result.evidences
        if e.chapter_order == chapter_order and e.text
    ]
    evidences.sort(key=lambda e: e.similarity or 0, reverse=True)
    for e in evidences:
        text = (e.text or "").strip()
        if not text:
            continue
        key = (e.paragraph_index, text[:80])
        if key in seen:
            continue
        seen.add(key)
        paragraphs.append({
            "text": text,
            "paragraph_index": e.paragraph_index
        })
        if len(paragraphs) >= limit:
            break

    return paragraphs


def to_frontend_display(result: ExploreResult) -> Dict[str, Any]:
    """转换为前端展示格式（V2 完整版）"""
    last_round = result.rounds[-1] if result.rounds else None
    return {
        "rounds": [
            {
                "round_idx": r.round_idx,
                "title": r.title,
                "reason": r.reason,  # AI 生成的决策理由（完整）
                "tool_calls": _format_tool_calls_for_frontend(r),
                "hit_count": r.new_evidences_count,
                "missing_items": r.missing_items,
                "status_text": _get_status_text(r),
                "evidences": [
                    {
                        "chapter": e.chapter_order,
                        "paragraph": e.paragraph_index,
                        "text": e.text[:100] + "..." if len(e.text) > 100 else e.text
                    }
                    for e in result.evidences if e.round_idx == r.round_idx
                ][:5],  # 每轮最多显示5条
                "review_status": _get_review_status(r),
                "status": "done"
            }
            for r in result.rounds
        ],
        "ai_analysis": {
            "summary": result.analysis,
            "next_action": "基于这些背景信息，我将执行续写，重点描写收集到的关键情节要素。",
            "next_tool": "",  # 空字符串，前端不显示
            "stats": {
                "worldview": sum(len(items) for items in result.worldview.values()),
                "chapters": _format_chapters_range(result.chapters),
                "evidences": len(result.evidences),
            }
        },
        "step_description": "多轮检索-定位-原文读取，由 LLM 自检驱动继续收集，最终输出完整证据链。",
        "tool_operation": {
            "icon": "Scan",
            "name": f"explore_content (max_rounds: {len(result.rounds)})"
        },
        "status": "completed",
        "stop_reason": result.stop_reason,
        "duration_ms": result.total_duration_ms
    }


def _format_tool_calls_for_frontend(round_data: ExploreRound) -> List[Dict[str, Any]]:
    """格式化工具调用为前端标签格式"""
    tags = []

    for tc in round_data.tool_calls:
        if tc.tool_name == "search_content":
            query = tc.params.get("query", "")
            tags.append({
                "type": "Search",
                "value": query,
                "highlight": query
            })
        elif tc.tool_name == "locate_content":
            chapter_order = tc.params.get("chapter_order")
            chapter_title = ""
            chapter_id = ""
            if isinstance(tc.result, dict):
                chapter_title = tc.result.get("chapter_title") or ""
                chapter_id = tc.result.get("chapter_id") or ""
                if not chapter_order:
                    chapter_order = tc.result.get("chapter_order")
            if isinstance(chapter_order, str) and chapter_order.isdigit():
                chapter_order = int(chapter_order)
            if isinstance(chapter_order, int):
                chapter_label = f"第{chapter_order}章"
            elif chapter_title:
                chapter_label = f"《{chapter_title}》"
            else:
                chapter_label = "章节未知"
            para = tc.result.get("paragraph_index") if isinstance(tc.result, dict) else None
            if isinstance(para, str) and para.isdigit():
                para = int(para)
            para_label = f"第{para}段" if isinstance(para, int) else "段落未知"
            tags.append({
                "type": "Locate",
                "value": f"{chapter_label} · {para_label}"
            })
        elif tc.tool_name == "read_paragraph":
            # 段落读取：显示章节和段落号
            chapter = tc.params.get("chapter_order", "?")
            para = tc.params.get("paragraph_index", "?")
            tags.append({
                "type": "ReadParagraph",
                "value": f"第{chapter}章 · 第{para}段"
            })
        elif tc.tool_name == "get_chapter_by_order_tool":
            # 整章阅读：仅在未禁止时使用
            chapter = tc.params.get("chapter_order", "?")
            tags.append({
                "type": "ReadRaw",
                "value": f"第{chapter}章"
            })
        elif tc.tool_name == "get_writing_context":
            # get_writing_context 工具：根据参数区分用途
            if tc.params.get("chapter_orders"):
                # 整章阅读
                chapter = tc.params.get("chapter_orders", "?")
                tags.append({
                    "type": "ReadRaw",
                    "value": f"第{chapter}章"
                })
            elif tc.params.get("include") == "worldview":
                # 世界观读取（不显示，或显示为 Worldview）
                tags.append({
                    "type": "Worldview",
                    "value": "世界观设定"
                })

    # 添加 Review 标签
    tags.append({
        "type": "Review",
        "value": _get_review_status(round_data)
    })

    return tags


def _format_chapters_range(chapters: Dict[int, ChapterRead]) -> str:
    """格式化章节范围"""
    if not chapters:
        return "-"
    orders = sorted(chapters.keys())
    if len(orders) == 1:
        return str(orders[0])
    return f"{orders[0]}-{orders[-1]}"


def _format_scope_ranges(scopes: List[Tuple[int, int]]) -> str:
    if not scopes:
        return "-"
    parts = []
    for start, end in scopes:
        if start == end:
            parts.append(f"第{start}章")
        else:
            parts.append(f"第{start}-{end}章")
    return "、".join(parts)


# ==================== ContentExplorer 核心类 ====================

class ContentExplorer:
    """内容探索器（AI 驱动版本）"""

    MAX_ROUNDS = 10  # 安全上限，防止死循环

    def __init__(
        self,
        work_id: str,
        target_task: str,
        max_rounds: int = 10,
        emit_callback: Optional[Callable[[dict], Awaitable[None]]] = None,
        step_id: Optional[int] = None,
        search_keywords: Optional[List[str]] = None,
        explore_mode: str = "pipeline",
        max_tool_calls: Optional[int] = None,
        max_read_paragraphs: Optional[int] = None
    ):
        """
        初始化内容探索器

        Args:
            work_id: 作品ID
            target_task: 目标任务描述
            max_rounds: 最大探索轮次（安全上限，AI 会自主决定何时停止）
            emit_callback: 事件发射回调
            step_id: 步骤ID
            search_keywords: 搜索关键词列表（由规划阶段直接提供，优先使用）
        """
        self.work_id = work_id
        self.target_task = target_task
        self.search_keywords = search_keywords  # 规划阶段传入的关键词
        self.chapter_scopes_raw = _parse_chapter_scopes(target_task)
        self.chapter_scopes = list(self.chapter_scopes_raw)
        self.scope_chapter_id: Optional[str] = None
        self.scope_look_ahead = 0
        self.scope_resolution_attempted = False
        self.scope_title_mapped = False
        self.title_order_map: Dict[int, int] = {}
        self.scope_search_contexts: Optional[List[Tuple[str, int]]] = None
        self.forbid_full_chapter = _forbid_full_chapter(target_task)
        self.require_full_chapter = _requires_full_chapter(target_task)
        self.require_paragraph_index = _requires_paragraph_index(target_task)
        self.max_rounds = min(max_rounds, self.MAX_ROUNDS)
        self.explore_mode = (explore_mode or "pipeline").strip().lower()
        self.max_tool_calls = max_tool_calls if isinstance(max_tool_calls, int) and max_tool_calls > 0 else TOOL_LOOP_MAX_CALLS_DEFAULT
        self.max_read_paragraphs = (
            max_read_paragraphs if isinstance(max_read_paragraphs, int) and max_read_paragraphs > 0 else TOOL_LOOP_MAX_READS_DEFAULT
        )
        self.emit_callback = emit_callback
        if isinstance(step_id, int) and step_id > 0:
            self.step_id = step_id
        else:
            self.step_id = 1
        self.state = ExploreState()
        self.start_time = get_utc_now()
        self.chapter_list_cache: Optional[List[Dict[str, Any]]] = None
        if self.require_paragraph_index:
            logger.info("[ContentExplorer] 启用严格段落号模式")
        if self.chapter_scopes_raw:
            logger.info("[ContentExplorer] 章节范围锁定: %s", _format_scope_ranges(self.chapter_scopes_raw))
        if self.require_full_chapter:
            logger.info("[ContentExplorer] 任务要求完整章节原文")
        if self.forbid_full_chapter:
            logger.info("[ContentExplorer] 任务禁止整章阅读")

    async def _ensure_scope_mapping(self) -> None:
        if not self.chapter_scopes_raw or self.scope_title_mapped:
            return
        self.scope_title_mapped = True
        try:
            async with AsyncSessionLocal() as db:
                from app.services.chapter_service import ChapterService
                chapter_svc = ChapterService(db)
                chapters = await chapter_svc.get_chapters_by_work(self.work_id)
            title_order_map: Dict[int, int] = {}
            self.chapter_list_cache = []
            for chapter in chapters:
                self.chapter_list_cache.append({
                    "chapter_id": str(chapter.id) if chapter.id else "",
                    "id": str(chapter.id) if chapter.id else "",
                    "order": chapter.order,
                    "title": chapter.title or "",
                    "word_count": getattr(chapter, "word_count", 0) or 0
                })
                title_no = _extract_title_chapter_number(chapter.title or "")
                if not isinstance(title_no, int):
                    continue
                if title_no not in title_order_map:
                    title_order_map[title_no] = chapter.order
            self.title_order_map = title_order_map
            total_chapters = len(chapters) if chapters else 0
            mapped = _map_scopes_to_orders(self.chapter_scopes_raw, title_order_map, total_chapters)
            if mapped:
                self.chapter_scopes = mapped
                logger.info(
                    "[ContentExplorer] 章节范围映射: %s -> %s",
                    _format_scope_ranges(self.chapter_scopes_raw),
                    _format_scope_ranges(self.chapter_scopes)
                )
            else:
                logger.warning(
                    "[ContentExplorer] 章节范围映射为空，保持原始范围: %s",
                    _format_scope_ranges(self.chapter_scopes_raw)
                )
        except Exception as e:
            logger.warning(f"[ContentExplorer] 章节范围映射异常: {e}")
            self.title_order_map = {}
            self.chapter_list_cache = None

    async def _get_chapter_list(self) -> List[Dict[str, Any]]:
        if self.chapter_list_cache is not None:
            return self.chapter_list_cache
        try:
            async with AsyncSessionLocal() as db:
                from app.services.chapter_service import ChapterService
                chapter_svc = ChapterService(db)
                chapters = await chapter_svc.get_chapters_by_work(self.work_id)
            self.chapter_list_cache = []
            for chapter in chapters or []:
                self.chapter_list_cache.append({
                    "chapter_id": str(chapter.id) if chapter.id else "",
                    "id": str(chapter.id) if chapter.id else "",
                    "order": chapter.order,
                    "title": chapter.title or "",
                    "word_count": getattr(chapter, "word_count", 0) or 0
                })
            self.chapter_list_cache.sort(key=lambda x: x.get("order") or 0)
            return self.chapter_list_cache
        except Exception as e:
            logger.warning(f"[ContentExplorer] 读取章节清单失败: {e}")
            self.chapter_list_cache = []
            return self.chapter_list_cache

    async def _get_chapter_info_by_order(self, chapter_order: int) -> Dict[str, Any]:
        chapters = await self._get_chapter_list()
        for ch in chapters:
            if ch.get("order") == chapter_order:
                return ch
        return {}

    async def _get_allowed_chapter_orders(self) -> List[int]:
        await self._ensure_scope_mapping()
        chapters = await self._get_chapter_list()
        orders = [ch.get("order") for ch in chapters if isinstance(ch.get("order"), int)]
        if self.chapter_scopes:
            orders = [order for order in orders if self._is_chapter_in_scope(order)]
        return orders

    async def _ensure_scope_context(self) -> Tuple[str, int]:
        await self._ensure_scope_mapping()
        if not self.chapter_scopes:
            return "", 0
        if self.scope_resolution_attempted:
            return self.scope_chapter_id or "", self.scope_look_ahead
        self.scope_resolution_attempted = True
        if len(self.chapter_scopes) != 1:
            logger.info("[ContentExplorer] 多段章节范围，跳过单范围定位优化")
            return "", 0
        start, end = self.chapter_scopes[0]
        try:
            from app.services.agent.langgraph_tools import resolve_chapter_id
            chapter_id, error_json = await resolve_chapter_id(self.work_id, str(start))
            if error_json:
                logger.warning(f"[ContentExplorer] 章节范围解析失败: {error_json}")
            else:
                self.scope_chapter_id = chapter_id
                self.scope_look_ahead = max(0, end - start)
        except Exception as e:
            logger.warning(f"[ContentExplorer] 章节范围解析异常: {e}")
        return self.scope_chapter_id or "", self.scope_look_ahead

    async def _get_scope_search_contexts(self) -> List[Tuple[str, int]]:
        if self.scope_search_contexts is not None:
            return self.scope_search_contexts
        self.scope_search_contexts = []
        await self._ensure_scope_mapping()
        if not self.chapter_scopes:
            return self.scope_search_contexts

        from app.services.agent.langgraph_tools import resolve_chapter_id

        for start, end in self.chapter_scopes:
            start_order = self._map_title_order_if_needed(start)
            end_order = self._map_title_order_if_needed(end)
            if not isinstance(start_order, int) or not isinstance(end_order, int):
                continue
            if start_order > end_order:
                start_order, end_order = end_order, start_order
            try:
                chapter_id, error_json = await resolve_chapter_id(self.work_id, str(start_order))
                if error_json or not chapter_id:
                    logger.warning(f"[ContentExplorer] 章节范围解析失败: {error_json}")
                    continue
                look_ahead = max(0, end_order - start_order)
                self.scope_search_contexts.append((chapter_id, look_ahead))
            except Exception as e:
                logger.warning(f"[ContentExplorer] 章节范围解析异常: {e}")
        return self.scope_search_contexts

    def _is_chapter_in_raw_scope(self, chapter_order: Optional[int]) -> bool:
        if not self.chapter_scopes_raw:
            return True
        if not isinstance(chapter_order, int):
            return False
        for start, end in self.chapter_scopes_raw:
            if start <= chapter_order <= end:
                return True
        return False

    def _map_title_order_if_needed(self, chapter_order: int) -> int:
        if not self.title_order_map or not self.chapter_scopes_raw:
            return chapter_order
        if not self._is_chapter_in_raw_scope(chapter_order):
            return chapter_order
        mapped = self.title_order_map.get(chapter_order)
        if isinstance(mapped, int):
            return mapped
        return chapter_order

    def _is_chapter_in_scope(self, chapter_order: Optional[int]) -> bool:
        if not self.chapter_scopes:
            return True
        if not isinstance(chapter_order, int):
            return False
        for start, end in self.chapter_scopes:
            if start <= chapter_order <= end:
                return True
        return False

    def _filter_results_in_scope(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not self.chapter_scopes:
            return results
        filtered = []
        for item in results:
            if not isinstance(item, dict):
                continue
            chapter_order = item.get("chapter_order")
            if isinstance(chapter_order, str) and chapter_order.isdigit():
                chapter_order = int(chapter_order)
                item["chapter_order"] = chapter_order
            if self._is_chapter_in_scope(chapter_order):
                filtered.append(item)
        return filtered

    def _filter_unreachable_missing(self, missing: List[str]) -> Tuple[List[str], List[str]]:
        if not missing:
            return [], []
        reachable = []
        unreachable = []
        for item in missing:
            text = str(item)
            if any(keyword in text for keyword in UNREACHABLE_MISSING_KEYWORDS):
                unreachable.append(text)
            else:
                reachable.append(text)
        return reachable, unreachable

    def _chapter_has_paragraph_evidence(self, chapter_order: int) -> bool:
        for p in self.state.paragraphs:
            if p.chapter_order == chapter_order:
                return True
        for e in self.state.evidences:
            if e.chapter_order == chapter_order and e.paragraph_index is not None:
                return True
        return False

    def _rank_chapters_by_evidence(self, chapter_orders: List[int]) -> List[int]:
        if not chapter_orders:
            return []
        scores = {order: 0.0 for order in chapter_orders}
        for e in self.state.evidences:
            order = e.chapter_order
            if order not in scores:
                continue
            similarity = e.similarity if isinstance(e.similarity, (int, float)) else 0.0
            scores[order] += 1.0 + max(similarity, 0.0)
            if e.paragraph_index is not None:
                scores[order] += 0.5
        return sorted(chapter_orders, key=lambda order: (-scores.get(order, 0.0), order))

    def _filter_chapters_for_reading(self, chapter_orders: List[int], limit: int) -> List[int]:
        if self.forbid_full_chapter:
            return []
        ranked = self._rank_chapters_by_evidence(chapter_orders)
        if self.require_full_chapter:
            return ranked[:limit]
        filtered = [order for order in ranked if not self._chapter_has_paragraph_evidence(order)]
        return filtered[:1]

    # ==================== 阶段1：精确搜索（Explore V2）====================

    async def _execute_exact_search_phase(self) -> bool:
        """
        执行精确搜索阶段（确定性，一次完成）

        Returns:
            bool: 是否成功获取到结果
        """
        from app.services.chapter_vector_service import ChapterVectorService
        from app.services.agent.langgraph_tools import read_paragraph

        logger.info("[ContentExplorer] ========== 阶段1：精确搜索 ==========")

        # 1. 仅使用规划阶段传入的关键词（外部驱动）
        if not self.search_keywords:
            logger.info("[ContentExplorer] 未提供 search_keywords，跳过精确搜索")
            return False
        keywords = [kw for kw in self.search_keywords if isinstance(kw, str) and kw.strip()]
        if not keywords:
            logger.info("[ContentExplorer] search_keywords 为空，跳过精确搜索")
            return False
        logger.info(f"[ContentExplorer] 使用规划传入的关键词: {keywords[:10]}")

        # 2. 确定章节范围
        chapter_range = None
        if self.chapter_scopes:
            # 取所有范围的最小和最大
            min_order = min(s[0] for s in self.chapter_scopes)
            max_order = max(s[1] for s in self.chapter_scopes)
            chapter_range = (min_order, max_order)
            logger.info(f"[ContentExplorer] 章节范围: {chapter_range}")

        # 3. 执行精确搜索
        try:
            async with AsyncSessionLocal() as db:
                vector_service = ChapterVectorService(db)
                results = await vector_service.exact_search_paragraphs(
                    work_id=self.work_id,
                    keywords=keywords[:15],  # 最多使用 15 个关键词
                    chapter_range=chapter_range,
                    match_mode="any",
                    limit=100
                )

            logger.info(f"[ContentExplorer] 精确搜索命中: {len(results)} 条")

            if not results:
                return False

            # 4. 将结果添加到候选列表，并按需读取原文
            read_limit = AUTO_READ_LIMIT_STRICT if self.require_paragraph_index else AUTO_READ_LIMIT
            read_used = 0
            for r in results:
                # 检查章节范围（二次过滤）
                if self.chapter_scopes and not self._is_chapter_in_scope(r["chapter_order"]):
                    continue

                candidate = {
                    "content": r["text"],
                    "chapter_id": r.get("chapter_id", ""),
                    "chapter_order": r["chapter_order"],
                    "chapter_title": r.get("chapter_title", ""),
                    "paragraph_index": r["paragraph_index"],
                    "node_id": r.get("node_id", ""),
                    "similarity": 1.0,  # 精确匹配
                    "source": "exact_search",
                    "matched_keywords": r.get("matched_keywords", [])
                }

                self.state.add_search_hit(
                    candidate,
                    query=",".join(r.get("matched_keywords", [])[:3]),
                    round_idx=0,  # 0 表示精确搜索阶段
                    chapter_scope_filter=self._is_chapter_in_scope if self.chapter_scopes else None
                )

                if read_used >= read_limit:
                    continue
                chapter_order = r.get("chapter_order")
                if isinstance(chapter_order, str) and chapter_order.isdigit():
                    chapter_order = int(chapter_order)
                paragraph_index = r.get("paragraph_index")
                if isinstance(paragraph_index, str) and paragraph_index.isdigit():
                    paragraph_index = int(paragraph_index)
                if (
                    paragraph_index is None
                    or not chapter_order
                    or not self.state.should_read_paragraph(chapter_order, paragraph_index)
                ):
                    continue

                try:
                    read_result = await read_paragraph.ainvoke({
                        "work_id": self.work_id,
                        "chapter_order": chapter_order,
                        "paragraph_index": paragraph_index,
                        "context_before": 2,
                        "context_after": 2
                    })
                    read_data = json.loads(read_result) if isinstance(read_result, str) else read_result
                    if read_data.get("success"):
                        self.state.record_paragraph_read(chapter_order, paragraph_index)
                        target_text, context_before, context_after = _extract_read_paragraph(read_data)
                        if not target_text:
                            target_text = read_data.get("content") or read_data.get("target_paragraph", "")
                        self.state.add_paragraph({
                            "chapter_order": chapter_order,
                            "chapter_title": read_data.get("chapter_title", ""),
                            "paragraph_index": paragraph_index,
                            "text": target_text,
                            "context_before": context_before,
                            "context_after": context_after,
                            "node_id": read_data.get("node_id", "")
                        }, 0)
                        if target_text:
                            evidence = {
                                "content": target_text,
                                "chapter_order": chapter_order,
                                "paragraph_index": paragraph_index,
                                "similarity": 1.0,
                                "source": "read_paragraph",
                                "chapter_title": read_data.get("chapter_title", "")
                            }
                            if self.state.add_evidence(
                                evidence,
                                query=",".join(r.get("matched_keywords", [])[:3]),
                                round_idx=0,
                                require_paragraph_index=self.require_paragraph_index,
                                chapter_scope_filter=self._is_chapter_in_scope if self.chapter_scopes else None
                            ):
                                read_used += 1
                except Exception as e:
                    logger.warning(f"[ContentExplorer] 精确搜索自动读取失败: {e}")

            logger.info(f"[ContentExplorer] 精确搜索添加证据: {len(self.state.evidences)} 条")
            return len(self.state.evidences) > 0

        except Exception as e:
            logger.error(f"[ContentExplorer] 精确搜索失败: {e}", exc_info=True)
            return False

    async def explore_tool_loop(self) -> ExploreResult:
        """执行探索（opencode 风格：LLM 工具调用循环）"""
        logger.info(f"[ContentExplorer] 开始探索 V5: work_id={self.work_id}, target={self.target_task[:50]}...")

        stop_reason = "达到工具调用上限"
        tool_calls_left = self.max_tool_calls
        reads_left = self.max_read_paragraphs
        last_tool_name = ""
        last_tool_result = ""
        round_idx = 0

        # 范围预检查
        allowed_orders = await self._get_allowed_chapter_orders()
        if self.chapter_scopes and not allowed_orders:
            stop_reason = "范围内无可用章节"
            analysis = await self._generate_analysis()
            total_duration_ms = int((get_utc_now() - self.start_time).total_seconds() * 1000)
            result = ExploreResult(
                evidences=self.state.evidences,
                search_hits=self.state.search_hits,
                paragraphs=self.state.paragraphs,
                chapters=self.state.chapters,
                worldview=self.state.worldview,
                analysis=analysis,
                stats=self.state.get_stats(),
                rounds=self.state.rounds,
                stop_reason=stop_reason,
                total_duration_ms=total_duration_ms
            )
            if self.emit_callback:
                await self._emit_summary_event(result)
            return result

        while tool_calls_left > 0:
            decision = await self._ai_tool_loop_decide(
                round_idx=round_idx + 1,
                last_tool_name=last_tool_name,
                last_tool_result=last_tool_result,
                tool_calls_left=tool_calls_left,
                reads_left=reads_left
            )
            if decision.action == "stop":
                stop_reason = decision.reason or "LLM 停止"
                break

            if decision.tool not in TOOL_LOOP_ALLOWED_TOOLS:
                stop_reason = f"不支持的工具: {decision.tool}"
                break

            if decision.tool in ("read_paragraph", "read_paragraphs") and reads_left <= 0:
                stop_reason = "达到读取上限"
                break

            before_evidences = len(self.state.evidences)
            before_paragraphs = len(self.state.paragraphs)

            tool_call, result_preview, reads_used = await self._execute_tool_action(
                decision.tool,
                decision.args,
                round_idx + 1,
                reads_left
            )

            tool_calls_left -= 1
            reads_left = max(0, reads_left - reads_used)

            new_evidences = len(self.state.evidences) - before_evidences
            new_paragraphs = len(self.state.paragraphs) - before_paragraphs

            round_data = ExploreRound(
                round_idx=round_idx + 1,
                title=_get_round_title(round_idx + 1),
                tool_calls=[tool_call],
                new_evidences_count=new_evidences,
                new_paragraphs_count=new_paragraphs,
                missing_items=[],
                sufficient=False,
                reason=decision.reason or ""
            )
            self.state.rounds.append(round_data)

            if self.emit_callback:
                await self._emit_round_event(round_data)

            last_tool_name = tool_call.tool_name
            last_tool_result = result_preview
            round_idx += 1

            if reads_left <= 0:
                stop_reason = "达到读取上限"
                break

        if self.state.rounds:
            self.state.rounds[-1].sufficient = True
            if stop_reason and not self.state.rounds[-1].reason:
                self.state.rounds[-1].reason = stop_reason

        analysis = await self._generate_analysis()
        total_duration_ms = int((get_utc_now() - self.start_time).total_seconds() * 1000)
        result = ExploreResult(
            evidences=self.state.evidences,
            search_hits=self.state.search_hits,
            paragraphs=self.state.paragraphs,
            chapters=self.state.chapters,
            worldview=self.state.worldview,
            analysis=analysis,
            stats=self.state.get_stats(),
            rounds=self.state.rounds,
            stop_reason=stop_reason,
            total_duration_ms=total_duration_ms
        )

        if self.emit_callback:
            await self._emit_summary_event(result)

        logger.info(f"[ContentExplorer] 探索完成(工具循环): {len(self.state.rounds)}轮, 原因={stop_reason}")
        return result

    async def explore(self) -> ExploreResult:
        """
        执行探索（重构：只读收集器 + LLM 自检循环）

        流程：
        1) 精确搜索（确定性）
        2) LLM 自检决定是否继续探索
        3) 若继续，执行语义搜索+定位+原文读取
        4) 每轮结束后再次自检，直到停止或收敛
        """
        logger.info(f"[ContentExplorer] 开始探索 V4: work_id={self.work_id}, target={self.target_task[:50]}...")

        stop_reason = "达到最大轮次"

        # ========== 阶段1：精确搜索（确定性，无 AI 调用）==========
        exact_search_success = await self._execute_exact_search_phase()
        exact_evidence_count = len(self.state.evidences)
        exact_paragraph_count = len(self.state.paragraphs)

        # 记录精确搜索轮次（不做规则验收）
        if exact_search_success and exact_evidence_count > 0:
            exact_search_round = ExploreRound(
                round_idx=0,
                title="精确搜索",
                tool_calls=[],
                new_evidences_count=exact_evidence_count,
                new_paragraphs_count=exact_paragraph_count,
                missing_items=[],
                sufficient=False,
                reason="精确搜索",
                coverage="",
                summary="",
                next_action=""
            )
            self.state.rounds.append(exact_search_round)
            if self.emit_callback:
                await self._emit_round_event(exact_search_round)

        # LLM 自检决定是否继续
        try:
            decision = await self._ai_self_check(0)
        except Exception as e:
            logger.warning(f"[ContentExplorer] LLM 自检失败，使用默认查询: {e}")
            fallback_query = self.target_task[:30] if self.target_task else ""
            fallback_query = fallback_query.strip()
            next_queries = [fallback_query] if fallback_query else []
            decision = SelfCheckDecision(
                continue_search=bool(next_queries),
                next_queries=next_queries,
                reason="自检失败，使用默认查询"
            )

        # 限制自检循环轮次（上限由 max_rounds 控制）
        max_selfcheck_rounds = self.max_rounds

        if not decision.continue_search:
            stop_reason = decision.reason or "自检停止"
        else:
            for round_idx in range(1, max_selfcheck_rounds + 1):
                round_plan = RoundPlan(
                    exact_keywords=[],
                    semantic_queries=decision.next_queries,
                    chapters_to_read=[],
                    paragraphs_to_read=[],
                    reason=decision.reason or ""
                )

                round_data = await self._execute_round_with_plan(round_idx, round_plan)
                self.state.rounds.append(round_data)

                if self.emit_callback:
                    await self._emit_round_event(round_data)

                # 自检决定是否继续
                try:
                    decision = await self._ai_self_check(round_idx)
                except Exception as e:
                    logger.warning(f"[ContentExplorer] LLM 自检失败，停止探索: {e}")
                    decision = SelfCheckDecision(
                        continue_search=False,
                        next_queries=[],
                        reason="自检失败，停止探索"
                    )

                round_data.reason = decision.reason or round_data.reason
                round_data.sufficient = not decision.continue_search

                if not decision.continue_search or not decision.next_queries:
                    stop_reason = decision.reason or "自检停止"
                    break

                # 收敛判定：连续无新增信息
                if self.state.check_convergence():
                    stop_reason = "信息收敛"
                    break

        # 生成分析
        analysis = await self._generate_analysis()

        # 计算总耗时
        total_duration_ms = int((get_utc_now() - self.start_time).total_seconds() * 1000)

        result = ExploreResult(
            evidences=self.state.evidences,
            search_hits=self.state.search_hits,
            paragraphs=self.state.paragraphs,
            chapters=self.state.chapters,
            worldview=self.state.worldview,
            analysis=analysis,
            stats=self.state.get_stats(),
            rounds=self.state.rounds,
            stop_reason=stop_reason,
            total_duration_ms=total_duration_ms
        )

        # 发射汇总事件
        if self.emit_callback:
            await self._emit_summary_event(result)

        logger.info(f"[ContentExplorer] 探索完成: {len(self.state.rounds)}轮, 原因={stop_reason}")

        return result

    # ==================== LLM 自检 ====================

    async def _ai_self_check(self, round_idx: int) -> SelfCheckDecision:
        """
        LLM 自检：判断是否继续探索，并给出下一轮搜索方向

        仅用于内部循环，不对外输出。
        """
        from app.services.agent.model_selector import TaskType

        ai_service = _get_ai_service()
        collected_summary = self._build_collected_summary()
        searched_hint = ", ".join(list(self.state.searched_queries)[:10]) if self.state.searched_queries else "无"

        prompt = f"""你是信息收集自检器，只负责判断是否需要继续搜索。

目标任务：{self.target_task}
当前轮次：第 {round_idx} 轮

已收集信息：
{collected_summary}

已搜索过的关键词（避免重复）：{searched_hint}

请判断是否还存在明显缺口：
- 若需要继续搜索，请给出 1-3 个下一轮搜索要点（语义短语），避免与已搜索过重复。
- 若不需要继续搜索，next_queries 置空。

只输出 JSON：
{{
  "continue": true,
  "next_queries": ["下一轮要搜的要点1", "要点2"],
  "reason": "一句话说明为何继续或停止"
}}"""

        response = await ai_service.call_ai(
            system_prompt="你是信息收集自检器。只输出 JSON，不要有其他内容。",
            user_prompt=prompt,
            max_tokens=400,
            temperature=0.2,
            task_type=TaskType.SIMPLE_QA
        )

        result = self._parse_json_response(response)
        raw_continue = result.get("continue", False)
        if isinstance(raw_continue, str):
            continue_flag = raw_continue.strip().lower() in ("true", "yes", "1", "是")
        else:
            continue_flag = bool(raw_continue)
        next_queries = [q for q in result.get("next_queries", []) if q and isinstance(q, str)]
        next_queries = [q for q in next_queries if self.state.should_search(q)]
        next_queries = next_queries[:3]
        reason = result.get("reason", "") if isinstance(result, dict) else ""

        if self.search_keywords:
            missing_keywords = []
            for kw in self.search_keywords:
                if not kw:
                    continue
                hit = any(kw in e.text or kw in e.query for e in self.state.evidences)
                if not hit:
                    missing_keywords.append(kw)
            if continue_flag:
                next_queries = [kw for kw in missing_keywords if self.state.should_search(kw)][:3]
            if continue_flag and not next_queries:
                continue_flag = False

        if continue_flag and not next_queries:
            continue_flag = False

        return SelfCheckDecision(
            continue_search=continue_flag,
            next_queries=next_queries,
            reason=reason
        )

    def _build_tool_loop_summary(
        self,
        last_tool_name: str,
        last_tool_result: str,
        tool_calls_left: int,
        reads_left: int
    ) -> str:
        lines = []
        if self.chapter_scopes:
            lines.append(f"- 任务章节范围：{_format_scope_ranges(self.chapter_scopes)}")
        lines.append(f"- 工具调用剩余：{tool_calls_left}，可读段落剩余：{reads_left}")
        lines.append(
            f"- 证据数：{len(self.state.evidences)}，候选数：{len(self.state.search_hits)}，已读段落：{len(self.state.paragraphs)}"
        )
        if self.state.searched_queries:
            lines.append(f"- 已搜索关键词：{', '.join(list(self.state.searched_queries)[:8])}")
        if last_tool_name:
            lines.append(f"- 上一次工具：{last_tool_name}")
        if last_tool_result:
            lines.append(f"- 上一次结果：{_truncate_text(last_tool_result, TOOL_LOOP_RESULT_PREVIEW_LIMIT)}")
        return "\n".join(lines)

    async def _ai_tool_loop_decide(
        self,
        round_idx: int,
        last_tool_name: str,
        last_tool_result: str,
        tool_calls_left: int,
        reads_left: int
    ) -> ToolLoopDecision:
        """LLM 工具循环决策（只读工具）"""
        from app.services.agent.model_selector import TaskType

        ai_service = _get_ai_service()
        summary = self._build_tool_loop_summary(
            last_tool_name,
            last_tool_result,
            tool_calls_left,
            reads_left
        )

        tools_desc = """可用工具（只读）：
1) list_chapters(work_id)
   - 作用：列出章节清单
2) list_paragraphs(work_id, chapter_order|chapter_id, offset, limit, preview_len)
   - 作用：列出某章段落索引（仅预览）
3) exact_search_paragraphs(work_id, keywords, match_mode, limit)
   - 作用：精确关键词匹配（Grep），返回候选段落
4) read_paragraph(work_id, chapter_order|chapter_id, paragraph_index, context_before, context_after)
   - 作用：读取指定段落原文
5) read_paragraphs(work_id, items, context_before, context_after)
   - 作用：批量读取多个段落原文

禁止使用 search_content（语义检索）。
"""

        prompt = f"""你是只读探索器，只能在限定工具内选择下一步行动。

目标任务：{self.target_task}
当前轮次：第 {round_idx} 轮

当前状态：
{summary}

{tools_desc}

请输出 JSON（不要其他内容）：
{{
  "action": "tool" 或 "stop",
  "tool": "工具名（action=tool 时必填）",
  "args": {{ "参数": "值" }},
  "reason": "一句话说明"
}}

注意：
- 必须遵守章节范围约束（如有）。
- 读取原文证据只能来自 read_paragraph/read_paragraphs。
"""

        try:
            response = await ai_service.call_ai(
                system_prompt="你是只读探索器。只输出 JSON，不要有其他内容。",
                user_prompt=prompt,
                max_tokens=500,
                temperature=0.2,
                task_type=TaskType.SIMPLE_QA
            )
            result = self._parse_json_response(response)
        except Exception as e:
            return ToolLoopDecision(action="stop", reason=f"决策失败: {e}")

        action_raw = str(result.get("action", "")).strip().lower()
        tool_name = str(result.get("tool") or result.get("tool_name") or "").strip()
        args = result.get("args") or result.get("params") or {}
        reason = result.get("reason", "") if isinstance(result, dict) else ""
        if not isinstance(args, dict):
            args = {}

        if action_raw in ("stop", "end", "finish", "false", "no"):
            return ToolLoopDecision(action="stop", reason=reason)

        if not action_raw:
            # 如果未明确 action，但给了 tool，则默认执行工具
            if tool_name:
                action_raw = "tool"
            else:
                return ToolLoopDecision(action="stop", reason=reason or "缺少 action/tool")

        if action_raw not in ("tool", "call", "use", "continue"):
            return ToolLoopDecision(action="stop", reason=reason or "非法 action")

        return ToolLoopDecision(action="tool", tool=tool_name, args=args, reason=reason)

    async def _execute_tool_action(
        self,
        tool_name: str,
        args: Dict[str, Any],
        round_idx: int,
        read_budget: int
    ) -> Tuple[ToolCall, str, int]:
        """执行工具调用（只读）"""
        from app.services.agent.langgraph_tools import (
            list_chapters,
            list_paragraphs,
            read_paragraph,
            read_paragraphs
        )
        from app.services.chapter_vector_service import ChapterVectorService

        tool_name = (tool_name or "").strip()
        params = dict(args or {})
        if "work_id" not in params:
            params["work_id"] = self.work_id
        reads_used = 0
        start = get_utc_now()

        def _preview_results(items: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
            preview = []
            for item in items[:limit]:
                if not isinstance(item, dict):
                    continue
                preview.append({
                    "chapter_order": item.get("chapter_order"),
                    "paragraph_index": item.get("paragraph_index"),
                    "snippet": _truncate_text(item.get("snippet") or item.get("content") or "", 80)
                })
            return preview

        result_data: Any = {"success": False, "error": "未执行"}

        if tool_name == "list_chapters":
            chapters = await self._get_chapter_list()
            if self.chapter_scopes:
                chapters = [ch for ch in chapters if self._is_chapter_in_scope(ch.get("order"))]
            result_data = {
                "success": True,
                "count": len(chapters),
                "chapters": chapters
            }

        elif tool_name == "list_paragraphs":
            chapter_order = params.get("chapter_order") or params.get("chapter")
            chapter_id = params.get("chapter_id") or ""
            if isinstance(chapter_order, str) and chapter_order.isdigit():
                chapter_order = int(chapter_order)
            if not isinstance(chapter_order, int) and chapter_id:
                chapters = await self._get_chapter_list()
                for ch in chapters:
                    if ch.get("id") == chapter_id or ch.get("chapter_id") == chapter_id:
                        chapter_order = ch.get("order")
                        break
            if not isinstance(chapter_order, int):
                result_data = {"success": False, "error": "缺少 chapter_order 或 chapter_id"}
            elif self.chapter_scopes and not self._is_chapter_in_scope(chapter_order):
                result_data = {"success": False, "error": f"章节超出范围: {chapter_order}"}
            else:
                params["work_id"] = self.work_id
                params["chapter_order"] = chapter_order
                result = await list_paragraphs.ainvoke(params)
                result_data = json.loads(result) if isinstance(result, str) else result

        elif tool_name == "exact_search_paragraphs":
            raw_keywords = params.get("keywords") or params.get("keyword") or params.get("query") or []
            if isinstance(raw_keywords, str):
                keywords = [raw_keywords.strip()]
            elif isinstance(raw_keywords, list):
                keywords = [str(k).strip() for k in raw_keywords if str(k).strip()]
            else:
                keywords = []
            if not keywords:
                result_data = {"success": False, "error": "缺少 keywords"}
            else:
                # 去重 & 过滤已搜索
                deduped = []
                for kw in keywords:
                    if not kw:
                        continue
                    if self.state.should_search(kw):
                        deduped.append(kw)
                keywords = deduped or keywords
                for kw in keywords:
                    self.state.record_search(kw)

                match_mode = params.get("match_mode") or params.get("mode") or "any"
                limit = params.get("limit") or 50
                if not isinstance(limit, int):
                    try:
                        limit = int(limit)
                    except Exception:
                        limit = 50
                if match_mode not in ("any", "all", "phrase"):
                    match_mode = "any"

                results: List[Dict[str, Any]] = []
                async with AsyncSessionLocal() as db:
                    vector_service = ChapterVectorService(db)
                    if self.chapter_scopes:
                        for start_order, end_order in self.chapter_scopes:
                            part = await vector_service.exact_search_paragraphs(
                                work_id=self.work_id,
                                keywords=keywords,
                                chapter_range=(start_order, end_order),
                                match_mode=match_mode,
                                limit=limit
                            )
                            results.extend(part or [])
                    else:
                        results = await vector_service.exact_search_paragraphs(
                            work_id=self.work_id,
                            keywords=keywords,
                            chapter_range=None,
                            match_mode=match_mode,
                            limit=limit
                        )

                # 章节范围过滤
                if self.chapter_scopes:
                    results = self._filter_results_in_scope(results)

                # 候选去重
                merged = {}
                for item in results:
                    if not isinstance(item, dict):
                        continue
                    if "snippet" not in item and "content" not in item:
                        item["content"] = item.get("text", "")
                    if "source" not in item:
                        item["source"] = "exact_search"
                    if "similarity" not in item:
                        item["similarity"] = 1.0
                    chapter_order = item.get("chapter_order")
                    paragraph_index = item.get("paragraph_index")
                    snippet = item.get("snippet") or item.get("content") or ""
                    key = (chapter_order, paragraph_index, str(snippet)[:80])
                    existing = merged.get(key)
                    if not existing or item.get("similarity", 0) > existing.get("similarity", 0):
                        merged[key] = item
                results = list(merged.values())

                query = ",".join(keywords[:3])
                for item in results:
                    self.state.add_search_hit(
                        item,
                        query=query,
                        round_idx=round_idx,
                        chapter_scope_filter=self._is_chapter_in_scope if self.chapter_scopes else None
                    )

                result_data = {
                    "success": True,
                    "keywords": keywords,
                    "hits": len(results),
                    "results": _preview_results(results)
                }

        elif tool_name == "read_paragraph":
            if read_budget <= 0:
                result_data = {"success": False, "error": "读取预算已用尽"}
            else:
                chapter_order = params.get("chapter_order") or params.get("chapter")
                paragraph_index = params.get("paragraph_index") or params.get("paragraph")
                chapter_id = params.get("chapter_id") or ""
                if isinstance(chapter_order, str) and chapter_order.isdigit():
                    chapter_order = int(chapter_order)
                if isinstance(paragraph_index, str) and paragraph_index.isdigit():
                    paragraph_index = int(paragraph_index)
                if not isinstance(chapter_order, int) and chapter_id:
                    chapters = await self._get_chapter_list()
                    for ch in chapters:
                        if ch.get("id") == chapter_id or ch.get("chapter_id") == chapter_id:
                            chapter_order = ch.get("order")
                            break
                if not isinstance(chapter_order, int) or not isinstance(paragraph_index, int):
                    result_data = {"success": False, "error": "缺少 chapter_order/paragraph_index"}
                elif self.chapter_scopes and not self._is_chapter_in_scope(chapter_order):
                    result_data = {"success": False, "error": f"章节超出范围: {chapter_order}"}
                elif not self.state.should_read_paragraph(chapter_order, paragraph_index):
                    result_data = {"success": True, "skipped": True, "message": "段落已读取"}
                else:
                    params["work_id"] = self.work_id
                    params["chapter_order"] = chapter_order
                    params["paragraph_index"] = paragraph_index
                    if chapter_id:
                        params["chapter_id"] = chapter_id
                    result = await read_paragraph.ainvoke(params)
                    result_data = json.loads(result) if isinstance(result, str) else result

                    if isinstance(result_data, dict) and result_data.get("success"):
                        self.state.record_paragraph_read(chapter_order, paragraph_index)
                        target_text, context_before, context_after = _extract_read_paragraph(result_data)
                        chapter_info = await self._get_chapter_info_by_order(chapter_order)
                        chapter_id = chapter_info.get("chapter_id") or chapter_info.get("id") or ""
                        chapter_title = result_data.get("chapter_title") or chapter_info.get("title") or ""
                        paragraph_data = {
                            "chapter_order": chapter_order,
                            "chapter_title": chapter_title,
                            "paragraph_index": paragraph_index,
                            "text": target_text,
                            "context_before": context_before,
                            "context_after": context_after,
                            "node_id": result_data.get("node_id") or ""
                        }
                        self.state.add_paragraph(paragraph_data, round_idx)
                        self.state.add_evidence(
                            {
                                "snippet": target_text,
                                "content": target_text,
                                "chapter_order": chapter_order,
                                "paragraph_index": paragraph_index,
                                "source": "read_paragraph",
                                "similarity": 1.0,
                                "chapter_id": chapter_id,
                                "chapter_title": chapter_title
                            },
                            query=str(params.get("query") or ""),
                            round_idx=round_idx,
                            require_paragraph_index=self.require_paragraph_index,
                            chapter_scope_filter=self._is_chapter_in_scope if self.chapter_scopes else None
                        )
                        reads_used = 1

        elif tool_name == "read_paragraphs":
            items = params.get("items") or []
            if not isinstance(items, list):
                items = []
            if read_budget <= 0:
                result_data = {"success": False, "error": "读取预算已用尽"}
            else:
                filtered_items = []
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    chapter_order = item.get("chapter_order") or item.get("chapter")
                    if isinstance(chapter_order, str) and chapter_order.isdigit():
                        chapter_order = int(chapter_order)
                        item["chapter_order"] = chapter_order
                    if isinstance(chapter_order, int) and (not self.chapter_scopes or self._is_chapter_in_scope(chapter_order)):
                        filtered_items.append(item)
                items = filtered_items
                if read_budget < len(items):
                    items = items[:read_budget]
                if not items:
                    result_data = {"success": False, "error": "没有可读取的段落（可能超出范围）"}
                else:
                    params["work_id"] = self.work_id
                    params["items"] = items
                    result = await read_paragraphs.ainvoke(params)
                    result_data = json.loads(result) if isinstance(result, str) else result
                    results_list = result_data.get("results", []) if isinstance(result_data, dict) else []
                    for entry in results_list:
                        if not isinstance(entry, dict) or not entry.get("success"):
                            continue
                        chapter_order = entry.get("chapter_order")
                        paragraph_index = entry.get("paragraph_index")
                        if not isinstance(chapter_order, int) or not isinstance(paragraph_index, int):
                            continue
                        if self.chapter_scopes and not self._is_chapter_in_scope(chapter_order):
                            continue
                        self.state.record_paragraph_read(chapter_order, paragraph_index)
                        target_text, context_before, context_after = _extract_read_paragraph(entry)
                        chapter_info = await self._get_chapter_info_by_order(chapter_order)
                        chapter_id = chapter_info.get("chapter_id") or chapter_info.get("id") or ""
                        chapter_title = entry.get("chapter_title") or chapter_info.get("title") or ""
                        paragraph_data = {
                            "chapter_order": chapter_order,
                            "chapter_title": chapter_title,
                            "paragraph_index": paragraph_index,
                            "text": target_text,
                            "context_before": context_before,
                            "context_after": context_after,
                            "node_id": entry.get("node_id") or ""
                        }
                        self.state.add_paragraph(paragraph_data, round_idx)
                        self.state.add_evidence(
                            {
                                "snippet": target_text,
                                "content": target_text,
                                "chapter_order": chapter_order,
                                "paragraph_index": paragraph_index,
                                "source": "read_paragraph",
                                "similarity": 1.0,
                                "chapter_id": chapter_id,
                                "chapter_title": chapter_title
                            },
                            query="",
                            round_idx=round_idx,
                            require_paragraph_index=self.require_paragraph_index,
                            chapter_scope_filter=self._is_chapter_in_scope if self.chapter_scopes else None
                        )
                        reads_used += 1

        else:
            result_data = {"success": False, "error": f"不支持的工具: {tool_name}"}

        duration_ms = int((get_utc_now() - start).total_seconds() * 1000)
        result_preview = json.dumps(result_data, ensure_ascii=False) if isinstance(result_data, dict) else str(result_data)
        result_preview = _truncate_text(result_preview, TOOL_LOOP_RESULT_PREVIEW_LIMIT)
        tool_call = ToolCall(
            tool_name=tool_name,
            params=params,
            result=result_data,
            duration_ms=duration_ms
        )
        return tool_call, result_preview, reads_used

    def _build_collected_summary(self) -> str:
        """构建已收集信息的摘要（V3.3：增加关键词覆盖统计）"""
        lines = []

        if self.chapter_scopes:
            lines.append(f"- 任务章节范围：{_format_scope_ranges(self.chapter_scopes)}")

        # 🆕 V3.3: 关键词覆盖统计（让 AI 明确知道每个关键词的命中情况）
        if self.search_keywords and self.state.evidences:
            lines.append("- 【关键词覆盖统计】")
            for kw in self.search_keywords[:10]:  # 最多展示 10 个关键词
                # 同时检查 e.text 和 e.query（query 包含精确搜索匹配的关键词）
                # 这样即使文本被截断，也能通过 query 检测到匹配
                count = sum(1 for e in self.state.evidences if kw in e.text or kw in e.query)
                status = "✓" if count > 0 else "✗"
                lines.append(f"    · \"{kw}\": {count} 条 {status}")
            lines.append("")  # 空行分隔

        # 证据统计（按章节分组，显示段落号）
        if self.state.evidences:
            evidence_chapters = set(e.chapter_order for e in self.state.evidences if e.chapter_order > 0)
            lines.append(f"- 证据片段：{len(self.state.evidences)} 条，来自章节：{sorted(evidence_chapters)}")

            # 按章节分组展示证据
            by_chapter: Dict[int, List[Evidence]] = {}
            for e in self.state.evidences:
                if e.chapter_order > 0:
                    if e.chapter_order not in by_chapter:
                        by_chapter[e.chapter_order] = []
                    by_chapter[e.chapter_order].append(e)

            for chapter_order in sorted(by_chapter.keys()):
                evidences = by_chapter[chapter_order]
                lines.append(f"  第{chapter_order}章 ({len(evidences)}条):")
                for e in evidences[:3]:  # 每章最多显示3条
                    para_label = f"第{e.paragraph_index}段" if isinstance(e.paragraph_index, int) else "段落未知"
                    lines.append(f"    · [{para_label}] {e.text[:60]}...")
        else:
            lines.append("- 证据片段：0 条")

        # 段落读取详情
        if self.state.paragraphs:
            lines.append(f"- 已读段落：{len(self.state.paragraphs)} 段")
            for p in self.state.paragraphs[:5]:
                lines.append(f"  · 第{p.chapter_order}章第{p.paragraph_index}段: {p.text[:50]}...")

        # 章节统计
        if self.state.chapters:
            chapter_info = [f"{ch.order}({ch.title})" for ch in self.state.chapters.values()]
            lines.append(f"- 已读章节原文：{', '.join(chapter_info)}")
        else:
            lines.append("- 已读章节原文：无")

        # 世界观统计
        if self.state.worldview:
            wv_count = sum(len(items) for items in self.state.worldview.values())
            lines.append(f"- 世界观条目：{wv_count} 个")

        return "\n".join(lines)

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """解析 AI 返回的 JSON（支持嵌套）"""
        import re

        text = response.strip()

        # 移除可能的 markdown 代码块标记
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        try:
            result = json.loads(text)
            return self._normalize_json_types(result)
        except json.JSONDecodeError:
            # 尝试找到 JSON 对象（支持嵌套）
            # 从第一个 { 到最后一个 }
            start_idx = text.find('{')
            end_idx = text.rfind('}')
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = text[start_idx:end_idx + 1]
                try:
                    result = json.loads(json_str)
                    return self._normalize_json_types(result)
                except json.JSONDecodeError:
                    pass
            raise ValueError(f"无法解析 JSON: {text[:200]}")

    def _normalize_json_types(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """规范化 JSON 中的类型（处理 AI 可能返回字符串的布尔值）"""
        if "sufficient" in data:
            val = data["sufficient"]
            if isinstance(val, str):
                data["sufficient"] = val.lower() in ("true", "yes", "是", "1")
        return data

    async def _execute_round_with_plan(self, round_idx: int, plan: RoundPlan) -> ExploreRound:
        """根据 AI 计划执行一轮探索"""
        from app.services.agent.langgraph_tools import search_content, get_writing_context, read_paragraph
        from app.services.agent.tools.locate_tools import locate_content

        tool_calls = []
        new_evidences = 0
        new_paragraphs = 0
        scope_chapter_id = ""
        scope_look_ahead = 0
        scope_contexts: List[Tuple[str, int]] = []
        scope_chapter_id, scope_look_ahead = await self._ensure_scope_context()
        if scope_chapter_id:
            scope_contexts = [(scope_chapter_id, scope_look_ahead)]
        elif self.chapter_scopes:
            scope_contexts = await self._get_scope_search_contexts()

        # 1. 首轮获取世界观
        if round_idx == 1:
            if self.state.should_read_worldview("all"):
                start = get_utc_now()
                try:
                    result = await get_writing_context.ainvoke({
                        "work_id": self.work_id,
                        "include": "worldview"
                    })
                    result_data = json.loads(result) if isinstance(result, str) else result
                    if "worldview" in result_data:
                        wv = result_data["worldview"]
                        for cat, items in wv.items():
                            if isinstance(items, list):
                                self.state.add_worldview_items(items, cat)
                    self.state.record_worldview_read("all")
                    duration = int((get_utc_now() - start).total_seconds() * 1000)
                    tool_calls.append(ToolCall(
                        tool_name="get_writing_context",
                        params={"include": "worldview"},
                        result=result_data,
                        duration_ms=duration
                    ))
                except Exception as e:
                    logger.warning(f"[ContentExplorer] 获取世界观失败: {e}")

        # 2. V3.1: 初始化变量（精确搜索已在阶段1完成，AI补充阶段只用语义搜索）
        auto_locate_used = 0
        auto_read_used = 0
        locate_limit = AUTO_LOCATE_LIMIT_STRICT if self.require_paragraph_index else AUTO_LOCATE_LIMIT
        read_limit = AUTO_READ_LIMIT_STRICT if self.require_paragraph_index else AUTO_READ_LIMIT

        # V3.1 说明：AI 补充阶段不再执行精确搜索
        # 原因：
        # 1. 阶段1已完成精确搜索，找到了所有"字面包含关键词"的内容
        # 2. AI 补充阶段的目的是找"语义相关但字面不同"的内容
        # 3. AI 生成的查询是语义性的（如"林仙的摆烂哲学"），不适合精确搜索
        # 原精确搜索代码已移除，保留 plan.exact_keywords 字段是为了向后兼容

        # 2.2 语义搜索（向量相似度）
        for query in plan.semantic_queries:
            if not self.state.should_search(query):
                continue

            start = get_utc_now()
            try:
                self.state.record_search(query)
                combined_results: List[Dict[str, Any]] = []
                if scope_contexts:
                    for chapter_id, look_ahead in scope_contexts:
                        call_start = get_utc_now()
                        search_params = {
                            "work_id": self.work_id,
                            "query": query,
                            "top_k": 5,
                            "chapter_id": chapter_id,
                            "look_ahead": look_ahead
                        }
                        result = await search_content.ainvoke(search_params)
                        result_data = json.loads(result) if isinstance(result, str) else result
                        combined_results.extend(result_data.get("results", []) if isinstance(result_data, dict) else [])
                        duration = int((get_utc_now() - call_start).total_seconds() * 1000)
                        tool_calls.append(ToolCall(
                            tool_name="search_content",
                            params={
                                "query": query,
                                "chapter_id": chapter_id,
                                "look_ahead": look_ahead
                            },
                            result=result_data,
                            duration_ms=duration
                        ))
                else:
                    search_params = {
                        "work_id": self.work_id,
                        "query": query,
                        "top_k": 5
                    }
                    result = await search_content.ainvoke(search_params)
                    result_data = json.loads(result) if isinstance(result, str) else result
                    combined_results = result_data.get("results", []) if isinstance(result_data, dict) else []
                    duration = int((get_utc_now() - start).total_seconds() * 1000)
                    tool_calls.append(ToolCall(
                        tool_name="search_content",
                        params={"query": query},
                        result=result_data,
                        duration_ms=duration
                    ))
                result_data = {"results": combined_results}

                if self.chapter_scopes and isinstance(result_data, dict):
                    result_data["results"] = self._filter_results_in_scope(result_data.get("results", []))
                if result_data.get("results"):
                    merged = {}
                    for item in result_data.get("results", []):
                        if not isinstance(item, dict):
                            continue
                        chapter_order = item.get("chapter_order")
                        paragraph_index = item.get("paragraph_index")
                        snippet = item.get("snippet") or item.get("content") or ""
                        key = (chapter_order, paragraph_index, str(snippet)[:80])
                        existing = merged.get(key)
                        if not existing or item.get("similarity", 0) > existing.get("similarity", 0):
                            merged[key] = item
                    result_data["results"] = list(merged.values())

                for item in result_data.get("results", []):
                    if not isinstance(item, dict):
                        continue
                    paragraph_index = item.get("paragraph_index")
                    chapter_id = item.get("chapter_id")
                    chapter_order = item.get("chapter_order")
                    snippet = item.get("snippet") or item.get("content") or ""

                    if isinstance(chapter_order, str) and chapter_order.isdigit():
                        chapter_order = int(chapter_order)
                    if isinstance(paragraph_index, str) and paragraph_index.isdigit():
                        paragraph_index = int(paragraph_index)
                        item["paragraph_index"] = paragraph_index
                    if self.chapter_scopes and not self._is_chapter_in_scope(chapter_order):
                        continue

                    self.state.add_search_hit(
                        item,
                        query,
                        round_idx,
                        chapter_scope_filter=self._is_chapter_in_scope if self.chapter_scopes else None
                    )

                    if paragraph_index is None and auto_locate_used < locate_limit and chapter_id:
                        min_snippet_len = 20
                        if self.require_paragraph_index:
                            min_snippet_len = 8
                        locate_candidates = []
                        if snippet and len(snippet) >= min_snippet_len:
                            locate_candidates.append(snippet)
                        if self.require_paragraph_index and query and len(query.strip()) >= 2:
                            locate_candidates.append(query)
                        locate_queries = []
                        seen_locate_queries = set()
                        for candidate in locate_candidates:
                            normalized = _normalize_locate_query(candidate)
                            if not normalized or normalized in seen_locate_queries:
                                continue
                            locate_queries.append(normalized)
                            seen_locate_queries.add(normalized)
                        for locate_query in locate_queries:
                            if auto_locate_used >= locate_limit:
                                break
                            auto_locate_used += 1
                            locate_start = get_utc_now()
                            locate_params = {
                                "chapter_id": chapter_id,
                                "query": locate_query,
                                "allow_global_fallback": False
                            }
                            locate_result = await locate_content.ainvoke(locate_params)
                            locate_data = json.loads(locate_result) if isinstance(locate_result, str) else locate_result
                            locate_duration = int((get_utc_now() - locate_start).total_seconds() * 1000)
                            tool_calls.append(ToolCall(
                                tool_name="locate_content",
                                params={
                                    "chapter_id": chapter_id,
                                    "chapter_order": chapter_order,
                                    "query": locate_query[:80],
                                    "allow_global_fallback": locate_params.get("allow_global_fallback", True)
                                },
                                result=locate_data,
                                duration_ms=locate_duration
                            ))
                            if (
                                isinstance(locate_data, dict)
                                and locate_data.get("success")
                                and not locate_data.get("cross_chapter")
                                and locate_data.get("paragraph_index") is not None
                            ):
                                item["paragraph_index"] = locate_data.get("paragraph_index")
                                paragraph_index = item.get("paragraph_index")
                                if isinstance(paragraph_index, str) and paragraph_index.isdigit():
                                    paragraph_index = int(paragraph_index)
                                    item["paragraph_index"] = paragraph_index
                                break

                    if (
                        paragraph_index is not None
                        and chapter_order
                        and auto_read_used < read_limit
                        and self.state.should_read_paragraph(chapter_order, paragraph_index)
                    ):
                        read_start = get_utc_now()
                        try:
                            read_result = await read_paragraph.ainvoke({
                                "work_id": self.work_id,
                                "chapter_order": chapter_order,
                                "paragraph_index": paragraph_index,
                                "context_before": 2,
                                "context_after": 2
                            })
                            read_data = json.loads(read_result) if isinstance(read_result, str) else read_result

                            if read_data.get("success"):
                                self.state.record_paragraph_read(chapter_order, paragraph_index)
                                target_text, context_before, context_after = _extract_read_paragraph(read_data)
                                if not target_text:
                                    target_text = read_data.get("target_paragraph", "")
                                self.state.add_paragraph({
                                    "chapter_order": chapter_order,
                                    "chapter_title": read_data.get("chapter_title", ""),
                                    "paragraph_index": paragraph_index,
                                    "text": target_text,
                                    "context_before": context_before,
                                    "context_after": context_after,
                                    "node_id": read_data.get("node_id", "")
                                }, round_idx)
                                if target_text:
                                    paragraph_evidence = {
                                        "content": target_text,
                                        "chapter_order": chapter_order,
                                        "paragraph_index": paragraph_index,
                                        "similarity": 1.0,
                                        "source": "read_paragraph",
                                        "chapter_title": read_data.get("chapter_title", "")
                                    }
                                    if self.state.add_evidence(
                                        paragraph_evidence,
                                        query,
                                        round_idx,
                                        require_paragraph_index=self.require_paragraph_index,
                                        chapter_scope_filter=self._is_chapter_in_scope if self.chapter_scopes else None
                                    ):
                                        new_evidences += 1
                                new_paragraphs += 1
                                auto_read_used += 1

                            read_duration = int((get_utc_now() - read_start).total_seconds() * 1000)
                            tool_calls.append(ToolCall(
                                tool_name="read_paragraph",
                                params={"chapter_order": chapter_order, "paragraph_index": paragraph_index},
                                result=read_data,
                                duration_ms=read_duration
                            ))
                        except Exception as e:
                            logger.warning(f"[ContentExplorer] 自动读取段落失败: {e}")

            except Exception as e:
                logger.warning(f"[ContentExplorer] 搜索失败: {e}")

        # 3. 读取 AI 规划的章节
        chapters_to_read = plan.chapters_to_read
        if chapters_to_read:
            normalized = []
            for c in chapters_to_read:
                if isinstance(c, str) and c.isdigit():
                    c = int(c)
                if isinstance(c, int):
                    normalized.append(self._map_title_order_if_needed(c))
            chapters_to_read = normalized
        if self.chapter_scopes:
            chapters_to_read = [c for c in chapters_to_read if self._is_chapter_in_scope(c)]
        chapters_to_read = self._filter_chapters_for_reading(chapters_to_read, limit=2)
        for chapter_order in chapters_to_read:
            if not self.state.should_read_chapter(chapter_order):
                continue

            start = get_utc_now()
            try:
                result = await get_writing_context.ainvoke({
                    "work_id": self.work_id,
                    "chapter_orders": str(chapter_order),
                    "include": "chapter"
                })
                result_data = json.loads(result) if isinstance(result, str) else result
                self.state.record_chapter_read(chapter_order)

                for ch in result_data.get("chapters", []):
                    self.state.add_chapter(ch, round_idx)

                duration = int((get_utc_now() - start).total_seconds() * 1000)
                tool_calls.append(ToolCall(
                    tool_name="get_writing_context",
                    params={"chapter_orders": str(chapter_order)},
                    result=result_data,
                    duration_ms=duration
                ))
            except Exception as e:
                logger.warning(f"[ContentExplorer] 读取章节失败: {e}")

        # 4. 读取 AI 规划的段落（精确验证）
        for para_info in plan.paragraphs_to_read:
            if not isinstance(para_info, dict):
                continue
            chapter_order = para_info.get("chapter") or para_info.get("chapter_order")
            paragraph_index = para_info.get("paragraph") or para_info.get("paragraph_index")
            if isinstance(chapter_order, str) and chapter_order.isdigit():
                chapter_order = int(chapter_order)
            if isinstance(chapter_order, int):
                chapter_order = self._map_title_order_if_needed(chapter_order)
            if not chapter_order or paragraph_index is None:
                continue
            if self.chapter_scopes and not self._is_chapter_in_scope(chapter_order):
                continue

            # 检查是否已读取该段落
            if not self.state.should_read_paragraph(chapter_order, paragraph_index):
                continue

            start = get_utc_now()
            try:
                result = await read_paragraph.ainvoke({
                    "work_id": self.work_id,
                    "chapter_order": chapter_order,
                    "paragraph_index": paragraph_index,
                    "context_before": 2,
                    "context_after": 2
                })
                result_data = json.loads(result) if isinstance(result, str) else result

                # 添加段落到状态
                if result_data.get("success"):
                    self.state.record_paragraph_read(chapter_order, paragraph_index)
                    target_text, context_before, context_after = _extract_read_paragraph(result_data)
                    if not target_text:
                        target_text = result_data.get("target_paragraph", "")
                    self.state.add_paragraph({
                        "chapter_order": chapter_order,
                        "chapter_title": result_data.get("chapter_title", ""),
                        "paragraph_index": paragraph_index,
                        "text": target_text,
                        "context_before": context_before,
                        "context_after": context_after,
                        "node_id": result_data.get("node_id", "")
                    }, round_idx)
                    if target_text:
                        paragraph_evidence = {
                            "content": target_text,
                            "chapter_order": chapter_order,
                            "paragraph_index": paragraph_index,
                            "similarity": 1.0,
                            "source": "read_paragraph",
                            "chapter_title": result_data.get("chapter_title", "")
                        }
                        if self.state.add_evidence(
                            paragraph_evidence,
                            "",
                            round_idx,
                            require_paragraph_index=self.require_paragraph_index,
                            chapter_scope_filter=self._is_chapter_in_scope if self.chapter_scopes else None
                        ):
                            new_evidences += 1
                    new_paragraphs += 1

                duration = int((get_utc_now() - start).total_seconds() * 1000)
                tool_calls.append(ToolCall(
                    tool_name="read_paragraph",
                    params={"chapter_order": chapter_order, "paragraph_index": paragraph_index},
                    result=result_data,
                    duration_ms=duration
                ))
            except Exception as e:
                logger.warning(f"[ContentExplorer] 读取段落失败: {e}")

        # 5. 如果 AI 没有规划任何行动，使用从证据中提取的章节
        # V3.1: 移除 exact_keywords 检查（已废弃），只检查实际使用的字段
        if not plan.semantic_queries and not plan.chapters_to_read and not plan.paragraphs_to_read:
            chapters_from_evidence = self._filter_chapters_for_reading(
                self._determine_chapters_to_read(),
                limit=2
            )
            for chapter_order in chapters_from_evidence:
                if not self.state.should_read_chapter(chapter_order):
                    continue

                start = get_utc_now()
                try:
                    result = await get_writing_context.ainvoke({
                        "work_id": self.work_id,
                        "chapter_orders": str(chapter_order),
                        "include": "chapter"
                    })
                    result_data = json.loads(result) if isinstance(result, str) else result
                    self.state.record_chapter_read(chapter_order)

                    for ch in result_data.get("chapters", []):
                        self.state.add_chapter(ch, round_idx)

                    duration = int((get_utc_now() - start).total_seconds() * 1000)
                    tool_calls.append(ToolCall(
                        tool_name="get_writing_context",
                        params={"chapter_orders": str(chapter_order)},
                        result=result_data,
                        duration_ms=duration
                    ))
                except Exception as e:
                    logger.warning(f"[ContentExplorer] 读取章节失败: {e}")

        return ExploreRound(
            round_idx=round_idx,
            title=_get_round_title(round_idx),  # 使用固定的简短标题
            reason=plan.reason if plan.reason else "",  # 保存完整的 AI 决策理由
            tool_calls=tool_calls,
            new_evidences_count=new_evidences,
            new_paragraphs_count=new_paragraphs,
            missing_items=[],  # 由 AI 评估后填充
            sufficient=False   # 由 AI 评估后更新
        )

    # ==================== 辅助方法 ====================

    def _determine_chapters_to_read(self) -> List[int]:
        """确定需要读取的章节"""
        # 从证据中提取章节号
        chapter_orders = set()
        for e in self.state.evidences:
            if e.chapter_order > 0:
                chapter_orders.add(e.chapter_order)

        # 排除已读取的
        to_read = [o for o in chapter_orders if o not in self.state.read_chapter_orders]
        if self.chapter_scopes:
            to_read = [o for o in to_read if self._is_chapter_in_scope(o)]

        return self._rank_chapters_by_evidence(to_read)

    async def _generate_analysis(self) -> str:
        """生成分析总结（优先使用 AI 生成的）"""
        # 优先使用最后一轮 AI 生成的 summary
        if self.state.rounds:
            last_round = self.state.rounds[-1]
            if last_round.summary:
                return last_round.summary

        # 兜底：生成硬编码统计信息
        stats = self.state.get_stats()

        analysis = f"经过 {stats['rounds_count']} 轮深度探索，收集到以下信息：\n\n"
        analysis += f"1. 世界观条目：{stats['total_worldview_items']} 个\n"
        analysis += f"2. 章节原文：{stats['total_chapters']} 章\n"
        analysis += f"3. 证据片段：{stats['total_evidences']} 条\n"
        analysis += f"4. 段落原文：{stats['total_paragraphs']} 段\n\n"
        if self.require_paragraph_index and self.state.skipped_evidences_strict:
            analysis += (
                f"严格段落号模式发现 {self.state.skipped_evidences_strict} 条无段落号证据（已保留待补齐）。\n\n"
            )

        if self.state.chapters:
            chapter_titles = [ch.title for ch in self.state.chapters.values()]
            analysis += f"已读取章节：{', '.join(chapter_titles)}\n"

        return analysis

    async def _emit_round_event(self, round_data: ExploreRound):
        """发射轮次事件"""
        from app.services.agent.stream.flow_events import FlowEventBuilder

        # 获取本轮的证据
        round_evidences = [
            {"chapter": e.chapter_order, "paragraph": e.paragraph_index, "text": e.text[:100]}
            for e in self.state.evidences if e.round_idx == round_data.round_idx
        ]

        event = FlowEventBuilder.explore_round(
            step_id=self.step_id,
            round_idx=round_data.round_idx,
            title=round_data.title,
            tool_calls=_format_tool_calls_for_frontend(round_data),
            hit_count=round_data.new_evidences_count,
            missing_items=round_data.missing_items,
            status_text=_get_status_text(round_data),
            evidences=round_evidences,
            review_status=_get_review_status(round_data),
            reason=round_data.reason  # AI 决策理由（完整）
        )
        await self.emit_callback(event)

    async def _emit_summary_event(self, result: ExploreResult):
        """发射汇总事件"""
        from app.services.agent.stream.flow_events import FlowEventBuilder

        last_round = result.rounds[-1] if result.rounds else None
        stats = {
            "worldview": sum(len(items) for items in result.worldview.values()),
            "chapters": _format_chapters_range(result.chapters),
            "evidences": len(result.evidences)
        }

        # 使用 AI 生成的总结和下一步行动（如果有的话）
        summary = result.analysis  # 默认使用硬编码的分析
        next_action = "基于这些背景信息，我将执行后续任务。"  # 默认值

        if last_round:
            # 优先使用 AI 生成的总结
            if last_round.summary:
                summary = last_round.summary
            # 优先使用 AI 生成的下一步行动
            if last_round.next_action:
                next_action = last_round.next_action

        event = FlowEventBuilder.explore_summary(
            step_id=self.step_id,
            total_rounds=len(result.rounds),
            summary=summary,  # AI 生成的总结
            next_action=next_action,  # AI 生成的下一步行动
            next_tool="",
            stats=stats,
            sufficient=None,
            coverage=None
        )
        await self.emit_callback(event)


# ==================== 工具定义 ====================

@tool
@register_as_tool("explore_content", "explore", "深度探索内容收集相关信息")
async def explore_content(
    work_id: str,
    target_task: str,
    search_keywords: Optional[List[str]] = None,
    max_rounds: int = 10,
    explore_mode: str = "tool_loop",
    max_tool_calls: Optional[int] = None,
    max_read_paragraphs: Optional[int] = None,
    output_mode: str = "full",
    user_id: Optional[str] = None,
    conversation_id: Optional[str] = None
) -> str:
    """深度探索内容，收集完成任务所需的所有信息

    Args:
        work_id: 作品ID（UUID格式，必需）
        target_task: 目标任务描述（如"续写第6章，需要了解主角性格和当前剧情"）
        search_keywords: 搜索关键词列表（由规划阶段直接提供，优先使用）
        max_rounds: 最大探索轮次（默认10轮）
        explore_mode: 探索模式（pipeline/tool_loop，默认pipeline）
        max_tool_calls: 工具调用上限（仅 tool_loop 生效）
        max_read_paragraphs: 读取段落上限（仅 tool_loop 生效）
        output_mode: 输出模式（full/evidence_only，默认full）
        user_id: 用户ID（可选）
        conversation_id: 会话ID（可选，用于共享缓存）

    Returns:
        JSON格式的探索结果
    """
    logger.info(f"[explore_content] 开始: work_id={work_id}, target={target_task[:50]}...")
    if search_keywords:
        logger.info(f"[explore_content] 规划传入关键词: {search_keywords[:10]}")
    output_mode_norm = (output_mode or "full").strip().lower()
    evidence_only_output = output_mode_norm in ("evidence", "evidence_only", "minimal")

    stream_handler = get_stream_event_handler()
    step_id = get_explore_step_id()
    step_id_value = None
    if step_id is not None:
        try:
            step_id_value = int(step_id)
        except (TypeError, ValueError):
            step_id_value = None

    events_emitted = False
    emit_callback = None
    if stream_handler and stream_handler.has_flow_event_callback():
        async def emit_callback(event: dict) -> None:
            nonlocal events_emitted
            if await stream_handler.emit_flow_event(event):
                events_emitted = True

    chapter_scopes = _parse_chapter_scopes(target_task)
    shared_cache_key = _build_explore_shared_key(
        work_id,
        user_id,
        conversation_id,
        chapter_scopes
    )
    shared_state = None
    if shared_cache_key:
        cached_state = _EXPLORE_SHARED_CACHE.get(shared_cache_key)
        if isinstance(cached_state, ExploreState):
            shared_state = cached_state

    explorer = ContentExplorer(
        work_id=work_id,
        target_task=target_task,
        max_rounds=max_rounds,
        emit_callback=emit_callback,
        step_id=step_id_value,
        search_keywords=search_keywords,
        explore_mode=explore_mode,
        max_tool_calls=max_tool_calls,
        max_read_paragraphs=max_read_paragraphs
    )
    if shared_state:
        explorer.state = _clone_explore_state(shared_state)
        logger.info(
            "[explore_content] 复用共享状态: searched=%s, read_paragraphs=%s, read_chapters=%s",
            len(explorer.state.searched_queries),
            len(explorer.state.read_paragraph_positions),
            len(explorer.state.read_chapter_orders)
        )

    try:
        if explorer.explore_mode in ("tool_loop", "tool", "opencode"):
            result = await explorer.explore_tool_loop()
        else:
            result = await explorer.explore()

        if shared_cache_key:
            cached_state = _EXPLORE_SHARED_CACHE.get(shared_cache_key)
            if isinstance(cached_state, ExploreState):
                merged_state = _merge_explore_states(cached_state, explorer.state)
                _EXPLORE_SHARED_CACHE.set(shared_cache_key, merged_state)
            else:
                _EXPLORE_SHARED_CACHE.set(shared_cache_key, _clone_explore_state(explorer.state))

        # 构建 explore_summary - 供后续工具（如 analyze_content）使用的文本摘要
        explore_summary = _build_explore_summary(result)

        # 2026-01-18: 构建兼容 get_writing_context 的 chapters 数组
        chapters_list = [
            {
                "id": str(ch.id) if ch.id else "",
                "title": ch.title,
                "order": ch.order,
                "content": ch.content,
                "word_count": ch.word_count
            }
            for order, ch in sorted(result.chapters.items())
        ]
        chapters_by_order = {
            entry.get("order"): entry
            for entry in chapters_list
            if entry.get("order")
        }
        fallback_chapters: Dict[int, Dict[str, Any]] = {}

        def _add_fallback_chapter(chapter_order: int, chapter_id: str = "", chapter_title: str = "") -> None:
            if not chapter_order:
                return
            entry = fallback_chapters.get(chapter_order)
            if not entry:
                entry = {
                    "id": "",
                    "title": "",
                    "order": chapter_order,
                    "content": "",
                    "word_count": 0
                }
            if not entry["id"] and chapter_id:
                entry["id"] = chapter_id
            if not entry["title"] and chapter_title:
                entry["title"] = chapter_title
            fallback_chapters[chapter_order] = entry

        for e in result.evidences:
            _add_fallback_chapter(e.chapter_order, e.chapter_id, e.chapter_title)

        for p in result.paragraphs:
            entry = chapters_by_order.get(p.chapter_order, {})
            chapter_id = entry.get("id") or entry.get("chapter_id") or ""
            chapter_title = p.chapter_title or entry.get("title") or ""
            _add_fallback_chapter(p.chapter_order, chapter_id, chapter_title)

        if fallback_chapters and work_id:
            try:
                from app.services.agent.langgraph_tools import resolve_chapter_id
                for chapter_order, entry in fallback_chapters.items():
                    if entry["id"]:
                        continue
                    resolved_id, _ = await resolve_chapter_id(work_id, str(chapter_order))
                    if resolved_id:
                        entry["id"] = resolved_id
            except Exception:
                pass

        for entry in fallback_chapters.values():
            if not entry["title"]:
                entry["title"] = f"第{entry['order']}章"

        if fallback_chapters:
            for chapter_order, entry in fallback_chapters.items():
                existing = chapters_by_order.get(chapter_order)
                if existing:
                    if not existing.get("id") and entry.get("id"):
                        existing["id"] = entry["id"]
                    if not existing.get("title") and entry.get("title"):
                        existing["title"] = entry["title"]
                    if not existing.get("content") and entry.get("content"):
                        existing["content"] = entry["content"]
                    if not existing.get("word_count") and entry.get("word_count"):
                        existing["word_count"] = entry["word_count"]
                else:
                    chapters_by_order[chapter_order] = entry
            chapters_list = [
                chapters_by_order[chapter_order]
                for chapter_order in sorted(chapters_by_order)
            ]

        if chapters_list and work_id:
            try:
                from app.services.agent.langgraph_tools import resolve_chapter_id
                for entry in chapters_list:
                    entry_id = entry.get("id")
                    if entry_id:
                        if not isinstance(entry_id, str):
                            entry["id"] = str(entry_id)
                        continue
                    chapter_order = entry.get("order") or entry.get("chapter_order")
                    if chapter_order:
                        resolved_id, _ = await resolve_chapter_id(work_id, str(chapter_order))
                        if resolved_id:
                            entry["id"] = resolved_id
                    if entry.get("id") is None:
                        entry["id"] = ""
            except Exception:
                pass

        for entry in chapters_list:
            if "chapter_id" not in entry:
                entry["chapter_id"] = entry.get("id") or ""

        for entry in chapters_list:
            entry["paragraphs"] = _build_chapter_paragraphs(
                result,
                entry.get("order", 0),
                entry.get("content", "")
            )

        # 2026-01-18: 构建兼容 get_writing_context 的 worldview 对象
        worldview_dict = {}
        for category, items in result.worldview.items():
            worldview_dict[category] = [
                {"name": item.name, "description": item.description}
                for item in items
            ]

        node_id_map = _build_node_id_map(result)
        locate_targets = _build_locate_targets(
            result,
            chapters_by_order,
            node_id_map=node_id_map,
            candidates=getattr(result, "search_hits", None)
        )
        evidences_output = _build_evidences_output(result, node_id_map=node_id_map)

        if evidence_only_output:
            return json.dumps({
                "success": True,
                "work_id": work_id,
                "target_task": target_task,
                "evidences": evidences_output,
                "locate_targets": locate_targets,
                "events_emitted": events_emitted
            }, ensure_ascii=False, indent=2)

        frontend_display = to_frontend_display(result)
        search_results = _build_search_results(result, node_id_map=node_id_map)
        if search_results and work_id:
            try:
                from app.services.agent.langgraph_tools import resolve_chapter_id
                for item in search_results:
                    chapter_order = item.get("chapter_order")
                    if not item.get("chapter_id") and chapter_order:
                        resolved_id, _ = await resolve_chapter_id(work_id, str(chapter_order))
                        if resolved_id:
                            item["chapter_id"] = resolved_id
                    if not item.get("chapter_title") and chapter_order:
                        item["chapter_title"] = f"第{chapter_order}章"
            except Exception:
                pass
        frontend_display["search_results"] = search_results
        frontend_display["locate_targets"] = locate_targets

        # 转换为JSON
        return json.dumps({
            "success": True,
            "work_id": work_id,
            "target_task": target_task,
            "analysis": result.analysis,
            "stats": result.stats,
            "stop_reason": result.stop_reason,
            "total_duration_ms": result.total_duration_ms,
            "frontend_display": frontend_display,
            "context_for_task": build_context_for_task(result),
            "events_emitted": events_emitted,
            # 添加 explore_summary 字段，便于 ParameterResolver 解析
            "explore_summary": explore_summary,
            # 新增：证据与定位目标（对外输出）
            "evidences": evidences_output,
            "locate_targets": locate_targets,
            # 2026-01-18: 添加兼容字段，支持 $ref 引用
            "chapters": chapters_list,
            "results": chapters_list,
            "worldview": worldview_dict
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"[explore_content] 失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "work_id": work_id
        }, ensure_ascii=False)
