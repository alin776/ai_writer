# -*- coding: utf-8 -*-
"""
Explore 内容探索工具（AI 驱动版本）

实现深度内容探索的核心逻辑：
1. LLM 通过工具循环逐步收集证据
2. 先列章节/段落预览，再精确搜索与读取原文
3. 基于已读原文证据做停止判断
4. 流式事件支持前端展示

Version: 2.0 - AI 驱动的 SubAgent 模式
"""

import json
import logging
import re
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Any, Optional, Callable, Awaitable
from datetime import datetime

from langchain_core.tools import tool
from .tool_registry import register_as_tool
from app.utils.datetime_utils import get_utc_now
from app.core.config import settings
from app.services.agent.utils.tool_context import get_stream_event_handler, get_explore_step_id
from app.services.agent.utils.performance import MemoryCache
from app.services.agent.utils.intent_retrieval import (
    IntentCompiler,
    QueryProgramBuilder,
    EvidenceJudge,
    IterationState,
    IntentSpec,
    AdaptiveController,
)
from app.services.agent.utils.explore_artifact import (
    save_explore_artifact as _save_explore_artifact,
    load_explore_artifact as _load_explore_artifact,
    record_session_artifact as _record_session_artifact
)
from app.core.database import AsyncSessionLocal
from app.core.redis import RedisClient

logger = logging.getLogger(__name__)

MIN_EVIDENCE_SIMILARITY = 0.35
AUTO_LOCATE_LIMIT = 3
AUTO_READ_LIMIT = 3
AUTO_LOCATE_LIMIT_STRICT = 12
AUTO_READ_LIMIT_STRICT = 12
LOCATE_QUERY_MAX_LEN = 200

TOOL_LOOP_MAX_CALLS_DEFAULT = 200
TOOL_LOOP_MAX_READS_DEFAULT = 200
TOOL_LOOP_RESULT_PREVIEW_LIMIT = 1200
SEARCH_HIT_TEXT_LIMIT = 2000
KEYWORD_READ_MAX_PER_TERM = 2
SEARCH_HIT_PREVIEW_LIMIT = 100
SEARCH_HIT_TOTAL_CHAR_LIMIT = 20000
SEARCH_HIT_MIN_ITEMS = 5
LIST_PARAGRAPHS_PAGE_SIZE = 50
ZERO_HIT_FORCE_REWRITE_THRESHOLD = 2
ZERO_HIT_NON_EXISTENT_MIN_STRATEGIES = 3
ZERO_HIT_SAME_FINGERPRINT_MAX_RETRIES = 1
FORCED_REWRITE_MAX_ROUNDS = 2
NO_PROGRESS_STOP_MIN_ROUNDS = 6
TOOL_LOOP_REPEAT_SIGNATURE_THRESHOLD = 2
TOOL_SIGNATURE_NOISE_PARAMS = {
    "cursor",
    "next_cursor",
    "query_session_id",
    "timestamp",
    "request_id",
}
INTENT_RETRIEVAL_MAX_PROBES = 8
INTENT_JUDGE_CARD_PREVIEW = 8
PER_CHAPTER_READ_CAP_RATIO = 0.2
PER_CHAPTER_READ_CAP_MIN = 10
PER_CHAPTER_READ_CAP_MAX = 30
TOOL_LOOP_ALLOWED_TOOLS = (
    "list_chapters",
    "list_paragraphs",
    "exact_search_paragraphs",
    "read_paragraph",
    "read_paragraphs"
)

EXPLORE_SHARED_TTL_SECONDS = 20 * 60
_EXPLORE_SHARED_CACHE = MemoryCache(max_size=50, default_ttl=EXPLORE_SHARED_TTL_SECONDS)
EXPLORE_RESULT_CACHE_TTL_SECONDS = 60 * 60
EXPLORE_RESULT_CACHE_MAX_CHARS = 200000
EXPLORE_RESULT_CACHE_VERSION = "v1"

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
    "改写",
    "替换",
    "润色",
    "插入",
    "扩写",
    "优化",
    "smart_rewrite",
    "smart_insert",
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


def _strip_chapter_hint_for_global_search(text: str) -> str:
    if not text:
        return text
    cleaned = text
    cleaned = re.sub(r"在章节\s*[0-9a-fA-F-]{8,36}\s*中", "在全文中", cleaned)
    cleaned = re.sub(r"章节\s*[0-9a-fA-F-]{8,36}", "全文", cleaned)
    cleaned = re.sub(r"(本章|当前章节|当前章|这一章|该章|此章)", "全文", cleaned)
    return cleaned


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
    # 避免 UUID 中的“数字-数字”片段被误识别为章节范围（如 e7-1917 -> 7-191）
    text = re.sub(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b", " ", text)
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
        _ai_service = HTTPAIService(model="gemini-2.5-flash", enable_model_selector=False)
    return _ai_service


# ==================== AI 决策数据结构 ====================

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
    is_target: bool = True       # 是否为明确目标段落（上下文范围读取为 False）


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
class SearchRecord:
    """搜索记录（类似 OpenCode 的 ToolPart）

    设计原则（来自 OpenCode）：
    - 元数据永久保留（query, tool, chapters）
    - 摘要智能压缩（hits_summary）
    - AI 决策时可见完整搜索历史

    穷尽标记设计：
    - chapter_scope: 搜索的章节范围，None 表示全书
    - worldview_checked: 是否已检查过世界观库
    - exhausted: 计算属性，判断是否已穷尽所有数据源
    """
    query: str                      # 搜索关键词
    tool: str                       # 工具名称
    hits_count: int                 # 命中数量
    hits_summary: str               # 结果摘要（关键信息，≤100字符）
    chapters_covered: List[int]     # 覆盖的章节号
    round_idx: int                  # 第几轮搜索的
    timestamp: datetime = field(default_factory=get_utc_now)
    compacted: bool = False         # 是否已被压缩（旧记录）
    chapter_scope: Optional[Tuple[int, int]] = None  # 搜索范围，None=全书
    worldview_checked: bool = False                   # 是否检查过世界观库
    worldview_hits: int = 0                           # 世界观命中数

    @property
    def exhausted(self) -> bool:
        """是否已穷尽所有数据源

        穷尽条件：
        1. 章节原文 0 命中 + 无范围限制（或已搜全书）
        2. 世界观也查过且 0 命中
        """
        return (
            self.hits_count == 0
            and self.chapter_scope is None
            and self.worldview_checked
            and self.worldview_hits == 0
        )


@dataclass
class QueryAttempt:
    """单次查询尝试（用于循环治理与可观测）"""
    query: str
    keywords: List[str]
    match_mode: str
    chapter_scope: Optional[Tuple[int, int]]
    round_idx: int
    strategy: str = "ai"  # ai/forced_rewrite
    hits: int = 0
    chapter_hits: int = 0
    worldview_hits: int = 0
    blocked_keywords: int = 0
    error: str = ""
    keyword_fingerprint: str = ""
    intent_id: str = ""
    probe_signature: str = ""
    probe_hypothesis: str = ""
    failure_reason: str = ""
    timestamp: datetime = field(default_factory=get_utc_now)


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

    context_coverage: Dict[Tuple[int, int], Tuple[int, int]] = field(default_factory=dict)
    # 目标段落的上下文覆盖范围 {(chapter_order, target_index): (start_index, end_index)}

    read_chapter_orders: Set[int] = field(default_factory=set)
    # 已读取完整原文的章节序号

    read_worldview_categories: Set[str] = field(default_factory=set)
    # 已读取的世界观分类

    # ========== 轮次记录（给前端展示）==========

    rounds: List[ExploreRound] = field(default_factory=list)
    # 每轮的执行记录

    # ========== 搜索历史（类似 OpenCode 的 ToolPart 历史）==========

    search_history: List['SearchRecord'] = field(default_factory=list)
    # 完整的搜索历史，包含每次搜索的结果摘要

    query_attempts: List['QueryAttempt'] = field(default_factory=list)
    # 每轮 exact_search 查询参数与命中情况（用于程序化防打转）

    iteration_state: IterationState = field(default_factory=IterationState)
    # 探针执行状态（签名防重、失败分布、must-have 覆盖率）

    latest_intent_spec: Dict[str, Any] = field(default_factory=dict)
    # 最近一次编译出的意图对象

    latest_query_program: Dict[str, Any] = field(default_factory=dict)
    # 最近一次生成的查询程序（用于可观测）

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
        """判断是否应该执行搜索（避免同查询短时间内重复空转）"""
        normalized = ",".join(_normalize_search_keywords((query or "").split(",")))
        if not normalized:
            return False
        if normalized not in self.searched_queries:
            return True
        # 同一 query 最近连续 0 命中时，要求换词/换范围
        repeated_zero = 0
        for attempt in reversed(self.query_attempts[-6:]):
            if (attempt.query or "") != normalized:
                continue
            if int(attempt.chapter_hits or 0) == 0 and int(attempt.worldview_hits or 0) == 0:
                repeated_zero += 1
            else:
                break
        return repeated_zero <= 1

    def record_search(self, query: str):
        """记录已搜索的 query"""
        self.searched_queries.add(query)

    def should_read_paragraph(self, chapter_order: int, paragraph_index: int) -> bool:
        """判断是否应该读取段落"""
        position = (chapter_order, paragraph_index)
        return position not in self.read_paragraph_positions

    def record_paragraph_read(self, chapter_order: int, paragraph_index: int):
        """记录已读取的段落"""
        self.read_paragraph_positions.add((chapter_order, paragraph_index))

    def record_context_coverage(
        self,
        chapter_order: int,
        target_index: int,
        start_index: int,
        end_index: int
    ) -> None:
        """记录目标段落的上下文覆盖范围"""
        key = (chapter_order, target_index)
        if key in self.context_coverage:
            prev_start, prev_end = self.context_coverage[key]
            start_index = min(prev_start, start_index)
            end_index = max(prev_end, end_index)
        self.context_coverage[key] = (start_index, end_index)

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
            text=result.get("snippet", result.get("content", ""))[:SEARCH_HIT_TEXT_LIMIT],
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
            node_id=data.get("node_id", "") or "",
            is_target=bool(data.get("is_target", True))
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
            name = item.get("name") or item.get("term") or ""
            description = item.get("description") or item.get("definition") or ""
            self.worldview[category].append(WorldviewItem(
                id=item.get("id", ""),
                name=name,
                category=category,
                description=description,
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

    # ========== 搜索历史管理（类似 OpenCode 的 Compaction）==========

    def add_search_record(self, record: 'SearchRecord') -> None:
        """添加搜索记录，并执行智能压缩"""
        self.search_history.append(record)
        self._compact_old_records()

    def add_query_attempt(self, attempt: 'QueryAttempt') -> None:
        """记录一次查询尝试（最多保留最近 50 条）"""
        self.query_attempts.append(attempt)
        if len(self.query_attempts) > 50:
            self.query_attempts = self.query_attempts[-50:]

    @staticmethod
    def _build_attempt_fingerprint(
        keywords: List[str],
        scope: Optional[Tuple[int, int]],
        mode: str
    ) -> str:
        # 局部导入，兼容 AST 片段测试环境（测试会抽取方法体单独执行）
        import hashlib as _hashlib

        normalized_keywords = sorted({
            str(kw).strip().lower()
            for kw in (keywords or [])
            if str(kw).strip()
        })
        scope_text = "global"
        if isinstance(scope, tuple) and len(scope) == 2:
            scope_text = f"{scope[0]}-{scope[1]}"
        mode_text = (mode or "any").strip().lower()
        raw = f"{','.join(normalized_keywords)}|{scope_text}|{mode_text}"
        return _hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]

    def count_zero_hit_fingerprint(
        self,
        keywords: List[str],
        scope: Optional[Tuple[int, int]],
        mode: str,
        window: int = 12
    ) -> int:
        if window <= 0:
            return 0
        fingerprint = self._build_attempt_fingerprint(keywords, scope, mode)
        attempts = self.query_attempts[-window:]
        count = 0
        for attempt in attempts:
            attempt_fingerprint = attempt.keyword_fingerprint or self._build_attempt_fingerprint(
                attempt.keywords,
                attempt.chapter_scope,
                attempt.match_mode,
            )
            if attempt_fingerprint != fingerprint:
                continue
            if int(attempt.chapter_hits or 0) != 0 or int(attempt.worldview_hits or 0) != 0:
                continue
            count += 1
        return count

    def has_recent_zero_hit_fingerprint(
        self,
        keywords: List[str],
        scope: Optional[Tuple[int, int]],
        strategy: str,
        mode: str,
        window: int = 8
    ) -> bool:
        if window <= 0:
            return False
        fingerprint = self._build_attempt_fingerprint(keywords, scope, mode)
        for attempt in reversed(self.query_attempts[-window:]):
            attempt_fingerprint = attempt.keyword_fingerprint or self._build_attempt_fingerprint(
                attempt.keywords,
                attempt.chapter_scope,
                attempt.match_mode,
            )
            if attempt_fingerprint != fingerprint:
                continue
            if int(attempt.chapter_hits or 0) != 0 or int(attempt.worldview_hits or 0) != 0:
                continue
            if strategy and (attempt.strategy or "").strip().lower() != strategy.strip().lower():
                continue
            return True
        return False

    def count_query_attempts(self) -> int:
        return len(self.query_attempts)

    def get_recent_query_attempts(self, limit: int = 6) -> List['QueryAttempt']:
        if limit <= 0:
            return []
        return self.query_attempts[-limit:]

    def has_full_scope_rewrite_proof(self, keyword: str) -> bool:
        """是否有“全书+改写策略+0命中”的证据，才允许视作穷尽"""
        if not keyword:
            return False
        has_full_scope_zero = False
        has_rewrite_zero = False
        for attempt in reversed(self.query_attempts):
            if keyword not in attempt.keywords:
                continue
            if attempt.chapter_scope is not None:
                continue
            if attempt.chapter_hits != 0 or attempt.worldview_hits != 0:
                continue
            has_full_scope_zero = True
            strategy_text = (attempt.strategy or "").lower()
            if "forced_rewrite" in strategy_text or "fallback" in strategy_text:
                has_rewrite_zero = True
            if has_full_scope_zero and has_rewrite_zero:
                return True
        return False

    def _compact_old_records(self, keep_recent: int = 10) -> None:
        """压缩旧的搜索记录（类似 OpenCode 的 Prune）

        策略：
        - 保留最近 keep_recent 条记录的完整摘要
        - 旧记录标记为 compacted，摘要被简化
        """
        if len(self.search_history) <= keep_recent:
            return

        # 标记旧记录为已压缩
        for record in self.search_history[:-keep_recent]:
            if not record.compacted:
                record.compacted = True
                # 简化摘要，只保留关键数字
                record.hits_summary = f"命中{record.hits_count}条"

    def get_search_history_summary(self) -> str:
        """获取搜索历史摘要（用于 AI 决策）

        类似 OpenCode 的 toModelMessages，为 AI 构建可见的搜索历史
        """
        if not self.search_history:
            return ""

        lines = []

        # 1. 最近的详细展示（未压缩，最多 6 条）
        recent = [r for r in self.search_history if not r.compacted]
        if recent:
            lines.append("【近期搜索】")
            # 最后 6 条详细展示
            detailed = recent[-6:]
            for r in detailed:
                chapters_str = ""
                if r.chapters_covered:
                    if len(r.chapters_covered) == 1:
                        chapters_str = f" 第{r.chapters_covered[0]}章"
                    else:
                        chapters_str = f" 第{min(r.chapters_covered)}-{max(r.chapters_covered)}章"
                lines.append(f"  · {r.query}: {r.hits_summary}{chapters_str}")

            # 其他未压缩但未详细展示的记录，简化显示
            other_recent = recent[:-6] if len(recent) > 6 else []
            if other_recent:
                other_queries = [f"{r.query}({r.hits_count}条)" for r in other_recent]
                lines.append(f"  （另有 {len(other_recent)} 条：{', '.join(other_queries)}）")

        # 2. 旧记录的压缩展示（排除已穷尽的，避免重复显示）
        compacted = [r for r in self.search_history if r.compacted and not r.exhausted]
        if compacted:
            queries = [r.query for r in compacted]
            lines.append(f"【历史搜索】已搜过: {', '.join(queries)}")

        # 3. 已穷尽的关键词（特别标注）
        exhausted = [r for r in self.search_history if r.exhausted]
        if exhausted:
            exhausted_queries = [r.query for r in exhausted]
            lines.append(f"【已确认不存在】{', '.join(exhausted_queries)}（章节原文+世界观均无结果，无需再搜）")

        return "\n".join(lines)

    def should_block_search(self, keyword: str, scope: Optional[Tuple[int, int]]) -> Tuple[bool, str]:
        """判断是否应该拦截搜索

        Args:
            keyword: 搜索关键词（单个）
            scope: 当前搜索范围，None 表示全书

        Returns:
            (是否拦截, 拦截原因)
        """
        # 查找该关键词的搜索记录
        for record in self.search_history:
            # 检查关键词是否在记录的 query 中（支持多关键词组合）
            record_keywords = [kw.strip() for kw in record.query.split(",") if kw.strip()]
            if keyword not in record_keywords:
                continue
            # 多关键词组合 0 命中时，不拦截单个关键词（避免因组合/解析问题误判）
            if len(record_keywords) > 1 and record.hits_count == 0 and record.worldview_hits == 0:
                continue

            # 情况1: 已穷尽 → 拦截
            if record.exhausted:
                if self.has_full_scope_rewrite_proof(keyword):
                    return True, f"关键词'{keyword}'已确认不存在（章节原文+世界观均无结果）"
                return False, ""

            # 情况2: 相同范围 + 0 命中 → 拦截（换参数无意义）
            if record.hits_count == 0 and record.worldview_hits == 0 and record.chapter_scope == scope:
                scope_desc = f"第{scope[0]}-{scope[1]}章" if scope else "全书"
                return True, f"关键词'{keyword}'在{scope_desc}范围内已搜索过，0命中"

        return False, ""

    def get_search_record(self, keyword: str) -> Optional['SearchRecord']:
        """获取关键词的搜索记录"""
        for record in reversed(self.search_history):  # 从最新的开始找
            if record.query == keyword:
                return record
        return None

    def update_search_record_worldview(self, keyword: str, worldview_hits: int) -> None:
        """更新搜索记录的世界观检查状态"""
        record = self.get_search_record(keyword)
        if record:
            record.worldview_checked = True
            record.worldview_hits = worldview_hits


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
    return f"深度探索（{round_idx}）"


def _get_review_status(round_data: ExploreRound) -> str:
    """获取审查状态"""
    # 仅用于前端展示，不参与判停逻辑
    return ""


def _get_status_text(round_data: ExploreRound) -> str:
    """获取状态文本（灰色显示）"""
    # 仅用于前端展示，不参与判停逻辑
    return ""


def _scopes_cache_key(scopes: List[Tuple[int, int]]) -> str:
    if not scopes:
        return "all"
    return ",".join(f"{start}-{end}" for start, end in scopes)


def _build_explore_shared_key(
    work_id: str,
    user_id: Optional[str],
    conversation_id: Optional[str],
    chapter_scopes: List[Tuple[int, int]],
    target_task: Optional[str] = None
) -> str:
    work_id = str(work_id or "").strip()
    if not work_id:
        return ""
    user_part = str(user_id or "anonymous").strip() or "anonymous"
    convo_part = str(conversation_id or "default").strip() or "default"
    scope_part = _scopes_cache_key(chapter_scopes)
    task_text = (target_task or "").strip()
    task_part = hashlib.sha1(task_text.encode("utf-8")).hexdigest()[:8] if task_text else "none"
    return f"{work_id}:{user_part}:{convo_part}:{scope_part}:{task_part}"


def _normalize_search_keywords(keywords: Optional[List[str]]) -> List[str]:
    if not keywords:
        return []
    normalized = []
    for item in keywords:
        value = str(item).strip()
        if value:
            normalized.append(value)
    if not normalized:
        return []
    return sorted(set(normalized))


def _build_explore_result_cache_key(
    work_id: str,
    user_id: Optional[str],
    chapter_scopes: List[Tuple[int, int]],
    target_task: str,
    search_keywords: Optional[List[str]],
    output_mode: str,
    require_paragraph_index: Optional[bool] = None,
    force_global_search: Optional[bool] = None
) -> str:
    work_id = str(work_id or "").strip()
    if not work_id:
        return ""
    user_part = str(user_id or "anonymous").strip() or "anonymous"
    scope_part = _scopes_cache_key(chapter_scopes)
    payload = {
        "task": (target_task or "").strip(),
        "keywords": _normalize_search_keywords(search_keywords),
        "output_mode": (output_mode or "").strip().lower(),
        "require_paragraph_index": bool(require_paragraph_index) if require_paragraph_index is not None else None,
        "force_global_search": bool(force_global_search) if force_global_search is not None else None,
        "schema": EXPLORE_RESULT_CACHE_VERSION
    }
    digest = hashlib.sha1(
        json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    return f"explore:result:{EXPLORE_RESULT_CACHE_VERSION}:{work_id}:{user_part}:{scope_part}:{digest}"


async def _get_cached_explore_result(cache_key: str) -> Optional[Dict[str, Any]]:
    if not cache_key:
        return None
    try:
        cached = await RedisClient.get(cache_key)
    except Exception as e:
        logger.debug(f"[explore_content] Redis缓存读取失败: {e}")
        return None
    if not cached:
        return None
    if isinstance(cached, dict):
        return cached
    if isinstance(cached, str):
        try:
            return json.loads(cached)
        except Exception:
            return None
    return None


async def _set_cached_explore_result(cache_key: str, payload: Dict[str, Any]) -> None:
    if not cache_key:
        return
    try:
        serialized = json.dumps(payload, ensure_ascii=False)
        if len(serialized) > EXPLORE_RESULT_CACHE_MAX_CHARS:
            logger.info(
                "[explore_content] 缓存跳过：结果过大（%s chars > %s）",
                len(serialized),
                EXPLORE_RESULT_CACHE_MAX_CHARS
            )
            return
        await RedisClient.set(cache_key, payload, expire=EXPLORE_RESULT_CACHE_TTL_SECONDS)
    except Exception as e:
        logger.debug(f"[explore_content] Redis缓存写入失败: {e}")


def _decorate_cached_payload(payload: Dict[str, Any], cache_key: str) -> Dict[str, Any]:
    data = dict(payload)
    data["cache_hit"] = True
    data["cache_key"] = cache_key
    data["events_emitted"] = False
    return data


def _clone_explore_state(state: ExploreState) -> ExploreState:
    source_iteration_state = getattr(state, "iteration_state", None)
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
        context_coverage=dict(state.context_coverage),
        read_chapter_orders=set(state.read_chapter_orders),
        read_worldview_categories=set(),
        rounds=[],
        search_history=list(state.search_history),  # 保留搜索历史
        query_attempts=list(state.query_attempts),
        iteration_state=source_iteration_state.clone() if isinstance(source_iteration_state, IterationState) else IterationState(),
        latest_intent_spec=dict(getattr(state, "latest_intent_spec", {}) or {}),
        latest_query_program=dict(getattr(state, "latest_query_program", {}) or {}),
    )


def _merge_explore_states(base: ExploreState, incoming: ExploreState) -> ExploreState:
    merged = _clone_explore_state(base)
    merged.searched_queries |= incoming.searched_queries
    merged.read_paragraph_positions |= incoming.read_paragraph_positions
    merged.read_chapter_orders |= incoming.read_chapter_orders
    for key, value in incoming.context_coverage.items():
        if key not in merged.context_coverage:
            merged.context_coverage[key] = value
            continue
        prev_start, prev_end = merged.context_coverage[key]
        start_index, end_index = value
        merged.context_coverage[key] = (min(prev_start, start_index), max(prev_end, end_index))
    # 合并搜索历史（去重，基于 query）
    seen_queries = {r.query for r in merged.search_history}
    for record in incoming.search_history:
        if record.query not in seen_queries:
            merged.search_history.append(record)
            seen_queries.add(record.query)
    merged.query_attempts.extend(incoming.query_attempts)
    if len(merged.query_attempts) > 50:
        merged.query_attempts = merged.query_attempts[-50:]
    merged.iteration_state.merge_from(getattr(incoming, "iteration_state", None))
    incoming_intent = getattr(incoming, "latest_intent_spec", None)
    incoming_program = getattr(incoming, "latest_query_program", None)
    if incoming_intent:
        merged.latest_intent_spec = dict(incoming_intent)
    if incoming_program:
        merged.latest_query_program = dict(incoming_program)
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


def _extract_target_quotes(target_task: str) -> List[str]:
    if not isinstance(target_task, str) or not target_task.strip():
        return []
    segments: List[str] = []
    seen = set()
    for match in re.findall(r'["“”‘’「」『』《》](.+?)["“”‘’「」『』》]', target_task):
        seg = (match or "").strip()
        if not seg or len(seg) < 4:
            continue
        if seg in seen:
            continue
        segments.append(seg)
        seen.add(seg)
    return segments


def _normalize_keywords(keywords: Optional[List[str]]) -> List[str]:
    normalized: List[str] = []
    seen = set()
    for kw in (keywords or []):
        text = str(kw).strip()
        if not text:
            continue
        if text in seen:
            continue
        normalized.append(text)
        seen.add(text)
    return normalized


def _score_paragraph_target(
    text: str,
    quoted_segments: List[str],
    keywords: List[str]
) -> Tuple[int, int, int]:
    score = 0
    quote_hits = 0
    keyword_hits = 0
    if text:
        for seg in quoted_segments:
            if seg and seg in text:
                quote_hits += 1
                score += 5
        lowered = text.lower()
        for kw in keywords:
            if kw and kw.lower() in lowered:
                keyword_hits += 1
                score += 1
    return score, quote_hits, keyword_hits


def _select_unique_target_paragraphs(
    result: ExploreResult,
    target_task: str,
    search_keywords: Optional[List[str]]
) -> None:
    if not result or not result.paragraphs:
        return
    candidates = [
        p for p in result.paragraphs
        if getattr(p, "is_target", True) and isinstance(getattr(p, "text", ""), str)
    ]
    if len(candidates) <= 1:
        return
    quoted_segments = _extract_target_quotes(target_task)
    keywords = _normalize_keywords(search_keywords)
    scored = []
    for p in candidates:
        score, quote_hits, keyword_hits = _score_paragraph_target(p.text, quoted_segments, keywords)
        scored.append((score, quote_hits, keyword_hits, p))
    scored.sort(key=lambda item: (item[0], item[1], item[2]), reverse=True)
    top = scored[0]
    runner_up = scored[1] if len(scored) > 1 else None
    top_score, top_quotes, _, top_para = top
    strong = False
    if runner_up is None:
        strong = True
    else:
        second_score, second_quotes, _, _ = runner_up
        if top_score >= 6 and (top_score - second_score) >= 2:
            strong = True
        elif top_quotes > 0 and second_quotes == 0:
            strong = True
    if not strong:
        return
    for _, _, _, para in scored:
        para.is_target = para is top_para


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
        node_id: str = "",
        text: str = "",
        before_anchor: str = "",
        after_anchor: str = ""
    ) -> None:
        query_text = (query or "").strip()
        if not query_text or not chapter_id:
            return
        query_text = query_text[:200]
        key = (chapter_id, paragraph_index, query_text[:80])
        if key in seen:
            return
        seen.add(key)
        parts = [part for part in [before_anchor, text or query_text, after_anchor] if part]
        insert_context = "\n".join(parts) if parts else (text or query_text)
        if node_id:
            locator_seed = f"{chapter_id}:{node_id}"
        elif paragraph_index is not None:
            locator_seed = f"{chapter_id}:{paragraph_index}"
        else:
            locator_seed = f"{chapter_id}:{query_text[:80]}"
        locator_id = hashlib.md5(locator_seed.encode("utf-8")).hexdigest()
        targets.append({
            "chapter_id": chapter_id,
            "chapter_order": chapter_order,
            "query": query_text,
            "text": text or query_text,
            "paragraph_index": paragraph_index,
            "node_id": node_id or "",
            "locator_id": locator_id,
            "reason": reason,
            "before_anchor": before_anchor,
            "after_anchor": after_anchor,
            "insert_context": insert_context,
            "allow_global_fallback": False
        })

    # 优先使用已读取段落（原文）
    for p in result.paragraphs:
        if not getattr(p, "is_target", True):
            continue
        chapter_id = ""
        entry = chapters_by_order.get(p.chapter_order, {})
        if entry:
            chapter_id = entry.get("id") or entry.get("chapter_id") or ""
        before_anchor = ""
        after_anchor = ""
        if p.context_before:
            before_anchor = (p.context_before[-1] or "")[-50:]
        if p.context_after:
            after_anchor = (p.context_after[0] or "")[:50]
        _add_target(
            chapter_order=p.chapter_order,
            paragraph_index=p.paragraph_index,
            chapter_id=chapter_id,
            query=p.text,
            reason="已读取原文段落",
            node_id=p.node_id or node_id_map.get((p.chapter_order, p.paragraph_index), ""),
            text=p.text,
            before_anchor=before_anchor,
            after_anchor=after_anchor
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
        if tc.tool_name == "list_chapters":
            tags.append({
                "type": "ListChapters",
                "value": "列章节"
            })
        elif tc.tool_name == "list_paragraphs":
            tags.append({
                "type": "ListParagraphs",
                "value": "列段落预览"
            })
        elif tc.tool_name == "exact_search_paragraphs":
            # 关键词搜索
            keywords = tc.params.get("keywords", "")
            if isinstance(keywords, list):
                keywords = ", ".join(keywords[:3])
            elif isinstance(keywords, str) and "|" in keywords:
                keywords = ", ".join(keywords.split("|")[:3])
            label = (keywords or "").strip()
            if not label:
                label = "关键词搜索"

            tags.append({
                "type": "Search",
                "value": label[:30] + ("..." if len(label) > 30 else ""),
                "highlight": label[:30]
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
        elif tc.tool_name == "read_paragraphs":
            # 批量段落读取：显示读取数量
            items = tc.params.get("items", [])
            count = len(items) if isinstance(items, list) else 0
            if count > 0:
                first = items[0] if items else {}
                chapter = first.get("chapter_order", "?")
                tags.append({
                    "type": "ReadParagraph",
                    "value": f"第{chapter}章 · {count}段"
                })
            else:
                # 分页模式：chapter_order/chapter_id + offset/limit
                chapter = tc.params.get("chapter_order") or tc.params.get("chapter")
                if not chapter and isinstance(tc.result, dict):
                    chapter = tc.result.get("chapter_order") or tc.result.get("chapter")
                if isinstance(chapter, str) and chapter.isdigit():
                    chapter = int(chapter)

                offset = tc.params.get("offset")
                limit = tc.params.get("limit")
                if offset is None and isinstance(tc.result, dict):
                    offset = tc.result.get("offset")
                if limit is None and isinstance(tc.result, dict):
                    limit = tc.result.get("limit")
                if isinstance(offset, str) and offset.isdigit():
                    offset = int(offset)
                if isinstance(limit, str) and limit.isdigit():
                    limit = int(limit)

                range_label = "分页读取"
                if isinstance(limit, int) and limit > 0:
                    start = (offset if isinstance(offset, int) else 0) + 1
                    end = start + limit - 1
                    range_label = f"第{start}~{end}段" if end > start else f"第{start}段"

                if isinstance(chapter, int):
                    chapter_label = f"第{chapter}章"
                    value = f"{chapter_label} · {range_label}"
                else:
                    value = range_label

                tags.append({
                    "type": "ReadParagraph",
                    "value": value
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

    MAX_ROUNDS = 200  # 安全上限，防止死循环

    def __init__(
        self,
        work_id: str,
        target_task: str,
        max_rounds: int = 200,
        emit_callback: Optional[Callable[[dict], Awaitable[None]]] = None,
        step_id: Optional[int] = None,
        search_keywords: Optional[List[str]] = None,
        max_tool_calls: Optional[int] = None,
        max_read_paragraphs: Optional[int] = None,
        require_paragraph_index: Optional[bool] = None,
        force_global_search: Optional[bool] = None,
        user_id: Optional[str] = None
    ):
        """
        初始化内容探索器

        Args:
            work_id: 作品ID
            target_task: 目标任务描述
            max_rounds: 最大探索轮次（安全上限，AI 会自主决定何时停止）
            emit_callback: 事件发射回调
            step_id: 步骤ID
            search_keywords: 规划层提供的可选种子词（仅作辅助，不作为唯一检索来源）
        """
        self.work_id = work_id
        self.target_task = target_task
        self.search_keywords = _normalize_search_keywords(search_keywords)  # 规划层可选种子词
        self.user_id = user_id
        self.force_global_search = bool(force_global_search)
        self.chapter_scopes_raw = _parse_chapter_scopes(target_task)
        if self.force_global_search:
            self.chapter_scopes_raw = []
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
        if require_paragraph_index is not None:
            self.require_paragraph_index = bool(require_paragraph_index)
        self.max_rounds = min(max_rounds, self.MAX_ROUNDS)
        self.max_tool_calls = max_tool_calls if isinstance(max_tool_calls, int) and max_tool_calls > 0 else TOOL_LOOP_MAX_CALLS_DEFAULT
        self.max_read_paragraphs = (
            max_read_paragraphs if isinstance(max_read_paragraphs, int) and max_read_paragraphs > 0 else None
        )
        self.emit_callback = emit_callback
        if isinstance(step_id, int) and step_id > 0:
            self.step_id = step_id
        else:
            self.step_id = 1
        self.state = ExploreState()
        self.intent_retrieval_v2 = bool(getattr(settings, "EXPLORE_INTENT_RETRIEVAL_V2", True))
        self.intent_probe_override_mode = str(
            getattr(settings, "EXPLORE_PROBE_OVERRIDE_MODE", "suggest_only")
        ).strip().lower() or "suggest_only"
        if self.intent_probe_override_mode not in {"suggest_only", "force"}:
            self.intent_probe_override_mode = "suggest_only"
        self.intent_compiler = IntentCompiler()
        self.query_program_builder = QueryProgramBuilder()
        self.evidence_judge = EvidenceJudge()
        self.adaptive_controller = AdaptiveController()
        self.start_time = get_utc_now()
        self.chapter_list_cache: Optional[List[Dict[str, Any]]] = None
        self.paragraph_node_id_cache: Dict[int, Dict[str, int]] = {}
        self.paragraph_list_ranges: Dict[int, List[Tuple[int, int]]] = {}
        self.allowed_chapter_orders: List[int] = []
        self.chapter_paragraph_counts: Dict[int, int] = {}
        self.chapter_read_caps: Dict[int, int] = {}
        self.flow_listed_chapters = False
        self.flow_listed_paragraphs: set[int] = set()
        if self.require_paragraph_index:
            logger.info("[ContentExplorer] 启用严格段落号模式")
        if self.chapter_scopes_raw:
            logger.info("[ContentExplorer] 章节范围锁定: %s", _format_scope_ranges(self.chapter_scopes_raw))
        if self.force_global_search:
            logger.info("[ContentExplorer] force_global_search 启用：忽略章节范围")
        if self.intent_retrieval_v2:
            logger.info(
                "[ContentExplorer] 启用意图驱动词法检索 V3 (probe_override_mode=%s)",
                self.intent_probe_override_mode,
            )
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

    def _cache_paragraph_index_map(self, chapter_order: int, result_data: Dict[str, Any]) -> None:
        if not isinstance(chapter_order, int):
            return
        paragraphs = result_data.get("paragraphs") if isinstance(result_data, dict) else None
        if not isinstance(paragraphs, list):
            return
        total = result_data.get("total_paragraphs") if isinstance(result_data, dict) else None
        if isinstance(total, int) and total > 0:
            self.chapter_paragraph_counts[chapter_order] = total
            self.chapter_read_caps[chapter_order] = self._calc_read_cap(total)
        node_map = self.paragraph_node_id_cache.setdefault(chapter_order, {})
        for para in paragraphs:
            if not isinstance(para, dict):
                continue
            idx = para.get("paragraph_index")
            if idx is None:
                idx = para.get("index")
            if isinstance(idx, str) and idx.isdigit():
                idx = int(idx)
            node_id = para.get("node_id") or ""
            if isinstance(idx, int) and node_id and node_id not in node_map:
                node_map[node_id] = idx

    def _record_listed_paragraph_range(
        self,
        chapter_order: int,
        offset: Optional[int],
        limit: Optional[int],
        total: Optional[int],
        approximate: bool = False
    ) -> None:
        if approximate:
            return
        if not isinstance(chapter_order, int):
            return
        if not isinstance(offset, int):
            offset = 0
        if not isinstance(limit, int) or limit <= 0:
            return
        start = max(0, offset)
        end = start + limit - 1
        if isinstance(total, int) and total > 0:
            end = min(end, total - 1)
        ranges = self.paragraph_list_ranges.setdefault(chapter_order, [])
        # 避免重复记录完全覆盖的范围
        for existing_start, existing_end in ranges:
            if existing_start <= start and existing_end >= end:
                return
        ranges.append((start, end))

    def _is_paragraph_index_listed(self, chapter_order: int, paragraph_index: int) -> bool:
        ranges = self.paragraph_list_ranges.get(chapter_order)
        if not ranges:
            return False
        for start, end in ranges:
            if start <= paragraph_index <= end:
                return True
        return False

    def _calc_read_cap(self, total_paragraphs: Optional[int]) -> int:
        if not isinstance(total_paragraphs, int) or total_paragraphs <= 0:
            return PER_CHAPTER_READ_CAP_MIN
        cap = int((total_paragraphs * PER_CHAPTER_READ_CAP_RATIO) + 0.9999)
        if cap < PER_CHAPTER_READ_CAP_MIN:
            cap = PER_CHAPTER_READ_CAP_MIN
        if cap > PER_CHAPTER_READ_CAP_MAX:
            cap = PER_CHAPTER_READ_CAP_MAX
        return cap

    def _get_chapter_read_count(self, chapter_order: int) -> int:
        if not isinstance(chapter_order, int):
            return 0
        return sum(1 for ch, _ in self.state.read_paragraph_positions if ch == chapter_order)

    def _get_chapter_remaining_reads(self, chapter_order: int) -> Optional[int]:
        # Per-chapter read caps disabled: return None to indicate no limit.
        return None

    def _can_read_chapter(self, chapter_order: int, planned_reads: int = 1) -> bool:
        remaining = self._get_chapter_remaining_reads(chapter_order)
        if remaining is None:
            return True
        return remaining >= planned_reads

    async def _load_chapter_paragraph_counts(self, chapter_orders: List[int]) -> None:
        if not chapter_orders:
            return
        try:
            from uuid import UUID
            from sqlalchemy import select, func
            from app.models.novel_chapter_vector import NovelChapterVector
            work_uuid = UUID(self.work_id) if isinstance(self.work_id, str) else self.work_id
            stmt = select(
                NovelChapterVector.chapter_order,
                func.count(NovelChapterVector.id).label("count")
            ).where(
                NovelChapterVector.work_id == work_uuid,
                NovelChapterVector.chapter_order.in_(chapter_orders)
            ).group_by(NovelChapterVector.chapter_order)
            async with AsyncSessionLocal() as db:
                result = await db.execute(stmt)
            for row in result.all():
                order = row[0]
                count = row[1]
                if isinstance(order, int) and isinstance(count, int) and count > 0:
                    self.chapter_paragraph_counts[order] = count
        except Exception as e:
            logger.warning(f"[ContentExplorer] 获取段落数失败: {e}")

    async def _init_chapter_read_caps(self, chapter_orders: List[int]) -> None:
        if not chapter_orders:
            return
        await self._load_chapter_paragraph_counts(chapter_orders)
        for order in chapter_orders:
            if order in self.chapter_read_caps:
                continue
            total = self.chapter_paragraph_counts.get(order)
            self.chapter_read_caps[order] = self._calc_read_cap(total)

    async def _get_allowed_chapter_orders(self) -> List[int]:
        await self._ensure_scope_mapping()
        chapters = await self._get_chapter_list()
        orders = [ch.get("order") for ch in chapters if isinstance(ch.get("order"), int)]
        if self.chapter_scopes:
            orders = [order for order in orders if self._is_chapter_in_scope(order)]
        return orders

    def _split_search_terms(self, text: str) -> List[str]:
        if not isinstance(text, str):
            return []
        parts = re.split(r"[,\s，。；;：:、|｜/]+", text)
        terms: List[str] = []
        seen = set()
        for raw in parts:
            value = raw.strip().strip("\"'“”‘’《》()[]{}")
            if not value or len(value) < 2:
                continue
            if value in seen:
                continue
            seen.add(value)
            terms.append(value)
        return terms

    def _parse_search_term_values(self, raw: Any) -> List[str]:
        terms: List[str] = []
        if isinstance(raw, str):
            terms.extend(self._split_search_terms(raw))
        elif isinstance(raw, list):
            for item in raw:
                terms.extend(self._split_search_terms(str(item)))
        elif raw is not None:
            terms.extend(self._split_search_terms(str(raw)))
        deduped: List[str] = []
        seen = set()
        for term in terms:
            value = str(term).strip().strip("\"'“”‘’《》")
            if not value:
                continue
            key = value.lower()
            if key in seen:
                continue
            seen.add(key)
            deduped.append(value)
        return deduped

    def _get_latest_exact_search_result(self) -> Dict[str, Any]:
        for round_data in reversed(self.state.rounds):
            for call in reversed(round_data.tool_calls):
                if call.tool_name != "exact_search_paragraphs":
                    continue
                if isinstance(call.result, dict):
                    return call.result
        return {}

    def _build_forced_rewrite_search_args(self) -> Optional[Dict[str, Any]]:
        """构造程序强制放宽查询参数（关键词模式），避免 0 命中空转。"""
        recent_attempts = self.state.get_recent_query_attempts(limit=5)
        latest_attempt = recent_attempts[-1] if recent_attempts else None

        latest_result = self._get_latest_exact_search_result()
        failure_reason = ""
        if isinstance(latest_result, dict):
            adaptive_overrides = latest_result.get("adaptive_overrides")
            if isinstance(adaptive_overrides, dict) and adaptive_overrides.get("keywords"):
                logger.info(
                    "[ContentExplorer] reuse adaptive overrides from latest result: strategy=%s",
                    adaptive_overrides.get("strategy")
                )
                return dict(adaptive_overrides)
            judge = latest_result.get("judge")
            if isinstance(judge, dict):
                failure_reason = str(judge.get("failure_reason") or "").strip()
            if not failure_reason:
                failure_reason = str(latest_result.get("failure_reason") or "").strip()
            if not failure_reason and not latest_result.get("success"):
                failure_reason = str(latest_result.get("error") or "").strip() or "lexical_miss"

        keywords: List[str] = []
        chapter_scope = None
        if latest_attempt:
            keywords.extend([kw for kw in latest_attempt.keywords if kw])
            chapter_scope = latest_attempt.chapter_scope

        if not keywords:
            keywords.extend(_normalize_search_keywords(self.search_keywords))

        if not keywords:
            quotes = _extract_target_quotes(self.target_task or "")
            for quote in quotes:
                keywords.extend(self._split_search_terms(quote))

        keywords = self.intent_compiler.sanitize_external_keywords(
            keywords,
            self.target_task or "",
            limit=6,
        )

        latest_terms_required = self._parse_search_term_values(latest_result.get("terms_required") if isinstance(latest_result, dict) else [])
        latest_terms_optional = self._parse_search_term_values(latest_result.get("terms_optional") if isinstance(latest_result, dict) else [])
        latest_terms_excluded = self._parse_search_term_values(latest_result.get("terms_excluded") if isinstance(latest_result, dict) else [])
        latest_proximity_terms = self._parse_search_term_values(latest_result.get("proximity_terms") if isinstance(latest_result, dict) else [])
        if not latest_proximity_terms and len(keywords) >= 2:
            latest_proximity_terms = keywords[:2]

        if self.intent_retrieval_v2 and (keywords or self.state.latest_intent_spec):
            adaptive_rewrite = self.adaptive_controller.build_rewrite(
                failure_reason=failure_reason or "lexical_miss",
                target_task=self.target_task or "",
                intent_spec=self.state.latest_intent_spec if isinstance(self.state.latest_intent_spec, dict) else {},
                iteration_state=self.state.iteration_state.to_dict(),
                latest_keywords=keywords,
                latest_terms_required=latest_terms_required,
                latest_terms_optional=latest_terms_optional,
                latest_terms_excluded=latest_terms_excluded,
                latest_proximity_terms=latest_proximity_terms,
                latest_scope=chapter_scope,
                seed_keywords=self.search_keywords or [],
            )
            if adaptive_rewrite:
                adaptive_args = adaptive_rewrite.to_search_args()
                logger.info(
                    "[ContentExplorer] adaptive rewrite generated: strategy=%s reason=%s keywords=%s",
                    adaptive_args.get("strategy"),
                    adaptive_args.get("adaptive_reason"),
                    adaptive_args.get("keywords"),
                )
                return adaptive_args

        if not keywords:
            return None

        args: Dict[str, Any] = {
            "keywords": keywords or None,
            "match_mode": "any",
            "limit": 100,
            "strategy": "forced_rewrite",
            "search_intent": "放宽关键词约束，确认是否存在相关段落",
        }
        if chapter_scope and isinstance(chapter_scope, tuple):
            args["chapter_range"] = [chapter_scope[0], chapter_scope[1]]
        return args

    def _collect_recent_attempt_keywords(self, limit: int = 16) -> List[str]:
        if limit <= 0:
            return []
        recent_attempts = self.state.get_recent_query_attempts(limit=max(limit * 2, 12))
        keywords: List[str] = []
        seen = set()
        fallback_pool: List[str] = []
        for attempt in recent_attempts:
            attempt_keywords = self.intent_compiler.sanitize_external_keywords(
                list(attempt.keywords or []),
                self.target_task or "",
                limit=6,
            )
            if int(attempt.chapter_hits or 0) <= 0:
                fallback_pool.extend(attempt_keywords[:2])
                continue
            for kw in attempt_keywords:
                value = str(kw or "").strip()
                if not value or value in seen:
                    continue
                seen.add(value)
                keywords.append(value)
                if len(keywords) >= limit:
                    return keywords
        if keywords:
            return keywords

        for kw in fallback_pool:
            value = str(kw or "").strip()
            if not value or value in seen:
                continue
            seen.add(value)
            keywords.append(value)
            if len(keywords) >= limit:
                break
        return keywords

    def _compile_intent_spec(
        self,
        manual_keywords: List[str],
        current_scope: Optional[Tuple[int, int]]
    ) -> IntentSpec:
        scope = current_scope
        if scope is None and self.chapter_scopes:
            min_order = min(item[0] for item in self.chapter_scopes)
            max_order = max(item[1] for item in self.chapter_scopes)
            scope = (min_order, max_order)
        seed_keywords = []
        seed_keywords.extend(self.search_keywords or [])
        seed_keywords.extend(manual_keywords or [])
        recent_keywords = self._collect_recent_attempt_keywords(limit=20)
        intent_spec = self.intent_compiler.compile(
            target_task=self.target_task or "",
            seed_keywords=seed_keywords,
            recent_keywords=recent_keywords,
            chapter_scope=scope
        )
        self.state.latest_intent_spec = intent_spec.to_dict()
        return intent_spec

    def _plan_exact_search_probe(
        self,
        manual_keywords: List[str],
        requested_match_mode: str,
        current_scope: Optional[Tuple[int, int]],
        limit: int
    ) -> Tuple[Optional[Dict[str, Any]], Optional[IntentSpec], Optional[Dict[str, Any]]]:
        if not self.intent_retrieval_v2:
            return None, None, None

        intent_spec = self._compile_intent_spec(
            manual_keywords=manual_keywords,
            current_scope=current_scope
        )
        query_program = self.query_program_builder.build(
            intent=intent_spec,
            manual_keywords=manual_keywords,
            requested_match_mode=requested_match_mode,
            chapter_scope=current_scope,
            iteration_state=self.state.iteration_state,
            max_probes=INTENT_RETRIEVAL_MAX_PROBES,
        )
        query_program_dict = query_program.to_dict()
        self.state.latest_query_program = query_program_dict
        probe = self.query_program_builder.pick_next_probe(
            program=query_program,
            iteration_state=self.state.iteration_state
        )
        if probe is None:
            return None, intent_spec, query_program_dict

        payload = self.query_program_builder.probe_to_search_payload(
            probe=probe,
            limit=limit
        )
        return {"probe": probe, "payload": payload}, intent_spec, query_program_dict

    def _has_unread_locatable_search_hits(self) -> bool:
        """是否存在“可定位且未读取”的章节候选命中。"""
        for hit in self.state.search_hits:
            if getattr(hit, "source_type", "") == "worldview":
                continue
            chapter_order = getattr(hit, "chapter_order", None)
            paragraph_index = getattr(hit, "paragraph_index", None)
            if not isinstance(chapter_order, int) or not isinstance(paragraph_index, int):
                continue
            if self.chapter_scopes and not self._is_chapter_in_scope(chapter_order):
                continue
            if self.state.should_read_paragraph(chapter_order, paragraph_index):
                return True
        return False

    def _evaluate_stop_quality_gate(self, stop_reason: str) -> Tuple[bool, str]:
        """程序化停机门槛：不把停机完全交给 AI。"""
        query_attempts = self.state.count_query_attempts()
        if query_attempts < 1:
            return False, "尚未执行有效查询，禁止停止"

        has_read_attempt = bool(self.state.read_paragraph_positions)
        has_locatable_search_hits = self._has_unread_locatable_search_hits()
        if has_locatable_search_hits and not has_read_attempt:
            return False, "已有候选命中但未读取原文，禁止停止"

        lower_reason = (stop_reason or "").lower()
        non_existent_hint = any(token in lower_reason for token in ("不存在", "无法找到", "无证据", "not found"))
        if non_existent_hint:
            target_scope: Optional[Tuple[int, int]] = None
            if self.chapter_scopes:
                min_order = min(scope[0] for scope in self.chapter_scopes)
                max_order = max(scope[1] for scope in self.chapter_scopes)
                target_scope = (min_order, max_order)

            full_scope_zero_strategies = set()
            for attempt in self.state.query_attempts:
                attempt_scope = attempt.chapter_scope
                if target_scope is None:
                    if attempt_scope is not None:
                        continue
                elif attempt_scope != target_scope:
                    continue
                if int(attempt.chapter_hits or 0) != 0:
                    continue
                # 严格段落模式下仅以“章节命中”判断，不让 worldview 命中阻塞停机。
                if not self.require_paragraph_index and int(attempt.worldview_hits or 0) != 0:
                    continue
                full_scope_zero_strategies.add(attempt.strategy or "ai")
            min_strategies = ZERO_HIT_NON_EXISTENT_MIN_STRATEGIES
            if self.require_paragraph_index or target_scope is not None:
                min_strategies = 2
            if len(full_scope_zero_strategies) < min_strategies:
                scope_label = "全局" if target_scope is None else f"范围{target_scope[0]}-{target_scope[1]}"
                return False, f"不存在结论证据不足（{scope_label}0命中策略不足）"

        return True, ""

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
            # 世界观结果不受章节范围限制
            if item.get("source") == "worldview":
                filtered.append(item)
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

    async def explore_tool_loop(self) -> ExploreResult:
        """执行探索（opencode 风格：LLM 工具调用循环）"""
        logger.info(f"[ContentExplorer] 开始探索 V5: work_id={self.work_id}, target={self.target_task[:50]}...")

        stop_reason = "达到工具调用上限"
        tool_calls_left = self.max_tool_calls
        reads_left = self.max_read_paragraphs
        last_tool_name = ""
        last_tool_result = ""
        round_idx = 0
        repeated_call_streak = 0
        last_tool_signature = ""
        consecutive_zero_hit_searches = 0
        forced_rewrite_used = 0
        prevented_stop_count = 0
        no_progress_rounds = 0

        def _build_tool_signature(tool_call: ToolCall) -> str:
            tool_params = {
                key: value
                for key, value in (tool_call.params or {}).items()
                if key != "work_id" and key not in TOOL_SIGNATURE_NOISE_PARAMS
            }
            if isinstance(tool_params.get("keywords"), list):
                normalized = _normalize_search_keywords([str(v) for v in tool_params.get("keywords") or []])
                tool_params["keywords"] = normalized
            for term_key in ("terms_required", "terms_optional", "terms_excluded", "proximity_terms"):
                if isinstance(tool_params.get(term_key), list):
                    normalized_terms = _normalize_search_keywords([str(v) for v in tool_params.get(term_key) or []])
                    tool_params[term_key] = normalized_terms
            if isinstance(tool_params.get("chapter_ranges"), list):
                ranges = []
                for item in tool_params.get("chapter_ranges") or []:
                    if isinstance(item, (list, tuple)) and len(item) >= 2:
                        try:
                            start = int(item[0])
                            end = int(item[1])
                        except Exception:
                            continue
                        if start > end:
                            start, end = end, start
                        ranges.append((start, end))
                if ranges:
                    tool_params["chapter_ranges"] = sorted(ranges)
            try:
                params_digest = json.dumps(tool_params, ensure_ascii=False, sort_keys=True)
            except Exception:
                params_digest = str(tool_params)
            return f"{tool_call.tool_name}:{params_digest}"

        # 范围预检查
        allowed_orders = await self._get_allowed_chapter_orders()
        self.allowed_chapter_orders = allowed_orders
        await self._init_chapter_read_caps(allowed_orders)
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
            # 不再发射探索总结事件（避免前端冗余模块）
            return result

        # 首轮自动获取世界观（按需小包，不受章节范围限制）
        if self.state.should_read_worldview("all"):
            try:
                from app.services.agent.langgraph_tools import get_worldview_pack
                logger.info("[ContentExplorer] 自动获取世界观小包...")
                keywords = self.search_keywords or []
                keywords = _normalize_search_keywords(keywords)
                chapter_orders = ""
                if self.chapter_scopes:
                    parts = []
                    for start, end in self.chapter_scopes:
                        if start == end:
                            parts.append(str(start))
                        else:
                            parts.append(f"{start}-{end}")
                    chapter_orders = ",".join(parts)
                wv_result = await get_worldview_pack.ainvoke({
                    "work_id": self.work_id,
                    "user_id": self.user_id or "",
                    "keywords": keywords,
                    "top_k": 5,
                    "include_guidelines": True,
                    "task_hint": self.target_task or "",
                    "chapter_orders": chapter_orders
                })
                wv_data = json.loads(wv_result) if isinstance(wv_result, str) else wv_result
                for cat in ("characters", "locations", "settings", "glossary"):
                    items = wv_data.get(cat)
                    if isinstance(items, list) and items:
                        self.state.add_worldview_items(items, cat)
                self.state.record_worldview_read("all")
                wv_count = sum(len(items) for items in self.state.worldview.values())
                logger.info(f"[ContentExplorer] 世界观小包获取完成: {wv_count} 条")
            except Exception as e:
                logger.warning(f"[ContentExplorer] 获取世界观小包失败: {e}")

        while tool_calls_left > 0 and round_idx < self.max_rounds:
            decision: Optional[ToolLoopDecision] = None
            if not self.flow_listed_chapters:
                reason = await self._ai_generate_forced_reason("list_chapters", {})
                decision = ToolLoopDecision(
                    action="tool",
                    tool="list_chapters",
                    args={},
                    reason=reason
                )
            elif not self.flow_listed_paragraphs:
                chapter_order = None
                if self.chapter_scopes:
                    chapter_order = self.chapter_scopes[0][0]
                else:
                    chapters = await self._get_chapter_list()
                    if chapters:
                        chapter_order = chapters[0].get("order")
                if isinstance(chapter_order, int):
                    chapter_order = self._map_title_order_if_needed(chapter_order)
                    reason = await self._ai_generate_forced_reason(
                        "list_paragraphs",
                        {
                            "chapter_order": chapter_order,
                            "offset": 0,
                            "limit": 50,
                            "preview_len": 80
                        }
                    )
                    decision = ToolLoopDecision(
                        action="tool",
                        tool="list_paragraphs",
                        args={
                            "chapter_order": chapter_order,
                            "offset": 0,
                            "limit": 50,
                            "preview_len": 80
                        },
                        reason=reason
                    )
            elif (
                consecutive_zero_hit_searches >= ZERO_HIT_FORCE_REWRITE_THRESHOLD
                and forced_rewrite_used < FORCED_REWRITE_MAX_ROUNDS
            ):
                forced_args = self._build_forced_rewrite_search_args()
                if forced_args:
                    forced_rewrite_used += 1
                    reason = (
                        f"连续{ZERO_HIT_FORCE_REWRITE_THRESHOLD}轮0命中，"
                        "程序触发放宽检索策略"
                    )
                    decision = ToolLoopDecision(
                        action="tool",
                        tool="exact_search_paragraphs",
                        args=forced_args,
                        reason=reason
                    )
                    logger.info("[ContentExplorer] 触发程序化改写检索: %s", forced_args)
                    consecutive_zero_hit_searches = 0

            if decision:
                logger.info("[ContentExplorer] 强制流程步骤: %s", decision.tool)
            else:
                decision = await self._ai_tool_loop_decide(
                    round_idx=round_idx + 1,
                    last_tool_name=last_tool_name,
                    last_tool_result=last_tool_result,
                    tool_calls_left=tool_calls_left,
                    reads_left=reads_left
                )
            if decision.action == "stop":
                can_stop, gate_reason = self._evaluate_stop_quality_gate(decision.reason or "")
                if can_stop:
                    stop_reason = decision.reason or "LLM 停止"
                    break

                prevented_stop_count += 1
                logger.info("[ContentExplorer] 停机门槛拦截: reason=%s", gate_reason)
                if forced_rewrite_used < FORCED_REWRITE_MAX_ROUNDS:
                    forced_args = self._build_forced_rewrite_search_args()
                    if forced_args:
                        forced_rewrite_used += 1
                        decision = ToolLoopDecision(
                            action="tool",
                            tool="exact_search_paragraphs",
                            args=forced_args,
                            reason=f"停机门槛未满足，程序触发改写检索：{gate_reason}"
                        )
                        logger.info("[ContentExplorer] 停机拦截后触发改写检索: %s", forced_args)
                    else:
                        last_tool_result = f"程序拒绝停止：{gate_reason}"
                        if prevented_stop_count >= 2:
                            stop_reason = f"停机被拒绝且无法构造新查询: {gate_reason}"
                            break
                        continue
                else:
                    last_tool_result = f"程序拒绝停止：{gate_reason}"
                    if prevented_stop_count >= 2:
                        stop_reason = f"停机被拒绝: {gate_reason}"
                        break
                    continue

            if decision.tool not in TOOL_LOOP_ALLOWED_TOOLS:
                stop_reason = f"不支持的工具: {decision.tool}"
                break

            before_evidences = len(self.state.evidences)
            before_paragraphs = len(self.state.paragraphs)
            before_search_hits = len(self.state.search_hits)

            tool_call, result_preview, reads_used = await self._execute_tool_action(
                decision.tool,
                decision.args,
                round_idx + 1,
                reads_left
            )

            tool_calls_left -= 1
            if reads_left is not None:
                reads_left = max(0, reads_left - reads_used)

            new_evidences = len(self.state.evidences) - before_evidences
            new_paragraphs = len(self.state.paragraphs) - before_paragraphs
            new_search_hits = len(self.state.search_hits) - before_search_hits

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

            if tool_call.tool_name == "exact_search_paragraphs":
                result_obj = tool_call.result if isinstance(tool_call.result, dict) else {}
                chapter_hits = result_obj.get("chapter_hits", result_obj.get("hits", 0))
                worldview_hits = result_obj.get("worldview_hits", 0)
                zero_hit_for_loop = (
                    int(chapter_hits or 0) == 0
                    and (self.require_paragraph_index or int(worldview_hits or 0) == 0)
                )
                if bool(result_obj.get("success")) and zero_hit_for_loop:
                    consecutive_zero_hit_searches += 1
                else:
                    consecutive_zero_hit_searches = 0
            elif tool_call.tool_name in ("read_paragraph", "read_paragraphs"):
                if new_evidences > 0 or new_paragraphs > 0:
                    consecutive_zero_hit_searches = 0

            if new_evidences > 0 or new_paragraphs > 0 or new_search_hits > 0:
                no_progress_rounds = 0
            else:
                no_progress_rounds += 1

            current_signature = _build_tool_signature(tool_call)
            if current_signature and current_signature == last_tool_signature:
                repeated_call_streak += 1
            else:
                repeated_call_streak = 1 if current_signature else 0
            last_tool_signature = current_signature

            if repeated_call_streak >= TOOL_LOOP_REPEAT_SIGNATURE_THRESHOLD:
                if tool_call.tool_name == "exact_search_paragraphs" and forced_rewrite_used < FORCED_REWRITE_MAX_ROUNDS:
                    forced_args = self._build_forced_rewrite_search_args()
                    if forced_args:
                        forced_rewrite_used += 1
                        repeated_call_streak = 0
                        last_tool_signature = ""
                        last_tool_result = "程序检测到重复查询，下一轮将强制改写参数"
                        logger.info("[ContentExplorer] 重复查询防打转触发改写: %s", forced_args)
                        continue
                stop_reason = f"连续{TOOL_LOOP_REPEAT_SIGNATURE_THRESHOLD}轮重复同一工具调用，停止探索"
                break

            if no_progress_rounds >= NO_PROGRESS_STOP_MIN_ROUNDS:
                stop_reason = f"连续{NO_PROGRESS_STOP_MIN_ROUNDS}轮无新增信息，停止探索"
                break

        if round_idx >= self.max_rounds and tool_calls_left > 0 and stop_reason == "达到工具调用上限":
            stop_reason = f"达到最大轮次上限({self.max_rounds})"

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

        # 不再发射探索总结事件（避免前端冗余模块）

        logger.info(f"[ContentExplorer] 探索完成(工具循环): {len(self.state.rounds)}轮, 原因={stop_reason}")
        return result

    # ==================== LLM 自检 ====================

    def _build_tool_loop_summary(
        self,
        last_tool_name: str,
        last_tool_result: str,
        tool_calls_left: int,
        reads_left: Optional[int]
    ) -> str:
        lines = []
        if self.chapter_scopes:
            lines.append(f"- 任务章节范围：{_format_scope_ranges(self.chapter_scopes)}")
        reads_desc = "不限" if reads_left is None else str(reads_left)
        lines.append(f"- 工具调用剩余：{tool_calls_left}，可读段落剩余：{reads_desc}")
        if self.chapter_read_caps and self.allowed_chapter_orders:
            budget_parts = []
            for order in self.allowed_chapter_orders[:10]:
                cap = self.chapter_read_caps.get(order)
                if not isinstance(cap, int):
                    continue
                used = self._get_chapter_read_count(order)
                budget_parts.append(f"第{order}章 {used}/{cap}")
            if budget_parts:
                lines.append(f"- 各章读取进度（已读/上限）：{'; '.join(budget_parts)}")

        # 优先展示搜索历史摘要（核心改进：类似 OpenCode 的 toModelMessages）
        search_summary = self.state.get_search_history_summary()
        if search_summary:
            lines.append(f"- 搜索历史：\n{search_summary}")
        elif self.state.searched_queries:
            # 兼容旧逻辑：如果没有搜索历史，显示已搜索词
            all_queries = list(self.state.searched_queries)
            lines.append(f"- 已搜索关键词（{len(all_queries)}个）：{', '.join(all_queries)}")

        recent_attempts = self.state.get_recent_query_attempts(limit=5)
        if recent_attempts:
            lines.append("- 最近查询策略：")
            for attempt in recent_attempts:
                scope_text = "全书" if attempt.chapter_scope is None else f"第{attempt.chapter_scope[0]}-{attempt.chapter_scope[1]}章"
                kw_text = ",".join(attempt.keywords[:4]) if attempt.keywords else "-"
                probe_text = attempt.probe_signature[:8] if attempt.probe_signature else "-"
                if attempt.error:
                    lines.append(
                        f"  · R{attempt.round_idx} [{attempt.strategy}] {scope_text} kw={kw_text} probe={probe_text} -> error:{attempt.error}"
                    )
                else:
                    lines.append(
                        f"  · R{attempt.round_idx} [{attempt.strategy}] {scope_text} kw={kw_text} probe={probe_text} -> hit={attempt.chapter_hits}/{attempt.hits}"
                    )

        if self.intent_retrieval_v2 and self.state.latest_intent_spec:
            intent_goal = (self.state.latest_intent_spec.get("goal") or "").strip()
            must_have = self.state.latest_intent_spec.get("must_have") or []
            if intent_goal:
                lines.append(f"- 当前检索意图：{_truncate_text(intent_goal, 120)}")
            if must_have:
                lines.append(f"- must_have 目标：{', '.join(must_have[:6])}")
            covered = sorted(self.state.iteration_state.covered_must_have_set)
            total_must_have = int(self.state.iteration_state.must_have_total or len(must_have) or 0)
            if total_must_have > 0:
                ratio = len(covered) / total_must_have
                lines.append(
                    f"- must_have 覆盖：{len(covered)}/{total_must_have} ({ratio:.0%})"
                )
            if covered:
                lines.append(f"- 已覆盖要素：{', '.join(covered[:8])}")
            if self.state.iteration_state.failed_reason_histogram:
                failure_parts = [
                    f"{key}:{value}"
                    for key, value in sorted(self.state.iteration_state.failed_reason_histogram.items())
                ]
                lines.append(f"- 失败原因分布：{'; '.join(failure_parts)}")

        # 最近一次搜索命中列表（对标 grep 输出：命中行列表）
        if self.state.search_hits:
            latest_query = None
            if self.state.search_history:
                latest_query = self.state.search_history[-1].query
            recent_hits: List[Evidence] = []
            if latest_query:
                recent_hits = [hit for hit in self.state.search_hits if hit.query == latest_query]
            if not recent_hits:
                latest_round = 0
                for hit in self.state.search_hits:
                    if isinstance(hit.round_idx, int) and hit.round_idx > latest_round:
                        latest_round = hit.round_idx
                recent_hits = [
                    hit for hit in self.state.search_hits
                    if not latest_round or hit.round_idx == latest_round
                ]
                label = f"第{latest_round}轮" if latest_round else "最近"
            else:
                label = f"关键词:{latest_query}"

            def _hit_score(item: Evidence) -> float:
                sim = item.similarity
                return float(sim) if isinstance(sim, (int, float)) else 0.0

            preview_hits = sorted(recent_hits, key=_hit_score, reverse=True)
            total_hits = len(preview_hits)
            preview_hits = preview_hits[:SEARCH_HIT_PREVIEW_LIMIT]
            lines.append(
                f"- 搜索命中列表（{label}，{total_hits}条，展示{len(preview_hits)}条）："
            )

            used_chars = 0
            shown = 0
            for hit in preview_hits:
                chapter_label = ""
                if isinstance(hit.chapter_order, int) and hit.chapter_order > 0:
                    chapter_label = f"第{hit.chapter_order}章"
                para_label = f"第{hit.paragraph_index}段" if isinstance(hit.paragraph_index, int) else ""
                if chapter_label:
                    location = f"{chapter_label}{para_label}"
                elif para_label:
                    location = para_label
                else:
                    location = hit.source_type or "search"
                meta_parts = []
                if hit.chapter_id:
                    meta_parts.append(f"chapter_id={hit.chapter_id}")
                if hit.node_id:
                    meta_parts.append(f"node_id={hit.node_id}")
                if not isinstance(hit.paragraph_index, int) and (hit.chapter_order or hit.chapter_id):
                    meta_parts.append("无段落号，先 list_paragraphs")
                if meta_parts:
                    location = f"{location} | " + " | ".join(meta_parts)
                text = (hit.text or "")[:SEARCH_HIT_TEXT_LIMIT]
                entry = f"  · [{location}] {text}"
                if shown >= SEARCH_HIT_MIN_ITEMS and used_chars + len(entry) > SEARCH_HIT_TOTAL_CHAR_LIMIT:
                    break
                lines.append(entry)
                used_chars += len(entry)
                shown += 1

            omitted = total_hits - shown
            if omitted > 0:
                lines.append(f"  （另有 {omitted} 条命中已省略）")

        # 已收集证据原文（让 AI 看到完整内容，判断是否符合预期）
        # 类似 OpenCode 的 toModelMessages：完整返回，超过上限再压缩旧的
        if self.state.evidences:
            EVIDENCE_PROTECT_CHARS = 8000  # 保护最近 8000 字符的证据原文
            evidence_lines = []
            total_chars = 0
            # 从最新的开始，保留完整原文
            for e in reversed(self.state.evidences):
                para_label = f"第{e.paragraph_index}段" if isinstance(e.paragraph_index, int) else ""
                entry = f"  · [第{e.chapter_order}章{para_label}] {e.text}"
                total_chars += len(entry)
                if total_chars >= EVIDENCE_PROTECT_CHARS:
                    remaining = len(self.state.evidences) - len(evidence_lines) - 1
                    if remaining > 0:
                        evidence_lines.append(f"  （另有 {remaining} 条旧证据已省略）")
                    break
                evidence_lines.append(entry)
            evidence_lines.reverse()
            lines.append(f"- 已收集证据（{len(self.state.evidences)}条）：")
            lines.extend(evidence_lines)

        # 已读段落位置（避免 AI 重复读取）
        if self.state.read_paragraph_positions:
            read_positions = sorted(self.state.read_paragraph_positions)
            chapter_reads: Dict[int, List[int]] = {}
            for ch, pi in read_positions:
                if ch not in chapter_reads:
                    chapter_reads[ch] = []
                chapter_reads[ch].append(pi)
            read_parts = []
            for ch in sorted(chapter_reads.keys()):
                paragraphs = chapter_reads[ch]
                if len(paragraphs) <= 5:
                    part = f"第{ch}章: 段落{','.join(map(str, paragraphs))}"
                else:
                    part = f"第{ch}章: 段落{min(paragraphs)}-{max(paragraphs)}（共{len(paragraphs)}段）"
                read_parts.append(part)
            lines.append(f"- 已读段落（{len(read_positions)}个，勿重复读取）：{'; '.join(read_parts)}")

        # 已覆盖的上下文范围（明确告诉 AI 无需重复读取）
        if self.state.context_coverage:
            coverage_parts = []
            for (chapter_order, target_index), (start_index, end_index) in sorted(
                self.state.context_coverage.items(),
                key=lambda item: (item[0][0], item[0][1])
            ):
                if start_index == end_index:
                    range_label = f"{start_index}"
                else:
                    range_label = f"{start_index}-{end_index}"
                coverage_parts.append(
                    f"第{chapter_order}章 目标段{target_index} 已覆盖段落{range_label}"
                )
            lines.append(f"- 上下文已覆盖（无需重复读取）：{'; '.join(coverage_parts)}")

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
        reads_left: Optional[int]
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

        # 🔧 2026-01-28: 隐藏 work_id 参数，由代码自动注入，避免 AI 误将参数名当作值
        tools_desc = """可用工具（只读）：
1) list_chapters()
   - 作用：列出章节清单
2) list_paragraphs(chapter_order, offset, limit, preview_len)
   - 作用：列出某章段落索引（仅预览）
3) exact_search_paragraphs(search_intent?, keywords?, terms_required?, terms_optional?, terms_excluded?, proximity_terms?, proximity_window?, match_mode, limit)
   - 作用：词法检索（Grep），优先传结构化参数（keywords + terms_* + proximity_*）
4) read_paragraph(chapter_order, paragraph_index, context_before, context_after)
   - 作用：读取指定段落原文
5) read_paragraphs(items, context_before, context_after)
   - 作用：批量读取多个段落原文（items 模式）
   - 或：read_paragraphs(chapter_order/chapter_id, offset, limit, context_before, context_after) 分页读取范围段落

禁止使用 search_content（语义检索）。
"""

        prompt = f"""你是只读探索器，只能在限定工具内选择下一步行动。

目标任务：{self.target_task}
当前轮次：第 {round_idx} 轮

当前状态：
{summary}

{tools_desc}

固定流程（尽量遵守）：
1) list_chapters → 2) list_paragraphs → 3) exact_search_paragraphs → 4) read_paragraph/read_paragraphs
说明：只有在已经明确范围或已知段落时，才允许跳过前面的步骤。

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
- read_paragraph 必须提供 chapter_order + paragraph_index（可用 list_paragraphs 的 index/paragraph_index）。
- read_paragraphs 可用两种模式：items 列表（chapter_order+paragraph_index）或分页模式（chapter_order/chapter_id + offset+limit）。
- items 模式不要用 chapter_id/node_id 直接定位；分页模式可用 chapter_id。
- exact_search_paragraphs 使用 keywords + terms_required/terms_optional/terms_excluded + proximity_terms/proximity_window，不要传 patterns/regex 参数。
- search_intent 仅用于描述本轮检索假设，不会自动回填为 must/optional 关键词。
- 需要排除词时，用 terms_excluded；需要关系邻近时，用 proximity_terms + proximity_window。
- 如果要区分硬约束与软约束：terms_required 放必须词，terms_optional 放可选词。
- 禁止一次性并列长串抽象负向词（如“代价/限制/风险/误判/副作用…”）；必须先拆成 1-2 个可落地关键词再检索。
- 不要搜索已搜索过的关键词或其变体（检查上方"搜索历史"中已搜过的内容）。
- 不要仅交换关键词顺序制造“新查询”（如 [A,B] 与 [B,A] 视为同一查询）。
- 若上方提示“上下文已覆盖”，则不要再次调用 read_paragraph/read_paragraphs 读取同一目标段落。

何时应选择 action="stop"：
1. 目标任务所需的关键信息已获取足够（检查搜索历史中的命中摘要）
2. 已搜索的关键词已覆盖目标概念（不要反复搜索同义词/变体）
3. 可读段落剩余不足 30 时，应优先停止而非继续搜索
4. 连续多轮搜索未发现新的有价值信息
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

    async def _ai_generate_forced_reason(
        self,
        tool_name: str,
        args: Optional[Dict[str, Any]] = None
    ) -> str:
        """为强制流程步骤生成 LLM 理由（用于描述行，不影响胶囊）"""
        from app.services.agent.model_selector import TaskType

        ai_service = _get_ai_service()
        args = args or {}
        prompt = f"""你是只读探索器。请为当前强制步骤生成一句简短理由（不超过20字），用于UI描述。

目标任务：{self.target_task}
当前强制工具：{tool_name}
参数：{json.dumps(args, ensure_ascii=False)}

输出要求：
- 只输出一句中文理由
- 不要包含英文或工具名
"""
        try:
            response = await ai_service.call_ai(
                system_prompt="你是只读探索器。只输出一句中文理由。",
                user_prompt=prompt,
                max_tokens=80,
                temperature=0.2,
                task_type=TaskType.SIMPLE_QA
            )
            return (response or "").strip()
        except Exception as e:
            logger.warning(f"[ContentExplorer] 强制步骤理由生成失败: {e}")
            return ""

    async def _execute_tool_action(
        self,
        tool_name: str,
        args: Dict[str, Any],
        round_idx: int,
        read_budget: Optional[int]
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
        # 🔧 2026-01-28: 无条件覆盖 work_id，防止 AI 生成错误值（如 "work_id" 字面字符串）
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

        def _pick_first_defined(mapping: Dict[str, Any], keys: Tuple[str, ...]) -> Any:
            for key in keys:
                if key in mapping:
                    value = mapping.get(key)
                    if value is not None:
                        return value
            return None

        result_data: Any = {"success": False, "error": "未执行"}
        logger.info(
            "[ExploreTool] call=%s params=%s",
            tool_name,
            _truncate_text(json.dumps(params, ensure_ascii=False), 800)
        )

        if tool_name == "list_chapters":
            chapters = await self._get_chapter_list()
            if self.chapter_scopes:
                chapters = [ch for ch in chapters if self._is_chapter_in_scope(ch.get("order"))]
            result_data = {
                "success": True,
                "count": len(chapters),
                "chapters": chapters
            }
            self.flow_listed_chapters = True
            logger.info(
                "[ExploreTool] done=%s success=%s count=%s",
                tool_name,
                True,
                len(chapters)
            )

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
                if isinstance(result_data, dict) and result_data.get("success") and isinstance(chapter_order, int):
                    self.flow_listed_paragraphs.add(chapter_order)
                    self._cache_paragraph_index_map(chapter_order, result_data)
                    approx = bool(result_data.get("approximate"))
                    offset_val = params.get("offset")
                    limit_val = params.get("limit")
                    if isinstance(offset_val, str) and offset_val.isdigit():
                        offset_val = int(offset_val)
                    if isinstance(limit_val, str) and limit_val.isdigit():
                        limit_val = int(limit_val)
                    if not isinstance(limit_val, int) or limit_val <= 0:
                        limit_val = LIST_PARAGRAPHS_PAGE_SIZE
                    self._record_listed_paragraph_range(
                        chapter_order=chapter_order,
                        offset=offset_val if isinstance(offset_val, int) else 0,
                        limit=limit_val,
                        total=result_data.get("total_paragraphs"),
                        approximate=approx
                    )
            logger.info(
                "[ExploreTool] done=%s success=%s chapter=%s offset=%s limit=%s approximate=%s",
                tool_name,
                bool(result_data.get("success")) if isinstance(result_data, dict) else False,
                chapter_order,
                params.get("offset"),
                params.get("limit"),
                result_data.get("approximate") if isinstance(result_data, dict) else None
            )

        elif tool_name == "exact_search_paragraphs":
            raw_keywords = params.get("keywords") or params.get("keyword") or params.get("query") or []
            strategy_label = str(params.get("strategy") or "ai").strip().lower() or "ai"
            requested_match_mode = str(params.get("match_mode") or params.get("mode") or "").strip().lower()
            search_intent_text = str(params.get("search_intent") or params.get("intent") or "").strip()

            def _split_keywords(text: str) -> List[str]:
                parts = [text]
                for sep in ("|", "｜", "/", "，", "、", ";", "；", ","):
                    new_parts: List[str] = []
                    for part in parts:
                        if sep in part:
                            new_parts.extend(part.split(sep))
                        else:
                            new_parts.append(part)
                    parts = new_parts
                return [p.strip() for p in parts if p.strip()]

            if isinstance(raw_keywords, str):
                keywords = _split_keywords(raw_keywords)
            elif isinstance(raw_keywords, list):
                keywords = []
                for item in raw_keywords:
                    text = str(item).strip()
                    if not text:
                        continue
                    keywords.extend(_split_keywords(text))
            else:
                keywords = []

            cleaned_keywords = []
            seen_kw = set()
            for kw in keywords:
                cleaned = str(kw).strip().strip("\"'“”‘’《》")
                if not cleaned:
                    continue
                if cleaned in seen_kw:
                    continue
                seen_kw.add(cleaned)
                cleaned_keywords.append(cleaned)
            keywords = self.intent_compiler.sanitize_external_keywords(
                cleaned_keywords,
                self.target_task or "",
                limit=10,
            )

            terms_required = self._parse_search_term_values(params.get("terms_required"))
            terms_optional = self._parse_search_term_values(params.get("terms_optional"))
            terms_excluded = self._parse_search_term_values(params.get("terms_excluded"))
            proximity_terms = self._parse_search_term_values(params.get("proximity_terms"))
            intent_hint_terms = self._parse_search_term_values(search_intent_text) if search_intent_text else []
            if not keywords and intent_hint_terms:
                keywords = self.intent_compiler.sanitize_external_keywords(
                    intent_hint_terms,
                    self.target_task or "",
                    limit=8,
                )
            proximity_window = params.get("proximity_window")
            if isinstance(proximity_window, str) and proximity_window.strip().isdigit():
                proximity_window = int(proximity_window.strip())
            if not isinstance(proximity_window, int) or proximity_window <= 0:
                proximity_window = 12

            if requested_match_mode in ("any", "all", "phrase"):
                match_mode = requested_match_mode
            elif requested_match_mode in ("fuzzy", "recall", "loose"):
                match_mode = "any"
            else:
                # 默认严格层：单词短语匹配，多词全量匹配（不自动回退 any）
                match_mode = "all" if len(keywords) > 1 else "phrase"

            def _coerce_int(value: Any) -> Optional[int]:
                if isinstance(value, int):
                    return value
                if isinstance(value, str) and value.strip().isdigit():
                    return int(value.strip())
                return None

            def _add_range(target: List[Tuple[int, int]], start: Any, end: Any) -> None:
                start_val = _coerce_int(start)
                end_val = _coerce_int(end)
                if start_val is None and end_val is None:
                    return
                if start_val is None:
                    start_val = end_val
                if end_val is None:
                    end_val = start_val
                if start_val is None or end_val is None:
                    return
                if start_val > end_val:
                    start_val, end_val = end_val, start_val
                target.append((start_val, end_val))

            def _parse_param_ranges(param_dict: Dict[str, Any]) -> List[Tuple[int, int]]:
                parsed: List[Tuple[int, int]] = []
                raw_range = param_dict.get("chapter_range")
                if raw_range:
                    if isinstance(raw_range, str):
                        nums = [int(n) for n in re.findall(r"\d+", raw_range)]
                        if nums:
                            start_num = nums[0]
                            end_num = nums[1] if len(nums) > 1 else nums[0]
                            _add_range(parsed, start_num, end_num)
                    elif isinstance(raw_range, (list, tuple)) and len(raw_range) >= 2:
                        _add_range(parsed, raw_range[0], raw_range[1])
                    elif isinstance(raw_range, dict):
                        _add_range(
                            parsed,
                            raw_range.get("chapter_order_start") or raw_range.get("start"),
                            raw_range.get("chapter_order_end") or raw_range.get("end")
                        )
                raw_ranges = param_dict.get("chapter_ranges")
                if raw_ranges and isinstance(raw_ranges, list):
                    for item in raw_ranges:
                        if isinstance(item, (list, tuple)) and len(item) >= 2:
                            _add_range(parsed, item[0], item[1])
                        elif isinstance(item, dict):
                            _add_range(
                                parsed,
                                item.get("chapter_order_start") or item.get("start"),
                                item.get("chapter_order_end") or item.get("end")
                            )
                raw_orders = param_dict.get("chapter_orders")
                parsed_orders: List[int] = []
                if isinstance(raw_orders, (list, tuple, set)):
                    for item in raw_orders:
                        order = _coerce_int(item)
                        if isinstance(order, int):
                            parsed_orders.append(order)
                        elif isinstance(item, str):
                            parsed_orders.extend(int(n) for n in re.findall(r"\d+", item))
                elif isinstance(raw_orders, str):
                    parsed_orders.extend(int(n) for n in re.findall(r"\d+", raw_orders))
                elif raw_orders is not None:
                    order = _coerce_int(raw_orders)
                    if isinstance(order, int):
                        parsed_orders.append(order)
                if parsed_orders:
                    for order in sorted(set(parsed_orders)):
                        _add_range(parsed, order, order)
                return parsed

            param_ranges = _parse_param_ranges(params)
            if not param_ranges:
                chapter_order_param = _coerce_int(params.get("chapter_order") or params.get("chapter"))
                if isinstance(chapter_order_param, int):
                    param_ranges = [(chapter_order_param, chapter_order_param)]
            ranges_to_use = param_ranges or (self.chapter_scopes or [])
            logger.info(
                "[ExploreTool] exact_search range resolved param=%s scope=%s effective=%s",
                param_ranges or None,
                self.chapter_scopes or None,
                ranges_to_use or "ALL"
            )

            current_scope: Optional[Tuple[int, int]] = None
            if ranges_to_use:
                min_order = min(s[0] for s in ranges_to_use)
                max_order = max(s[1] for s in ranges_to_use)
                current_scope = (min_order, max_order)

            limit = params.get("limit") or 50
            if not isinstance(limit, int):
                try:
                    limit = int(limit)
                except Exception:
                    limit = 50

            planned_probe_signature = ""
            planned_probe_hypothesis = ""
            intent_spec: Optional[IntentSpec] = None
            query_program_info: Optional[Dict[str, Any]] = None
            probe_exhausted = False
            probe_override_applied = False
            if self.intent_retrieval_v2:
                ai_has_structured_query = bool(
                    keywords
                    or terms_required
                    or terms_optional
                    or terms_excluded
                    or proximity_terms
                )
                planned_probe, intent_spec, query_program_info = self._plan_exact_search_probe(
                    manual_keywords=list(keywords),
                    requested_match_mode=requested_match_mode,
                    current_scope=current_scope,
                    limit=limit
                )
                if planned_probe:
                    planned_payload = planned_probe.get("payload") if isinstance(planned_probe, dict) else {}
                    if isinstance(planned_payload, dict):
                        apply_probe_as_primary = (
                            self.intent_probe_override_mode == "force"
                            or not ai_has_structured_query
                        )
                        planned_keywords = planned_payload.get("keywords")
                        if apply_probe_as_primary and isinstance(planned_keywords, list):
                            keywords = self.intent_compiler.sanitize_external_keywords(
                                planned_keywords,
                                self.target_task or "",
                                limit=10,
                            )
                            probe_override_applied = True
                        planned_required = planned_payload.get("terms_required")
                        planned_optional = planned_payload.get("terms_optional")
                        planned_excluded = planned_payload.get("terms_excluded")
                        planned_proximity = planned_payload.get("proximity_terms")
                        parsed_required = self._parse_search_term_values(planned_required)
                        parsed_optional = self._parse_search_term_values(planned_optional)
                        parsed_excluded = self._parse_search_term_values(planned_excluded)
                        parsed_proximity = self._parse_search_term_values(planned_proximity)

                        # 默认“建议模式”：不覆盖 AI 明确给出的结构化参数，只填缺口。
                        # force 模式才执行旧行为（探针参数全量覆盖）。
                        if apply_probe_as_primary:
                            if parsed_required:
                                terms_required = parsed_required
                            if parsed_optional:
                                terms_optional = parsed_optional
                            if parsed_excluded:
                                terms_excluded = parsed_excluded
                            if parsed_proximity:
                                proximity_terms = parsed_proximity
                            probe_override_applied = True
                        else:
                            if not keywords and isinstance(planned_keywords, list):
                                keywords = self.intent_compiler.sanitize_external_keywords(
                                    planned_keywords,
                                    self.target_task or "",
                                    limit=10,
                                )
                            if not terms_required and parsed_required:
                                terms_required = parsed_required
                            if not terms_optional and parsed_optional:
                                terms_optional = parsed_optional
                            if not terms_excluded and parsed_excluded:
                                terms_excluded = parsed_excluded
                            if not proximity_terms and parsed_proximity:
                                proximity_terms = parsed_proximity

                        # 兼容旧行为：仍保留以下判断块（不清空 AI 显式字段）
                        if "terms_required" in planned_payload:
                            if parsed_required:
                                if apply_probe_as_primary or not terms_required:
                                    terms_required = parsed_required
                        if "terms_optional" in planned_payload:
                            if parsed_optional:
                                if apply_probe_as_primary or not terms_optional:
                                    terms_optional = parsed_optional
                        if "terms_excluded" in planned_payload:
                            if parsed_excluded:
                                if apply_probe_as_primary or not terms_excluded:
                                    terms_excluded = parsed_excluded
                        if "proximity_terms" in planned_payload:
                            if parsed_proximity:
                                if apply_probe_as_primary or not proximity_terms:
                                    proximity_terms = parsed_proximity
                        planned_proximity_window = planned_payload.get("proximity_window")
                        if (
                            isinstance(planned_proximity_window, int)
                            and planned_proximity_window > 0
                            and (apply_probe_as_primary or "proximity_window" not in params)
                        ):
                            proximity_window = planned_proximity_window
                        planned_mode = str(planned_payload.get("match_mode") or "").strip().lower()
                        if planned_mode in ("any", "all", "phrase") and (
                            apply_probe_as_primary or not requested_match_mode
                        ):
                            match_mode = planned_mode
                        planned_strategy = str(planned_payload.get("strategy") or "").strip().lower()
                        if planned_strategy and apply_probe_as_primary:
                            strategy_label = planned_strategy
                        planned_probe_signature = str(planned_payload.get("probe_signature") or "").strip()
                        planned_probe_hypothesis = str(planned_payload.get("probe_hypothesis") or "").strip()
                        params["keywords"] = list(keywords)
                        params["terms_required"] = list(terms_required)
                        params["terms_optional"] = list(terms_optional)
                        params["terms_excluded"] = list(terms_excluded)
                        params["proximity_terms"] = list(proximity_terms)
                        params["proximity_window"] = proximity_window
                        params["match_mode"] = match_mode
                        if planned_probe_signature:
                            params["probe_signature"] = planned_probe_signature
                        if planned_probe_hypothesis:
                            params["probe_hypothesis"] = planned_probe_hypothesis
                        params["strategy"] = strategy_label
                        params["probe_override_applied"] = probe_override_applied
                else:
                    probe_exhausted = True
                    self.state.iteration_state.mark_failure("probe_exhausted")

            blocked_keywords: List[Dict[str, str]] = []
            filtered_keywords: List[str] = []
            for kw in keywords:
                blocked, reason = self.state.should_block_search(kw, current_scope)
                if blocked:
                    blocked_keywords.append({"keyword": kw, "reason": reason})
                    continue
                filtered_keywords.append(kw)
            keywords = filtered_keywords
            if not terms_required:
                terms_required = list(keywords[:2])
            if not terms_optional and len(keywords) > len(terms_required):
                terms_optional = [kw for kw in keywords if kw not in terms_required][:3]
            if not proximity_terms and len(terms_required) >= 2:
                proximity_terms = terms_required[:2]
            fingerprint_terms = keywords or terms_required or terms_optional or proximity_terms
            keyword_fingerprint = self.state._build_attempt_fingerprint(fingerprint_terms, current_scope, match_mode) if fingerprint_terms else ""
            blocked_by_same_fingerprint = False
            if fingerprint_terms and strategy_label != "forced_rewrite" and not probe_exhausted:
                zero_hit_same_fingerprint = self.state.count_zero_hit_fingerprint(
                    keywords=fingerprint_terms,
                    scope=current_scope,
                    mode=match_mode,
                )
                if zero_hit_same_fingerprint > ZERO_HIT_SAME_FINGERPRINT_MAX_RETRIES:
                    blocked_by_same_fingerprint = True
                    blocked_keywords.append({
                        "keyword": ",".join(fingerprint_terms[:3]),
                        "reason": (
                            f"同查询指纹已连续0命中{zero_hit_same_fingerprint}次，"
                            "请更换关键词或范围"
                        )
                    })
            active_query_keywords = keywords or terms_required or terms_optional or proximity_terms
            query_terms = active_query_keywords[:3]
            query = ",".join(query_terms) if query_terms else "exact_search"

            if not active_query_keywords or blocked_by_same_fingerprint or probe_exhausted:
                if blocked_by_same_fingerprint:
                    error_text = "同查询指纹连续0命中，已阻止重复搜索"
                elif probe_exhausted:
                    error_text = "查询程序无可执行新探针"
                else:
                    error_text = "关键词已被拦截" if blocked_keywords else "缺少可执行的 keywords"
                result_data = {
                    "success": False,
                    "error": error_text,
                    "blocked_keywords": blocked_keywords,
                    "strategy": strategy_label,
                    "match_mode": match_mode,
                    "keyword_fingerprint": keyword_fingerprint,
                    "keywords": list(active_query_keywords),
                    "terms_required": list(terms_required),
                    "terms_optional": list(terms_optional),
                    "terms_excluded": list(terms_excluded),
                    "proximity_terms": list(proximity_terms),
                    "proximity_window": proximity_window,
                    "probe_signature": planned_probe_signature,
                    "probe_hypothesis": planned_probe_hypothesis,
                    "intent_id": intent_spec.intent_id if isinstance(intent_spec, IntentSpec) else "",
                    "query_program_probes": len((query_program_info or {}).get("probes") or []),
                }
                if planned_probe_signature:
                    self.state.iteration_state.mark_probe(planned_probe_signature)
                if blocked_by_same_fingerprint:
                    self.state.iteration_state.mark_failure("duplicate_fingerprint")
                elif not active_query_keywords:
                    self.state.iteration_state.mark_failure("no_keywords")
                self.state.add_query_attempt(QueryAttempt(
                    query=query,
                    keywords=list(active_query_keywords),
                    match_mode=match_mode,
                    chapter_scope=current_scope,
                    round_idx=round_idx,
                    strategy=strategy_label,
                    hits=0,
                    chapter_hits=0,
                    worldview_hits=0,
                    blocked_keywords=len(blocked_keywords),
                    error=error_text,
                    keyword_fingerprint=keyword_fingerprint,
                    intent_id=intent_spec.intent_id if isinstance(intent_spec, IntentSpec) else "",
                    probe_signature=planned_probe_signature,
                    probe_hypothesis=planned_probe_hypothesis,
                    failure_reason="probe_exhausted" if probe_exhausted else (
                        "duplicate_fingerprint" if blocked_by_same_fingerprint else "no_keywords"
                    ),
                ))
            else:
                if planned_probe_signature:
                    self.state.iteration_state.mark_probe(planned_probe_signature)
                for kw in active_query_keywords:
                    self.state.record_search(kw)

                results: List[Dict[str, Any]] = []
                effective_keywords = list(active_query_keywords)
                effective_match_mode = match_mode
                effective_strategy = "strict" if strategy_label == "ai" else f"{strategy_label}_strict"
                search_attempt_layers: List[Dict[str, Any]] = []

                worldview_matches = self._search_worldview_for_keywords(active_query_keywords) if active_query_keywords else []
                if worldview_matches:
                    logger.info(f"[ContentExplorer] 世界观匹配: {len(worldview_matches)} 条")
                    for wv_item in worldview_matches:
                        results.append({
                            "snippet": wv_item.get("description", "")[:200],
                            "content": wv_item.get("description", ""),
                            "chapter_order": None,
                            "paragraph_index": None,
                            "source": "worldview",
                            "similarity": 1.0,
                            "worldview_category": wv_item.get("category", ""),
                            "worldview_name": wv_item.get("name", "")
                        })

                async with AsyncSessionLocal() as db:
                    vector_service = ChapterVectorService(db)
                    search_fn = vector_service.exact_search_paragraphs

                    async def _run_exact_search_layer(
                        layer_strategy: str,
                        layer_keywords: List[str],
                        layer_match_mode: str,
                        layer_terms_required: Optional[List[str]] = None,
                        layer_terms_optional: Optional[List[str]] = None,
                        layer_terms_excluded: Optional[List[str]] = None,
                        layer_proximity_terms: Optional[List[str]] = None,
                        layer_proximity_window: Optional[int] = None,
                    ) -> List[Dict[str, Any]]:
                        layer_results: List[Dict[str, Any]] = []
                        if ranges_to_use:
                            for start_order, end_order in ranges_to_use:
                                part = await search_fn(
                                    work_id=self.work_id,
                                    keywords=layer_keywords,
                                    chapter_range=(start_order, end_order),
                                    match_mode=layer_match_mode,
                                    limit=limit,
                                    terms_required=layer_terms_required,
                                    terms_optional=layer_terms_optional,
                                    terms_excluded=layer_terms_excluded,
                                    proximity_terms=layer_proximity_terms,
                                    proximity_window=layer_proximity_window,
                                )
                                layer_results.extend(part or [])
                        else:
                            part = await search_fn(
                                work_id=self.work_id,
                                keywords=layer_keywords,
                                chapter_range=None,
                                match_mode=layer_match_mode,
                                limit=limit,
                                terms_required=layer_terms_required,
                                terms_optional=layer_terms_optional,
                                terms_excluded=layer_terms_excluded,
                                proximity_terms=layer_proximity_terms,
                                proximity_window=layer_proximity_window,
                            )
                            layer_results.extend(part or [])

                        dropped_missing_locator = 0
                        normalized_layer_results: List[Dict[str, Any]] = []
                        for item in layer_results:
                            if not isinstance(item, dict):
                                continue
                            chapter_order = item.get("chapter_order")
                            paragraph_index = item.get("paragraph_index")
                            if isinstance(chapter_order, str) and chapter_order.isdigit():
                                chapter_order = int(chapter_order)
                            if isinstance(paragraph_index, str) and paragraph_index.isdigit():
                                paragraph_index = int(paragraph_index)
                            if not isinstance(chapter_order, int) or not isinstance(paragraph_index, int):
                                dropped_missing_locator += 1
                                continue
                            item["chapter_order"] = chapter_order
                            item["paragraph_index"] = paragraph_index
                            normalized_layer_results.append(item)

                        layer_chapter_hits = [
                            item for item in normalized_layer_results
                            if isinstance(item, dict) and item.get("source") != "worldview"
                        ]
                        layer_query_terms = layer_keywords[:3]
                        layer_query = ",".join(layer_query_terms) if layer_query_terms else "exact_search"
                        search_attempt_layers.append({
                            "strategy": layer_strategy,
                            "keywords": list(layer_keywords),
                            "terms_required": list(layer_terms_required or []),
                            "terms_optional": list(layer_terms_optional or []),
                            "terms_excluded": list(layer_terms_excluded or []),
                            "proximity_terms": list(layer_proximity_terms or []),
                            "proximity_window": layer_proximity_window,
                            "match_mode": layer_match_mode,
                            "hits": len(normalized_layer_results),
                            "chapter_hits": len(layer_chapter_hits),
                            "dropped_missing_locator": dropped_missing_locator,
                            "intent_id": intent_spec.intent_id if isinstance(intent_spec, IntentSpec) else "",
                            "probe_signature": planned_probe_signature,
                        })
                        self.state.add_query_attempt(QueryAttempt(
                            query=layer_query,
                            keywords=list(layer_keywords),
                            match_mode=layer_match_mode,
                            chapter_scope=current_scope,
                            round_idx=round_idx,
                            strategy=layer_strategy,
                            hits=len(normalized_layer_results),
                            chapter_hits=len(layer_chapter_hits),
                            worldview_hits=len(worldview_matches),
                            blocked_keywords=len(blocked_keywords),
                            error="",
                            keyword_fingerprint=self.state._build_attempt_fingerprint(
                                (layer_keywords or [])
                                + (layer_terms_required or [])
                                + (layer_terms_optional or []),
                                current_scope,
                                layer_match_mode,
                            ),
                            intent_id=intent_spec.intent_id if isinstance(intent_spec, IntentSpec) else "",
                            probe_signature=planned_probe_signature,
                            probe_hypothesis=planned_probe_hypothesis,
                        ))
                        return normalized_layer_results

                    chapter_results = await _run_exact_search_layer(
                        layer_strategy=effective_strategy,
                        layer_keywords=active_query_keywords,
                        layer_match_mode=match_mode,
                        layer_terms_required=terms_required,
                        layer_terms_optional=terms_optional,
                        layer_terms_excluded=terms_excluded,
                        layer_proximity_terms=proximity_terms,
                        layer_proximity_window=proximity_window,
                    )
                    results.extend(chapter_results)

                match_mode = effective_match_mode
                strategy_label = effective_strategy
                query_terms = active_query_keywords[:3]
                query = ",".join(query_terms) if query_terms else "exact_search"

                filter_stats: Dict[str, int] = {
                    "before_scope_filter": len(results),
                    "dropped_scope": 0,
                    "before_locator_filter": 0,
                    "dropped_locator": 0,
                    "weak_literal_hits": 0,
                }
                filter_stats["weak_literal_hits"] = sum(
                    1
                    for item in results
                    if isinstance(item, dict) and bool(item.get("weak_literal_match"))
                )

                if param_ranges:
                    before_param_filter = len(results)
                    results = [
                        r for r in results
                        if isinstance(r, dict)
                        and isinstance(r.get("chapter_order"), int)
                        and any(start <= r.get("chapter_order") <= end for start, end in param_ranges)
                    ]
                    filter_stats["dropped_scope"] += max(0, before_param_filter - len(results))

                if self.chapter_scopes:
                    before_scope_filter = len(results)
                    results = self._filter_results_in_scope(results)
                    filter_stats["dropped_scope"] += max(0, before_scope_filter - len(results))

                # 定位契约兜底：仅允许可定位命中进入后续读取流程
                locator_filtered_results: List[Dict[str, Any]] = []
                dropped_locator_results = 0
                filter_stats["before_locator_filter"] = len(results)
                for item in results:
                    if not isinstance(item, dict):
                        continue
                    if item.get("source") == "worldview":
                        locator_filtered_results.append(item)
                        continue
                    chapter_order = item.get("chapter_order")
                    paragraph_index = item.get("paragraph_index")
                    if isinstance(chapter_order, str) and chapter_order.isdigit():
                        chapter_order = int(chapter_order)
                    if isinstance(paragraph_index, str) and paragraph_index.isdigit():
                        paragraph_index = int(paragraph_index)
                    if not isinstance(chapter_order, int) or not isinstance(paragraph_index, int):
                        dropped_locator_results += 1
                        continue
                    item["chapter_order"] = chapter_order
                    item["paragraph_index"] = paragraph_index
                    locator_filtered_results.append(item)
                if dropped_locator_results:
                    logger.info(
                        "[ExploreTool] exact_search locator filter dropped=%s",
                        dropped_locator_results
                    )
                filter_stats["dropped_locator"] = dropped_locator_results
                results = locator_filtered_results

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
                    if item.get("source") == "worldview":
                        key = ("worldview", item.get("worldview_name"), str(snippet)[:80])
                    else:
                        key = (chapter_order, paragraph_index, str(snippet)[:80])
                    existing = merged.get(key)
                    if not existing or item.get("similarity", 0) > existing.get("similarity", 0):
                        merged[key] = item
                results = list(merged.values())

                judge_summary: Dict[str, Any] = {
                    "cards": [],
                    "covered_terms": [],
                    "coverage_ratio": 0.0,
                    "failure_reason": "",
                    "avg_score": 0.0,
                }
                if isinstance(intent_spec, IntentSpec):
                    chapter_results_for_judge = [
                        item for item in results
                        if isinstance(item, dict) and item.get("source") != "worldview"
                    ]
                    judge_summary = self.evidence_judge.judge(
                        results=chapter_results_for_judge,
                        intent=intent_spec,
                        active_keywords=active_query_keywords,
                    )
                    covered_terms = judge_summary.get("covered_terms") or []
                    self.state.iteration_state.update_coverage(
                        covered_terms=covered_terms,
                        total_must_have=len(intent_spec.must_have),
                    )
                    failure_reason = str(judge_summary.get("failure_reason") or "").strip()
                    if failure_reason:
                        self.state.iteration_state.mark_failure(failure_reason)

                def _extract_matched_keywords(item: Dict[str, Any], pool: List[str]) -> List[str]:
                    matched_list = item.get("matched_keywords") if isinstance(item, dict) else None
                    if isinstance(matched_list, list) and matched_list:
                        return [kw for kw in matched_list if kw in pool]
                    text = item.get("text") or item.get("content") or item.get("snippet") or ""
                    if not text:
                        return []
                    text_lower = text.lower()
                    return [kw for kw in pool if kw.lower() in text_lower]

                for item in results:
                    self.state.add_search_hit(
                        item,
                        query=query,
                        round_idx=round_idx,
                        chapter_scope_filter=self._is_chapter_in_scope if self.chapter_scopes else None
                    )

                ordered_results = results
                if results and active_query_keywords:
                    keyword_hits: Dict[str, List[Dict[str, Any]]] = {kw: [] for kw in active_query_keywords}
                    for item in results:
                        if not isinstance(item, dict) or item.get("source") == "worldview":
                            continue
                        for mk in _extract_matched_keywords(item, active_query_keywords):
                            keyword_hits.setdefault(mk, []).append(item)
                    position_map: Dict[Tuple[int, int], Dict[str, Any]] = {}
                    for item in results:
                        if not isinstance(item, dict) or item.get("source") == "worldview":
                            continue
                        chapter_order = item.get("chapter_order")
                        paragraph_index = item.get("paragraph_index")
                        if isinstance(chapter_order, int) and isinstance(paragraph_index, int):
                            position_map.setdefault((chapter_order, paragraph_index), item)
                    priority_positions: List[Tuple[int, int]] = []
                    used_positions: Set[Tuple[int, int]] = set()
                    for kw, items_for_kw in keyword_hits.items():
                        added = 0
                        for item in items_for_kw:
                            chapter_order = item.get("chapter_order")
                            paragraph_index = item.get("paragraph_index")
                            if not isinstance(chapter_order, int) or not isinstance(paragraph_index, int):
                                continue
                            key = (chapter_order, paragraph_index)
                            if key in used_positions:
                                continue
                            priority_positions.append(key)
                            used_positions.add(key)
                            added += 1
                            if added >= KEYWORD_READ_MAX_PER_TERM:
                                break
                    if priority_positions:
                        priority_items = [position_map[pos] for pos in priority_positions if pos in position_map]
                        priority_set = set(priority_positions)
                        tail_items = [
                            item for item in results
                            if not isinstance(item, dict)
                            or item.get("source") == "worldview"
                            or (
                                isinstance(item.get("chapter_order"), int)
                                and isinstance(item.get("paragraph_index"), int)
                                and (item.get("chapter_order"), item.get("paragraph_index")) not in priority_set
                            )
                        ]
                        ordered_results = priority_items + tail_items

                read_keyword_hits: Set[str] = set()
                if ordered_results and (read_budget is None or read_budget > 0):
                    for item in ordered_results:
                        if read_budget is not None and read_budget <= 0:
                            break
                        if item.get("source") == "worldview":
                            continue
                        chapter_order = item.get("chapter_order")
                        paragraph_index = item.get("paragraph_index")
                        if isinstance(chapter_order, str) and chapter_order.isdigit():
                            chapter_order = int(chapter_order)
                        if isinstance(paragraph_index, str) and paragraph_index.isdigit():
                            paragraph_index = int(paragraph_index)
                        if not isinstance(chapter_order, int) or not isinstance(paragraph_index, int):
                            continue
                        if self.chapter_scopes and not self._is_chapter_in_scope(chapter_order):
                            continue
                        if not self.state.should_read_paragraph(chapter_order, paragraph_index):
                            continue
                        if not self._can_read_chapter(chapter_order):
                            continue
                        try:
                            read_result = await read_paragraph.ainvoke({
                                "work_id": self.work_id,
                                "chapter_order": chapter_order,
                                "paragraph_index": paragraph_index,
                                "context_before": 2,
                                "context_after": 2,
                                "index_base": "zero"
                            })
                            read_data = json.loads(read_result) if isinstance(read_result, str) else read_result
                            if isinstance(read_data, dict) and read_data.get("success"):
                                self.state.record_paragraph_read(chapter_order, paragraph_index)
                                target_text, context_before, context_after = _extract_read_paragraph(read_data)
                                chapter_info = await self._get_chapter_info_by_order(chapter_order)
                                chapter_id = chapter_info.get("chapter_id") or chapter_info.get("id") or ""
                                chapter_title = read_data.get("chapter_title") or chapter_info.get("title") or ""
                                if target_text and active_query_keywords:
                                    text_lower = target_text.lower()
                                    for kw in active_query_keywords:
                                        if kw and kw.lower() in text_lower:
                                            read_keyword_hits.add(kw)
                                paragraph_data = {
                                    "chapter_order": chapter_order,
                                    "chapter_title": chapter_title,
                                    "paragraph_index": paragraph_index,
                                    "text": target_text,
                                    "context_before": context_before,
                                    "context_after": context_after,
                                    "node_id": read_data.get("node_id") or ""
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
                                    query=query,
                                    round_idx=round_idx,
                                    require_paragraph_index=self.require_paragraph_index,
                                    chapter_scope_filter=self._is_chapter_in_scope if self.chapter_scopes else None
                                )
                                reads_used += 1
                                if read_budget is not None:
                                    read_budget -= 1
                        except Exception:
                            continue

                chapter_hits = [r for r in results if r.get("source") != "worldview"]
                worldview_hits_count = len(worldview_matches) if worldview_matches else 0
                missing_keywords = [kw for kw in active_query_keywords if kw not in read_keyword_hits] if active_query_keywords else []
                failure_reason_text = str(judge_summary.get("failure_reason") or "").strip()
                adaptive_overrides: Dict[str, Any] = {}
                if self.intent_retrieval_v2 and (failure_reason_text or not chapter_hits):
                    adaptive_rewrite = self.adaptive_controller.build_rewrite(
                        failure_reason=failure_reason_text or "lexical_miss",
                        target_task=self.target_task or "",
                        intent_spec=self.state.latest_intent_spec if isinstance(self.state.latest_intent_spec, dict) else {},
                        iteration_state=self.state.iteration_state.to_dict(),
                        latest_keywords=active_query_keywords,
                        latest_terms_required=terms_required,
                        latest_terms_optional=terms_optional,
                        latest_terms_excluded=terms_excluded,
                        latest_proximity_terms=proximity_terms,
                        latest_scope=current_scope,
                        seed_keywords=self.search_keywords or [],
                    )
                    if adaptive_rewrite:
                        adaptive_overrides = adaptive_rewrite.to_search_args()
                if failure_reason_text:
                    for attempt in reversed(self.state.query_attempts):
                        if attempt.round_idx != round_idx:
                            continue
                        if not attempt.failure_reason:
                            attempt.failure_reason = failure_reason_text
                        if not attempt.probe_signature and planned_probe_signature:
                            attempt.probe_signature = planned_probe_signature
                        if not attempt.probe_hypothesis and planned_probe_hypothesis:
                            attempt.probe_hypothesis = planned_probe_hypothesis

                result_data = {
                    "success": True,
                    "keywords": list(active_query_keywords),
                    "terms_required": list(terms_required),
                    "terms_optional": list(terms_optional),
                    "terms_excluded": list(terms_excluded),
                    "proximity_terms": list(proximity_terms),
                    "proximity_window": proximity_window,
                    "match_mode": match_mode,
                    "strategy": strategy_label,
                    "intent_id": intent_spec.intent_id if isinstance(intent_spec, IntentSpec) else "",
                    "probe_signature": planned_probe_signature,
                    "probe_hypothesis": planned_probe_hypothesis,
                    "search_layers": search_attempt_layers,
                    "hits": len(results),
                    "chapter_hits": len(chapter_hits),
                    "worldview_hits": worldview_hits_count,
                    "results": _preview_results(results),
                    "missing_keywords": missing_keywords,
                    "blocked_keywords": blocked_keywords,
                    "judge": {
                        "coverage_ratio": judge_summary.get("coverage_ratio"),
                        "covered_terms": judge_summary.get("covered_terms"),
                        "failure_reason": judge_summary.get("failure_reason"),
                        "avg_score": judge_summary.get("avg_score"),
                        "cards": (judge_summary.get("cards") or [])[:INTENT_JUDGE_CARD_PREVIEW],
                    },
                    "failure_reason": judge_summary.get("failure_reason") or "",
                    "filter_stats": filter_stats,
                    "query_program_probes": len((query_program_info or {}).get("probes") or []),
                    "probe_override_applied": probe_override_applied,
                    "must_have_coverage_set": sorted(self.state.iteration_state.covered_must_have_set),
                    "must_have_total": int(self.state.iteration_state.must_have_total or 0),
                    "must_have_coverage_ratio": self.state.iteration_state.novel_evidence_ratio,
                }
                if adaptive_overrides:
                    result_data["adaptive_overrides"] = adaptive_overrides

                chapters_in_results = list(set(
                    r.get("chapter_order") for r in results
                    if isinstance(r.get("chapter_order"), int)
                ))
                hits_summary = self._generate_hits_summary(results, keywords)
                self.state.add_search_record(SearchRecord(
                    query=query,
                    tool="exact_search_paragraphs",
                    hits_count=len(chapter_hits),
                    hits_summary=hits_summary,
                    chapters_covered=chapters_in_results,
                    round_idx=round_idx,
                    chapter_scope=current_scope,
                    worldview_checked=True,
                    worldview_hits=worldview_hits_count
                ))

                logger.info(
                    "[ExploreTool] done=%s success=%s hits=%s (chapter=%s, worldview=%s) strategy=%s probe=%s keywords=%s blocked=%s coverage=%.2f",
                    tool_name,
                    True,
                    len(results),
                    len(chapter_hits),
                    worldview_hits_count,
                    strategy_label,
                    planned_probe_signature,
                    ",".join(keywords[:6]),
                    len(blocked_keywords),
                    float(self.state.iteration_state.novel_evidence_ratio or 0.0)
                )

        elif tool_name == "read_paragraph":
            if read_budget is not None and read_budget <= 0:
                result_data = {"success": False, "error": "读取预算已用尽"}
            else:
                chapter_order = params.get("chapter_order") or params.get("chapter")
                paragraph_index = _pick_first_defined(params, ("paragraph_index", "paragraph"))
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
                elif not self._can_read_chapter(chapter_order):
                    result_data = {"success": False, "error": "本章读取上限已达"}
                else:
                    params["work_id"] = self.work_id
                    params["chapter_order"] = chapter_order
                    params["paragraph_index"] = paragraph_index
                    params["index_base"] = "zero"
                    if chapter_id:
                        params["chapter_id"] = chapter_id
                    result = await read_paragraph.ainvoke(params)
                    result_data = json.loads(result) if isinstance(result, str) else result
                logger.info(
                    "[ExploreTool] done=%s success=%s chapter=%s paragraph=%s index_base=%s",
                    tool_name,
                    bool(result_data.get("success")) if isinstance(result_data, dict) else False,
                    chapter_order,
                    paragraph_index,
                    params.get("index_base")
                )

                if isinstance(result_data, dict) and result_data.get("success") and not result_data.get("skipped"):
                    self.state.record_paragraph_read(chapter_order, paragraph_index)
                    target_text, context_before, context_after = _extract_read_paragraph(result_data)
                    if not target_text:
                        target_text = result_data.get("content") or result_data.get("target_paragraph", "")
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
                    if target_text:
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

                    paragraphs = result_data.get("paragraphs", [])
                    target_index = result_data.get("target_index")
                    if isinstance(paragraphs, list):
                        indices = [
                            para.get("index")
                            for para in paragraphs
                            if isinstance(para, dict) and isinstance(para.get("index"), int)
                        ]
                        if isinstance(target_index, int) and indices:
                            self.state.record_context_coverage(
                                chapter_order=chapter_order,
                                target_index=target_index,
                                start_index=min(indices),
                                end_index=max(indices)
                            )
                        for para in paragraphs:
                            if not isinstance(para, dict):
                                continue
                            if para.get("is_target"):
                                continue
                            context_index = para.get("index")
                            if not isinstance(context_index, int):
                                continue
                            if not self.state.should_read_paragraph(chapter_order, context_index):
                                continue
                            context_text = para.get("text") or ""
                            if not context_text:
                                continue
                            self.state.record_paragraph_read(chapter_order, context_index)
                            self.state.add_paragraph(
                                {
                                    "chapter_order": chapter_order,
                                    "chapter_title": chapter_title,
                                    "paragraph_index": context_index,
                                    "text": context_text,
                                    "context_before": [],
                                    "context_after": [],
                                    "node_id": "",
                                    "is_target": False
                                },
                                round_idx
                            )

        elif tool_name == "read_paragraphs":
            items = params.get("items")
            if items is None:
                items = []
            if not isinstance(items, list):
                items = []
            use_range = (
                not items
                and (
                    "chapter_order" in params
                    or "chapter_id" in params
                    or "offset" in params
                    or "limit" in params
                )
            )
            if read_budget is not None and read_budget <= 0:
                result_data = {"success": False, "error": "读取预算已用尽"}
            else:
                chapter_id_map: Optional[Dict[str, int]] = None
                if use_range:
                    chapter_order = params.get("chapter_order")
                    chapter_id = params.get("chapter_id") or ""
                    if isinstance(chapter_order, str) and chapter_order.isdigit():
                        chapter_order = int(chapter_order)
                        params["chapter_order"] = chapter_order
                    if not isinstance(chapter_order, int) and chapter_id:
                        chapters = await self._get_chapter_list()
                        chapter_id_map = {}
                        for ch in chapters:
                            order_val = ch.get("order")
                            if not isinstance(order_val, int):
                                continue
                            for key in (ch.get("id"), ch.get("chapter_id")):
                                if key:
                                    chapter_id_map[str(key)] = order_val
                        chapter_order = chapter_id_map.get(str(chapter_id))
                        if isinstance(chapter_order, int):
                            params["chapter_order"] = chapter_order
                    if not isinstance(chapter_order, int):
                        result_data = {"success": False, "error": "缺少章节参数"}
                    elif self.chapter_scopes and not self._is_chapter_in_scope(chapter_order):
                        result_data = {"success": False, "error": "章节超出范围"}
                    else:
                        offset = params.get("offset", 0)
                        limit = params.get("limit", 50)
                        if isinstance(offset, str) and offset.isdigit():
                            offset = int(offset)
                        if isinstance(limit, str) and limit.isdigit():
                            limit = int(limit)
                        if not isinstance(offset, int):
                            offset = 0
                        if not isinstance(limit, int):
                            limit = 1
                        if offset < 0:
                            offset = 0
                        if limit <= 0:
                            limit = 1
                        remaining = self._get_chapter_remaining_reads(chapter_order)
                        if remaining is not None and remaining <= 0:
                            result_data = {"success": False, "error": "该章节读取预算已用尽"}
                        else:
                            if remaining is not None:
                                limit = min(limit, remaining)
                            if read_budget is not None:
                                limit = min(limit, read_budget)
                            if limit <= 0:
                                result_data = {"success": False, "error": "没有可读取的段落（可能超出范围）"}
                            else:
                                params["work_id"] = self.work_id
                                params["chapter_order"] = chapter_order
                                params["offset"] = offset
                                params["limit"] = limit
                                result = await read_paragraphs.ainvoke(params)
                                result_data = json.loads(result) if isinstance(result, str) else result
                else:
                    # 确保 list_paragraphs 覆盖候选段落区间（用于 node_id/范围校验）
                    try:
                        missing_ranges: Dict[int, Set[int]] = {}
                        for item in items:
                            if not isinstance(item, dict):
                                continue
                            chapter_order = item.get("chapter_order") or item.get("chapter")
                            paragraph_index = _pick_first_defined(item, ("paragraph_index", "paragraph", "index"))
                            if isinstance(chapter_order, str) and chapter_order.isdigit():
                                chapter_order = int(chapter_order)
                            if isinstance(paragraph_index, str) and paragraph_index.isdigit():
                                paragraph_index = int(paragraph_index)
                            if not isinstance(chapter_order, int) or not isinstance(paragraph_index, int):
                                continue
                            if self.chapter_scopes and not self._is_chapter_in_scope(chapter_order):
                                continue
                            if self._is_paragraph_index_listed(chapter_order, paragraph_index):
                                continue
                            offset = (paragraph_index // LIST_PARAGRAPHS_PAGE_SIZE) * LIST_PARAGRAPHS_PAGE_SIZE
                            missing_ranges.setdefault(chapter_order, set()).add(offset)
                        for chapter_order, offsets in missing_ranges.items():
                            for offset in sorted(offsets):
                                list_params = {
                                    "work_id": self.work_id,
                                    "chapter_order": chapter_order,
                                    "offset": offset,
                                    "limit": LIST_PARAGRAPHS_PAGE_SIZE,
                                    "preview_len": 0
                                }
                                list_result = await list_paragraphs.ainvoke(list_params)
                                list_data = json.loads(list_result) if isinstance(list_result, str) else list_result
                                if isinstance(list_data, dict) and list_data.get("success"):
                                    self.flow_listed_paragraphs.add(chapter_order)
                                    self._cache_paragraph_index_map(chapter_order, list_data)
                                    self._record_listed_paragraph_range(
                                        chapter_order=chapter_order,
                                        offset=offset,
                                        limit=LIST_PARAGRAPHS_PAGE_SIZE,
                                        total=list_data.get("total_paragraphs"),
                                        approximate=bool(list_data.get("approximate"))
                                    )
                    except Exception:
                        pass
                    filtered_items = []
                    remaining_by_chapter: Dict[int, Optional[int]] = {}
                    filter_stats = {
                        "total": len(items),
                        "invalid_items": 0,
                        "out_of_scope": 0,
                        "already_read": 0,
                        "chapter_budget_exhausted": 0
                    }
                    for item in items:
                        if not isinstance(item, dict):
                            filter_stats["invalid_items"] += 1
                            continue
                        chapter_order = item.get("chapter_order") or item.get("chapter")
                        chapter_id = item.get("chapter_id") or params.get("chapter_id") or ""
                        if isinstance(chapter_order, str) and chapter_order.isdigit():
                            chapter_order = int(chapter_order)
                            item["chapter_order"] = chapter_order
                        if not isinstance(chapter_order, int) and chapter_id:
                            if chapter_id_map is None:
                                chapters = await self._get_chapter_list()
                                chapter_id_map = {}
                                for ch in chapters:
                                    order_val = ch.get("order")
                                    if not isinstance(order_val, int):
                                        continue
                                    for key in (ch.get("id"), ch.get("chapter_id")):
                                        if key:
                                            chapter_id_map[str(key)] = order_val
                            chapter_order = chapter_id_map.get(str(chapter_id))
                            if isinstance(chapter_order, int):
                                item["chapter_order"] = chapter_order

                        paragraph_index = _pick_first_defined(item, ("paragraph_index", "paragraph", "index"))
                        if isinstance(paragraph_index, str) and paragraph_index.isdigit():
                            paragraph_index = int(paragraph_index)
                        if not isinstance(paragraph_index, int):
                            node_id = item.get("node_id") or ""
                            if node_id and isinstance(chapter_order, int):
                                mapped_index = self.paragraph_node_id_cache.get(chapter_order, {}).get(node_id)
                                if isinstance(mapped_index, int):
                                    paragraph_index = mapped_index
                        if not isinstance(chapter_order, int) or not isinstance(paragraph_index, int):
                            filter_stats["invalid_items"] += 1
                            continue
                        item["paragraph_index"] = paragraph_index
                        if self.chapter_scopes and not self._is_chapter_in_scope(chapter_order):
                            filter_stats["out_of_scope"] += 1
                            continue
                        if not self.state.should_read_paragraph(chapter_order, paragraph_index):
                            filter_stats["already_read"] += 1
                            continue
                        remaining = remaining_by_chapter.get(chapter_order)
                        if remaining is None:
                            remaining = self._get_chapter_remaining_reads(chapter_order)
                            remaining_by_chapter[chapter_order] = remaining
                        if remaining is not None and remaining <= 0:
                            filter_stats["chapter_budget_exhausted"] += 1
                            continue
                        filtered_items.append(item)
                        if remaining is not None:
                            remaining_by_chapter[chapter_order] = remaining - 1
                    items = filtered_items
                    if read_budget is not None and read_budget < len(items):
                        filter_stats["read_budget_trimmed"] = len(items) - read_budget
                        items = items[:read_budget]
                    if not items:
                        parts = []
                        if filter_stats["invalid_items"]:
                            parts.append(f"无效{filter_stats['invalid_items']}")
                        if filter_stats["out_of_scope"]:
                            parts.append(f"超范围{filter_stats['out_of_scope']}")
                        if filter_stats["already_read"]:
                            parts.append(f"已读{filter_stats['already_read']}")
                        if filter_stats["chapter_budget_exhausted"]:
                            parts.append(f"预算{filter_stats['chapter_budget_exhausted']}")
                        if filter_stats.get("read_budget_trimmed"):
                            parts.append(f"预算裁剪{filter_stats['read_budget_trimmed']}")
                        empty_reason = "没有可读取的段落"
                        if parts:
                            empty_reason = f"没有可读取的段落（{'，'.join(parts)}）"
                        result_data = {
                            "success": False,
                            "error": empty_reason,
                            "empty_reason": empty_reason,
                            "count": 0,
                            "errors": 0,
                            "invalid_items": filter_stats["invalid_items"],
                            "filtered_counts": filter_stats,
                            "index_base": "zero"
                        }
                        logger.info(
                            "[ExploreTool] read_paragraphs filtered counts: total=%s invalid=%s out_of_scope=%s already_read=%s budget=%s",
                            filter_stats["total"],
                            filter_stats["invalid_items"],
                            filter_stats["out_of_scope"],
                            filter_stats["already_read"],
                            filter_stats["chapter_budget_exhausted"]
                        )
                    else:
                        params["work_id"] = self.work_id
                        params["items"] = items
                        params["index_base"] = "zero"
                        result = await read_paragraphs.ainvoke(params)
                        result_data = json.loads(result) if isinstance(result, str) else result
                count_hint = params.get("limit") if use_range else (len(items) if isinstance(items, list) else 0)
                logger.info(
                    "[ExploreTool] done=%s success=%s count=%s index_base=%s",
                    tool_name,
                    bool(result_data.get("success")) if isinstance(result_data, dict) else False,
                    count_hint,
                    params.get("index_base")
                )
                actual_count = result_data.get("count") if isinstance(result_data, dict) else None
                if isinstance(result_data, dict) and (not result_data.get("success") or actual_count == 0):
                    logger.info(
                        "[ExploreTool] read_paragraphs failed details: empty_reason=%s error=%s invalid_items=%s index_base=%s",
                        result_data.get("empty_reason"),
                        result_data.get("error"),
                        result_data.get("invalid_items"),
                        result_data.get("index_base")
                    )
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
                    if not self.state.should_read_paragraph(chapter_order, paragraph_index):
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
                        "node_id": entry.get("node_id") or "",
                        "is_target": not use_range
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
        """构建已收集信息的摘要（仅提供样本，不做统计驱动）"""
        lines = []

        if self.chapter_scopes:
            lines.append(f"- 任务章节范围：{_format_scope_ranges(self.chapter_scopes)}")

        # 证据样本（不展示数量统计）
        if self.state.evidences:
            lines.append("- 证据片段样本：")
            for e in self.state.evidences[:8]:
                para_label = f"第{e.paragraph_index}段" if isinstance(e.paragraph_index, int) else "段落未知"
                lines.append(f"  · 第{e.chapter_order}章{para_label}: {e.text[:60]}...")
        else:
            lines.append("- 证据片段：无")

        # 段落读取样本
        if self.state.paragraphs:
            lines.append("- 已读段落样本：")
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

    # ==================== 辅助方法 ====================

    def _search_worldview_for_keywords(self, keywords: List[str]) -> List[Dict]:
        """在已加载的世界观中搜索关键词匹配

        Args:
            keywords: 搜索关键词列表

        Returns:
            匹配的世界观条目列表，每个条目包含 name, description, category
        """
        if not self.state.worldview:
            return []

        matches = []
        seen_names = set()

        for category, items in self.state.worldview.items():
            for item in items:
                name = item.name if hasattr(item, 'name') else item.get('name', '')
                description = item.description if hasattr(item, 'description') else item.get('description', '')

                # 检查关键词是否匹配名称或描述
                for kw in keywords:
                    kw_lower = kw.lower()
                    name_lower = name.lower() if name else ""
                    desc_lower = description.lower() if description else ""

                    if kw_lower in name_lower or kw_lower in desc_lower:
                        if name not in seen_names:
                            seen_names.add(name)
                            matches.append({
                                "name": name,
                                "description": description,
                                "category": category
                            })
                        break  # 一个 item 只添加一次

        return matches

    def _generate_hits_summary(self, results: List[Dict], keywords: List[str]) -> str:
        """生成搜索结果摘要（类似 OpenCode 的 output truncation）

        策略：
        - 提取关键信息（章节、段落、内容片段）
        - 支持世界观结果
        - 限制在 100 字符以内
        - 突出与目标任务相关的信息
        """
        if not results:
            return "无命中"

        # 统计章节分布和世界观命中
        chapters = set()
        worldview_names = []
        snippets = []
        first_location = None
        for r in results[:5]:  # 只看前5条
            if r.get("source") == "worldview":
                wv_name = r.get("worldview_name", "")
                if wv_name:
                    worldview_names.append(wv_name)
            else:
                ch = r.get("chapter_order")
                if isinstance(ch, int):
                    chapters.add(ch)
                pi = r.get("paragraph_index")
                if isinstance(pi, str) and pi.isdigit():
                    pi = int(pi)
                if first_location is None and isinstance(ch, int) and isinstance(pi, int):
                    first_location = (ch, pi)
            snippet = r.get("snippet") or r.get("content") or r.get("text") or ""
            if snippet:
                snippets.append(snippet[:40])

        # 生成摘要
        parts = []
        parts.append(f"{len(results)}条命中")
        if worldview_names:
            parts.append(f"世界观:{','.join(worldview_names[:2])}")
        if first_location:
            ch, pi = first_location
            parts.append(f"首条第{ch}章第{pi}段")
        elif chapters:
            if len(chapters) == 1:
                parts.append(f"第{list(chapters)[0]}章")
            else:
                parts.append(f"覆盖第{min(chapters)}-{max(chapters)}章")
        if snippets and not worldview_names:  # 有世界观时优先显示世界观名称
            preview = snippets[0][:30] + "..." if len(snippets[0]) > 30 else snippets[0]
            parts.append(f"如「{preview}」")

        summary = ", ".join(parts)
        return summary[:100]  # 限制长度

    async def _generate_analysis(self) -> str:
        """生成分析总结（优先使用 AI 生成的）"""
        # 优先使用最后一轮 AI 生成的 summary
        if self.state.rounds:
            last_round = self.state.rounds[-1]
            if last_round.summary:
                return last_round.summary

        summary, _ = await self._generate_summary_and_next_action()
        if summary:
            return summary

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

    async def _generate_summary_and_next_action(self) -> Tuple[str, str]:
        """使用 LLM 生成探索总结与下一步行动"""
        from app.services.agent.model_selector import TaskType

        ai_service = _get_ai_service()
        stats = self.state.get_stats()
        summary_context = self._build_collected_summary()
        prompt = f"""你是只读探索器，请基于以下信息生成「探索总结」与「下一步行动」。

目标任务：{self.target_task}
统计信息：轮次{stats.get('rounds_count', 0)}，证据{stats.get('total_evidences', 0)}，段落{stats.get('total_paragraphs', 0)}，章节{stats.get('total_chapters', 0)}。

已收集信息摘要：
{summary_context}

输出要求：
1) 输出两行：
探索总结：<一句话总结>
下一步行动：<一句话行动>
2) 只输出上述两行，不要其他内容。
"""
        try:
            response = await ai_service.call_ai(
                system_prompt="你是只读探索器。只输出两行总结与行动。",
                user_prompt=prompt,
                max_tokens=200,
                temperature=0.2,
                task_type=TaskType.SIMPLE_QA
            )
        except Exception as e:
            logger.warning(f"[ContentExplorer] 总结生成失败: {e}")
            return "", ""

        text = (response or "").strip()
        summary = ""
        next_action = ""
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("探索总结："):
                summary = line.replace("探索总结：", "").strip()
            elif line.startswith("下一步行动："):
                next_action = line.replace("下一步行动：", "").strip()

        if not summary and text:
            summary = text[:200]
        return summary, next_action

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

        # 使用 AI 生成的总结（如果有的话）
        summary = result.analysis  # 默认使用硬编码的分析
        next_action = ""  # 不展示下一步行动

        if last_round:
            # 优先使用 AI 生成的总结
            if last_round.summary:
                summary = last_round.summary
        else:
            auto_summary, auto_next = await self._generate_summary_and_next_action()
            if auto_summary:
                summary = auto_summary

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
    max_rounds: int = 200,
    max_tool_calls: Optional[int] = None,
    max_read_paragraphs: Optional[int] = None,
    output_mode: str = "full",
    require_paragraph_index: Optional[bool] = None,
    force_global_search: Optional[bool] = None,
    user_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
    use_cache: bool = True,
    force_refresh: bool = False
) -> str:
    """深度探索内容，收集完成任务所需的所有信息

    Args:
        work_id: 作品ID（UUID格式，必需）
        target_task: 目标任务描述（如"续写第6章，需要了解主角性格和当前剧情"）
        search_keywords: 搜索关键词列表（由规划阶段直接提供，优先使用）
        max_rounds: 最大探索轮次（默认100轮）
        max_tool_calls: 工具调用上限（仅 tool_loop 生效）
        max_read_paragraphs: 读取段落上限（可选，不传则不设全局上限）
        output_mode: 输出模式（evidence_only/full，默认 full；full 返回前端展示字段）
        require_paragraph_index: 是否强制要求段落索引（编辑类请求应为 True）
        force_global_search: 是否忽略章节范围（用于引用句子但未指定章节时）
        user_id: 用户ID（可选）
        conversation_id: 会话ID（可选，用于共享缓存）
        use_cache: 是否启用 Redis 结果缓存（默认 True）
        force_refresh: 是否跳过缓存强制刷新（默认 False）

    Returns:
        JSON格式的探索结果
    """
    logger.info(f"[explore_content] 开始: work_id={work_id}, target={target_task[:50]}...")
    if search_keywords:
        logger.info(f"[explore_content] 规划传入关键词: {search_keywords[:10]}")
    output_mode_norm = (output_mode or "evidence_only").strip().lower()
    evidence_only_output = output_mode_norm in ("evidence", "evidence_only", "minimal")
    use_cache = bool(use_cache)
    force_refresh = bool(force_refresh)
    force_global_search = bool(force_global_search)

    target_task_for_explorer = target_task or ""
    if force_global_search:
        target_task_for_explorer = _strip_chapter_hint_for_global_search(target_task_for_explorer)
        if "全文" not in target_task_for_explorer and "全书" not in target_task_for_explorer:
            target_task_for_explorer = f"{target_task_for_explorer}（全文范围搜索）"
        logger.info("[explore_content] force_global_search 已启用：忽略章节范围")

    # 工具内事件：若有 stream handler，则由工具实时发射
    stream_handler = get_stream_event_handler()
    emit_callback = stream_handler.emit_flow_event if stream_handler else None
    step_id_value = get_explore_step_id()

    async def _attach_artifact(result_payload: Dict[str, Any]) -> None:
        """保存 Explore 完整结果到 Artifact，并注入 artifact_id/preview"""
        try:
            metadata = {
                "target_task": target_task,
                "output_mode": output_mode_norm,
                "force_global_search": force_global_search,
                "require_paragraph_index": bool(require_paragraph_index) if require_paragraph_index is not None else None,
                "search_keywords": search_keywords or []
            }
            artifact_info = await _save_explore_artifact(
                payload=result_payload,
                work_id=work_id,
                user_id=user_id,
                metadata=metadata
            )
        except Exception as exc:
            logger.debug(f"[explore_content] Artifact 保存失败: {exc}")
            return

        if artifact_info.get("stored"):
            artifact_id = artifact_info.get("artifact_id") or ""
            preview_source = result_payload.get("explore_summary") or result_payload.get("context_for_task") or ""
            if not preview_source:
                evidences = result_payload.get("evidences") or []
                if isinstance(evidences, list):
                    preview_source = "；".join(
                        [str(item.get("text", "")) for item in evidences[:3] if isinstance(item, dict)]
                    )
            preview_text = _truncate_text(preview_source, 1200)
            result_payload["artifact_id"] = artifact_id
            result_payload["artifact_preview"] = preview_text
            result_payload["artifact_created_at"] = artifact_info.get("created_at")
            # 写入 Redis 会话状态（便于下轮取回）
            if conversation_id:
                try:
                    await _record_session_artifact(
                        session_id=conversation_id,
                        artifact_id=artifact_id,
                        work_id=work_id,
                        created_at=artifact_info.get("created_at"),
                        preview=preview_text
                    )
                except Exception as exc:
                    logger.debug(f"[explore_content] 记录会话 artifact 失败: {exc}")
            # 将 artifact_id 写入 explore_summary，便于后续按需取回
            if result_payload.get("explore_summary"):
                result_payload["explore_summary"] = (
                    str(result_payload.get("explore_summary"))
                    + f"\n\n[artifact_id] {artifact_id}"
                )
            else:
                result_payload["explore_summary"] = f"[artifact_id] {artifact_id}"
        else:
            result_payload["artifact_id"] = ""
            result_payload["artifact_skipped_reason"] = artifact_info.get("reason", "unknown")
    events_emitted = emit_callback is not None

    chapter_scopes = _parse_chapter_scopes(target_task_for_explorer)
    if force_global_search:
        chapter_scopes = []
    cache_key = ""
    if use_cache:
        cache_key = _build_explore_result_cache_key(
            work_id=work_id,
            user_id=user_id,
            chapter_scopes=chapter_scopes,
            target_task=target_task_for_explorer,
            search_keywords=search_keywords,
            output_mode=output_mode_norm,
            require_paragraph_index=require_paragraph_index,
            force_global_search=force_global_search
        )
        if cache_key and not force_refresh:
            cached_payload = await _get_cached_explore_result(cache_key)
            if cached_payload:
                cached_payload = _decorate_cached_payload(cached_payload, cache_key)
                return json.dumps(cached_payload, ensure_ascii=False, indent=2)

    shared_cache_key = _build_explore_shared_key(
        work_id,
        user_id,
        conversation_id,
        chapter_scopes,
        target_task_for_explorer
    )
    shared_state = None
    if shared_cache_key:
        cached_state = _EXPLORE_SHARED_CACHE.get(shared_cache_key)
        if isinstance(cached_state, ExploreState):
            shared_state = cached_state

        explorer = ContentExplorer(
            work_id=work_id,
            target_task=target_task_for_explorer,
            max_rounds=max_rounds,
            emit_callback=emit_callback,
            step_id=step_id_value,
            search_keywords=search_keywords,
            max_tool_calls=max_tool_calls,
            max_read_paragraphs=max_read_paragraphs,
            require_paragraph_index=require_paragraph_index,
            force_global_search=force_global_search,
            user_id=user_id
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
        result = await explorer.explore_tool_loop()
        # 仅对“已读取原文”的候选做唯一性选择；低置信时保留多候选供确认
        selection_keywords = _normalize_keywords(search_keywords)
        for attempt in explorer.state.get_recent_query_attempts(limit=20):
            for kw in attempt.keywords:
                if kw and kw not in selection_keywords:
                    selection_keywords.append(kw)
        _select_unique_target_paragraphs(result, target_task_for_explorer, selection_keywords)

        if shared_cache_key:
            cached_state = _EXPLORE_SHARED_CACHE.get(shared_cache_key)
            if isinstance(cached_state, ExploreState):
                merged_state = _merge_explore_states(cached_state, explorer.state)
                _EXPLORE_SHARED_CACHE.set(shared_cache_key, merged_state)
            else:
                _EXPLORE_SHARED_CACHE.set(shared_cache_key, _clone_explore_state(explorer.state))

        node_id_map = _build_node_id_map(result)

        # 最小章节映射（用于 locate_targets 的 chapter_id）
        chapters_by_order: Dict[int, Dict[str, Any]] = {}

        def _add_min_chapter(chapter_order: int, chapter_id: str = "", chapter_title: str = "") -> None:
            if not chapter_order:
                return
            entry = chapters_by_order.get(chapter_order)
            if not entry:
                entry = {
                    "id": "",
                    "chapter_id": "",
                    "title": "",
                    "order": chapter_order
                }
            if chapter_id and not entry.get("id"):
                entry["id"] = chapter_id
            if chapter_title and not entry.get("title"):
                entry["title"] = chapter_title
            if entry.get("id") and not entry.get("chapter_id"):
                entry["chapter_id"] = entry["id"]
            chapters_by_order[chapter_order] = entry

        for e in result.evidences:
            _add_min_chapter(e.chapter_order, e.chapter_id, e.chapter_title)

        for p in result.paragraphs:
            _add_min_chapter(p.chapter_order, "", p.chapter_title)

        if work_id and chapters_by_order:
            try:
                from app.services.agent.langgraph_tools import resolve_chapter_id
                for chapter_order, entry in chapters_by_order.items():
                    if entry.get("id"):
                        continue
                    resolved_id, _ = await resolve_chapter_id(work_id, str(chapter_order))
                    if resolved_id:
                        entry["id"] = resolved_id
                        entry["chapter_id"] = resolved_id
            except Exception:
                pass

        locate_targets = _build_locate_targets(
            result,
            chapters_by_order,
            node_id_map=node_id_map,
            candidates=getattr(result, "search_hits", None)
        )
        evidences_output = _build_evidences_output(result, node_id_map=node_id_map)

        if explorer.require_paragraph_index and not locate_targets:
            has_locatable_chapter_candidate = any(
                isinstance(getattr(hit, "chapter_order", None), int)
                and isinstance(getattr(hit, "paragraph_index", None), int)
                and getattr(hit, "source_type", "") != "worldview"
                for hit in (result.search_hits or [])
            )
            has_read_paragraph = any(
                isinstance(getattr(p, "chapter_order", None), int)
                and isinstance(getattr(p, "paragraph_index", None), int)
                for p in (result.paragraphs or [])
            )
            if not has_locatable_chapter_candidate and not has_read_paragraph:
                search_results = _build_search_results(result, node_id_map=node_id_map)
                frontend_display = to_frontend_display(result)
                frontend_display["search_results"] = search_results
                frontend_display["locate_targets"] = []
                worldview_dict = {}
                for category, items in result.worldview.items():
                    worldview_dict[category] = [
                        {"name": item.name, "description": item.description}
                        for item in items
                    ]
                result_payload = {
                    "success": True,
                    "no_hits": True,
                    "message": "探索未命中可定位章节段落（chapter_order+paragraph_index）。",
                    "evidences": evidences_output,
                    "locate_targets": [],
                    "search_results": search_results,
                    "paragraphs": [],
                    "chapters": [],
                    "worldview": worldview_dict,
                    "analysis": result.analysis,
                    "stats": result.stats,
                    "intent_retrieval_v2": explorer.intent_retrieval_v2,
                    "intent_state": explorer.state.iteration_state.to_dict(),
                    "intent_spec": explorer.state.latest_intent_spec,
                    "query_program": explorer.state.latest_query_program,
                    "frontend_display": frontend_display
                }
                await _attach_artifact(result_payload)
                if use_cache and cache_key:
                    await _set_cached_explore_result(cache_key, result_payload)
                return json.dumps(result_payload, ensure_ascii=False, indent=2)

            message = "探索未产出可定位段落（缺少 paragraph_index/node_id），请先用 list_paragraphs/read_paragraphs 精确读取目标段落。"
            result_payload = {
                "success": False,
                "error": "missing_locate_targets",
                "message": message,
                "evidences": evidences_output,
                "locate_targets": locate_targets
            }
            if use_cache and cache_key:
                await _set_cached_explore_result(cache_key, result_payload)
            return json.dumps(result_payload, ensure_ascii=False, indent=2)

        if evidence_only_output:
            result_payload = {
                "success": True,
                "evidences": evidences_output,
                "locate_targets": locate_targets,
                "intent_retrieval_v2": explorer.intent_retrieval_v2,
                "intent_state": explorer.state.iteration_state.to_dict(),
                "intent_spec": explorer.state.latest_intent_spec,
                "query_program": explorer.state.latest_query_program,
            }
            await _attach_artifact(result_payload)
            if use_cache and cache_key:
                await _set_cached_explore_result(cache_key, result_payload)
            return json.dumps(result_payload, ensure_ascii=False, indent=2)

        # full 输出（兼容旧字段）
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

        worldview_dict = {}
        for category, items in result.worldview.items():
            worldview_dict[category] = [
                {"name": item.name, "description": item.description}
                for item in items
            ]

        explore_summary = _build_explore_summary(result)
        frontend_display = to_frontend_display(result)
        search_results = _build_search_results(result, node_id_map=node_id_map)
        frontend_display["search_results"] = search_results
        frontend_display["locate_targets"] = locate_targets

        result_payload = {
            "success": True,
            "work_id": work_id,
            "target_task": target_task,
            "analysis": result.analysis,
            "stats": result.stats,
            "stop_reason": result.stop_reason,
            "total_duration_ms": result.total_duration_ms,
            "frontend_display": frontend_display,
            "context_for_task": build_context_for_task(result),
            "explore_summary": explore_summary,
            "evidences": evidences_output,
            "locate_targets": locate_targets,
            "chapters": chapters_list,
            "results": chapters_list,
            "worldview": worldview_dict,
            "events_emitted": events_emitted,
            "intent_retrieval_v2": explorer.intent_retrieval_v2,
            "intent_state": explorer.state.iteration_state.to_dict(),
            "intent_spec": explorer.state.latest_intent_spec,
            "query_program": explorer.state.latest_query_program,
        }
        await _attach_artifact(result_payload)
        if use_cache and cache_key:
            await _set_cached_explore_result(cache_key, result_payload)
        return json.dumps(result_payload, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"[explore_content] 失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "work_id": work_id
        }, ensure_ascii=False)


@register_as_tool("load_explore_artifact", "explore", "读取已保存的探索结果")
async def load_explore_artifact(
    artifact_id: str,
    work_id: str,
    user_id: Optional[str] = None,
    mode: str = "full",
    max_chars: Optional[int] = None
) -> str:
    """按 artifact_id 读取 Explore 结果（可选 summary/metadata/full）"""
    result = await _load_explore_artifact(
        artifact_id=artifact_id,
        work_id=work_id,
        user_id=user_id,
        mode=mode,
        max_chars=max_chars
    )
    return json.dumps(result, ensure_ascii=False, indent=2)
