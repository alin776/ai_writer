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

    range_match = re.search(r"第\s*(\d+)\s*[到至\-~—～]\s*(\d+)\s*章", text)
    if range_match:
        start = int(range_match.group(1))
        end = int(range_match.group(2))
        return (min(start, end), max(start, end))

    range_cn_match = re.search(r"第\s*([一二两三四五六七八九十]+)\s*[到至\-~—～]\s*([一二两三四五六七八九十]+)\s*章", text)
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

    for match in re.finditer(r"第\s*(\d+)\s*[到至\-~—～]\s*(\d+)\s*章", text):
        start = int(match.group(1))
        end = int(match.group(2))
        scopes.append((min(start, end), max(start, end)))

    for match in re.finditer(r"第\s*([一二两三四五六七八九十]+)\s*[到至\-~—～]\s*([一二两三四五六七八九十]+)\s*章", text):
        start = _chinese_to_int(match.group(1))
        end = _chinese_to_int(match.group(2))
        if isinstance(start, int) and isinstance(end, int):
            scopes.append((min(start, end), max(start, end)))

    # 兼容“章节1-2”“章节(1-2, 34-35)”等写法
    if "章节" in text:
        for match in re.finditer(r"章节\s*\(?\s*(\d+)\s*[到至\-~—～]\s*(\d+)", text):
            start = int(match.group(1))
            end = int(match.group(2))
            scopes.append((min(start, end), max(start, end)))
        for match in re.finditer(r"章节\s*\(?\s*([一二两三四五六七八九十]+)\s*[到至\-~—～]\s*([一二两三四五六七八九十]+)", text):
            start = _chinese_to_int(match.group(1))
            end = _chinese_to_int(match.group(2))
            if isinstance(start, int) and isinstance(end, int):
                scopes.append((min(start, end), max(start, end)))
        for match in re.finditer(r"(\d+)\s*[到至\-~—～]\s*(\d+)", text):
            start = int(match.group(1))
            end = int(match.group(2))
            scopes.append((min(start, end), max(start, end)))

    # 兼容“1-2章”写法
    for match in re.finditer(r"(\d+)\s*[到至\-~—～]\s*(\d+)\s*章", text):
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
    title_order_map: Dict[int, int]
) -> List[Tuple[int, int]]:
    if not scopes or not title_order_map:
        return []
    mapped: List[Tuple[int, int]] = []
    for start, end in scopes:
        orders = [
            order for title_no, order in title_order_map.items()
            if start <= title_no <= end
        ]
        if not orders:
            continue
        mapped.append((min(orders), max(orders)))
    if not mapped:
        return []
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
class ExplorationPlan:
    """AI 生成的探索计划（第0步）"""
    key_entities: List[str]           # 关键实体
    aspects_to_find: List[str]        # 需要了解的方面
    initial_queries: List[str]        # 初始搜索词
    understanding: str                # AI 对任务的理解


@dataclass
class RoundPlan:
    """AI 生成的单轮行动计划（V3：区分精确搜索和语义搜索）"""
    exact_keywords: List[str]         # 精确搜索关键词（找具体实体：人名、地名）
    semantic_queries: List[str]       # 语义搜索 query（找抽象概念：性格、关系）
    chapters_to_read: List[int]       # 本轮要读的章节
    paragraphs_to_read: List[Dict]    # 本轮要读的段落 [{"chapter": 3, "paragraph": 15}]
    reason: str                       # AI 决策理由


@dataclass
class SufficiencyAssessment:
    """AI 对信息充足性的评估"""
    sufficient: bool                  # 是否充足
    coverage: str                     # 覆盖情况描述
    missing: List[str]                # 缺失的信息
    summary: str = ""                 # 探索总结（AI生成）
    next_action: str = ""             # 下一步行动（AI生成）


@dataclass
class EvidenceExtraction:
    """
    AI 提取的客观指标（V3.4：分离提取与判断）

    核心理念：让 AI 只做客观提取，代码做确定性判断
    - AI 提取：关键词覆盖、章节范围、内容质量等客观指标
    - 代码判断：基于提取结果用规则判断是否充足
    """
    # 关键词覆盖情况（AI 提取）
    keyword_coverage: Dict[str, bool]  # {"林仙": True, "叶凡": True, "系统10086": False}

    # 章节覆盖情况（AI 提取）
    chapters_with_evidence: List[int]  # [1, 5, 10, 15]

    # 内容质量评估（AI 提取）
    has_direct_quotes: bool           # 是否有直接引用原文
    has_character_interactions: bool  # 是否有人物互动描写
    has_plot_details: bool            # 是否有情节细节

    # 探索总结（AI 生成，用于后续任务）
    summary: str                      # 探索过程和收集到的关键内容
    next_action: str                  # 下一步将如何完成任务

    # 可选：AI 认为可能缺失的内容（仅供参考，不影响判断）
    potential_gaps: List[str] = None  # ["试探博弈阶段", "具体对话内容"]

    def __post_init__(self):
        if self.potential_gaps is None:
            self.potential_gaps = []


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
    # 搜索到的所有证据片段

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
            if source_type not in ("paragraph", "read_paragraph", "exact_search"):
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
            chapter_title=chapter_title
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
            round_idx=round_idx
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
    if round_data.sufficient:
        return "通过"
    elif round_data.missing_items:
        return "覆盖不足"
    else:
        return "补齐要点"


def _get_status_text(round_data: ExploreRound) -> str:
    """获取状态文本（灰色显示）"""
    if round_data.missing_items:
        return ""  # 有缺失项时不显示状态文本
    elif round_data.sufficient:
        return "覆盖度达标"
    else:
        return "补漏完成"


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
        paragraphs=[],
        chapters={},
        worldview={},
        searched_queries=set(state.searched_queries),
        evidence_keys=set(),
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


def _build_search_results(result: ExploreResult, limit: int = 10) -> List[Dict[str, Any]]:
    """构建兼容 frontend_display.search_results 的精简列表"""
    results: List[Dict[str, Any]] = []
    seen = set()
    evidences = sorted(result.evidences, key=lambda e: e.similarity or 0, reverse=True)
    for e in evidences:
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
            "node_id": node_id_by_index.get(p.paragraph_index)
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
    coverage_label = "未知"
    if last_round and last_round.coverage:
        coverage_label = "充足" if last_round.sufficient else "覆盖不足"
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
            "sufficient": last_round.sufficient if last_round and last_round.coverage else None,
            "coverage": last_round.coverage if last_round and last_round.coverage else "",
            "stats": {
                "worldview": sum(len(items) for items in result.worldview.values()),
                "chapters": _format_chapters_range(result.chapters),
                "evidences": len(result.evidences),
                "coverage": coverage_label
            }
        },
        "step_description": "多轮检索-定位-原文读取，逐轮 review 覆盖度，补漏后输出完整证据链。",
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
        search_keywords: Optional[List[str]] = None
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
        self.emit_callback = emit_callback
        if isinstance(step_id, int) and step_id > 0:
            self.step_id = step_id
        else:
            self.step_id = 1
        self.state = ExploreState()
        self.start_time = get_utc_now()
        self.exploration_plan: Optional[ExplorationPlan] = None  # AI 生成的探索计划
        self.missing_items_from_assessment: List[str] = []  # V3: 阶段2评估后的缺失项，用于指导阶段3
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
            for chapter in chapters:
                title_no = _extract_title_chapter_number(chapter.title or "")
                if not isinstance(title_no, int):
                    continue
                if title_no not in title_order_map:
                    title_order_map[title_no] = chapter.order
            self.title_order_map = title_order_map
            mapped = _map_scopes_to_orders(self.chapter_scopes_raw, title_order_map)
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

        logger.info("[ContentExplorer] ========== 阶段1：精确搜索 ==========")

        # 1. 优先使用规划阶段传入的关键词（最精准）
        if self.search_keywords and len(self.search_keywords) >= 2:
            keywords = self.search_keywords
            logger.info(f"[ContentExplorer] 使用规划传入的关键词: {keywords[:10]}")
        else:
            # 兜底：从任务描述中提取关键词
            keywords = _extract_keywords_for_search(self.target_task)
            if not keywords:
                logger.warning("[ContentExplorer] 未提取到关键词，跳过精确搜索")
                return False
            logger.info(f"[ContentExplorer] 使用提取的关键词: {keywords[:10]}")

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

            # 4. 将结果添加到 evidences
            for r in results:
                # 检查章节范围（二次过滤）
                if self.chapter_scopes and not self._is_chapter_in_scope(r["chapter_order"]):
                    continue

                evidence = {
                    "content": r["text"],
                    "chapter_order": r["chapter_order"],
                    "chapter_title": r.get("chapter_title", ""),
                    "paragraph_index": r["paragraph_index"],
                    "similarity": 1.0,  # 精确匹配
                    "source": "exact_search",
                    "matched_keywords": r.get("matched_keywords", [])
                }

                self.state.add_evidence(
                    evidence,
                    query=",".join(r.get("matched_keywords", [])[:3]),
                    round_idx=0,  # 0 表示精确搜索阶段
                    require_paragraph_index=self.require_paragraph_index,
                    chapter_scope_filter=self._is_chapter_in_scope if self.chapter_scopes else None
                )

            logger.info(f"[ContentExplorer] 精确搜索添加证据: {len(self.state.evidences)} 条")
            return len(self.state.evidences) > 0

        except Exception as e:
            logger.error(f"[ContentExplorer] 精确搜索失败: {e}", exc_info=True)
            return False

    async def explore(self) -> ExploreResult:
        """
        执行探索（V3：精确搜索 + AI 评估 + AI 补充循环）

        流程：
        1. 阶段1：精确搜索（SQL ILIKE，确定性，无 AI 调用）
        2. 阶段2：AI 评估覆盖度（1次 AI 调用）
           - sufficient=true → 直接返回
           - sufficient=false → 保存 missing_items，进入阶段3
        3. 阶段3：AI 补充循环（最多3轮，参考 missing_items）

        Returns:
            ExploreResult: 探索结果
        """
        logger.info(f"[ContentExplorer] 开始探索 V3: work_id={self.work_id}, target={self.target_task[:50]}...")

        stop_reason = "达到最大轮次"

        # ========== 阶段1：精确搜索（确定性，无 AI 调用）==========
        exact_search_success = await self._execute_exact_search_phase()
        exact_evidence_count = len(self.state.evidences)

        # ========== 阶段2：AI 评估覆盖度（无论精确搜索结果数量）==========
        if exact_search_success and exact_evidence_count > 0:
            logger.info(f"[ContentExplorer] 阶段2：AI 评估覆盖度 (精确搜索找到 {exact_evidence_count} 条证据)")

            try:
                # 调用 AI 评估
                assessment = await self._ai_assess_sufficiency()

                # 创建精确搜索轮次记录（包含 AI 评估结果）
                exact_search_round = ExploreRound(
                    round_idx=0,
                    title="精确搜索",
                    tool_calls=[],
                    new_evidences_count=exact_evidence_count,
                    new_paragraphs_count=0,
                    missing_items=assessment.missing if not assessment.sufficient else [],
                    sufficient=assessment.sufficient,
                    reason=assessment.coverage,  # V3.4.1: 使用 AI 评估的覆盖度描述，而非硬编码
                    coverage=assessment.coverage,
                    summary=assessment.summary,
                    next_action=assessment.next_action
                )
                self.state.rounds.append(exact_search_round)

                # 发射轮次事件
                if self.emit_callback:
                    await self._emit_round_event(exact_search_round)

                # V3 核心改动：AI 判断充足则直接返回（仅1次 AI 调用）
                if assessment.sufficient:
                    logger.info(f"[ContentExplorer] AI 判断信息充足，跳过补充循环: {assessment.coverage}")
                    stop_reason = f"AI 判断信息充足: {assessment.coverage}"

                    total_duration_ms = int((get_utc_now() - self.start_time).total_seconds() * 1000)
                    return ExploreResult(
                        evidences=self.state.evidences,
                        paragraphs=self.state.paragraphs,
                        chapters=self.state.chapters,
                        worldview=self.state.worldview,
                        analysis=assessment.summary,
                        stats=self.state.get_stats(),
                        rounds=self.state.rounds,
                        stop_reason=stop_reason,
                        total_duration_ms=total_duration_ms
                    )

                # 保存 missing_items 用于阶段3规划
                self.missing_items_from_assessment = assessment.missing
                logger.info(f"[ContentExplorer] AI 评估不足，缺失项: {self.missing_items_from_assessment}")

            except Exception as e:
                logger.warning(f"[ContentExplorer] AI 评估失败，直接进入补充循环: {e}")
                # V3: AI 评估失败时不再用数量判断，直接进入阶段3补充循环
                exact_search_round = ExploreRound(
                    round_idx=0,
                    title="精确搜索",
                    tool_calls=[],
                    new_evidences_count=exact_evidence_count,
                    new_paragraphs_count=0,
                    missing_items=["AI 评估失败，需要补充探索"],
                    sufficient=False,
                    reason="AI 评估异常，进入补充循环",
                    coverage=f"精确搜索找到 {exact_evidence_count} 条证据，待进一步补充",
                    summary=f"通过精确搜索，找到 {exact_evidence_count} 条相关证据。",
                    next_action="启动补充探索以确保信息覆盖完整。"
                )
                self.state.rounds.append(exact_search_round)

                if self.emit_callback:
                    await self._emit_round_event(exact_search_round)
                # 不再用 >=5 条规则返回，直接继续进入阶段3

        # ========== 阶段3：AI 补充循环（如果阶段2评估不足）==========
        logger.info(f"[ContentExplorer] 阶段3：AI 补充循环，当前 {exact_evidence_count} 条证据")

        # 第0步：AI 理解任务
        try:
            self.exploration_plan = await self._ai_understand_task()
            logger.info(f"[ContentExplorer] AI 任务理解完成: {self.exploration_plan.understanding[:100]}...")
        except Exception as e:
            logger.warning(f"[ContentExplorer] AI 任务理解失败，使用默认策略: {e}")
            self.exploration_plan = ExplorationPlan(
                key_entities=[],
                aspects_to_find=[],
                initial_queries=[self.target_task[:30]],
                understanding=self.target_task
            )

        # 限制 AI 补充轮次（最多 3 轮，而不是 10 轮）
        max_supplement_rounds = min(self.max_rounds, 3)

        for round_idx in range(1, max_supplement_rounds + 1):
            round_start = get_utc_now()

            # AI 决定本轮行动
            try:
                round_plan = await self._ai_plan_round(round_idx)
            except Exception as e:
                logger.warning(f"[ContentExplorer] AI 轮次规划失败，使用默认策略: {e}")
                # 首轮优先使用 exploration_plan.initial_queries 作为语义搜索
                default_queries = []
                if round_idx == 1:
                    if self.exploration_plan and self.exploration_plan.initial_queries:
                        default_queries = self.exploration_plan.initial_queries[:3]
                    else:
                        default_queries = [self.target_task[:30]]
                round_plan = RoundPlan(
                    exact_keywords=[],  # V3: 默认不做精确搜索
                    semantic_queries=default_queries,  # V3: 使用语义搜索
                    chapters_to_read=[],
                    paragraphs_to_read=[],
                    reason="默认策略"
                )

            # 执行本轮探索
            round_data = await self._execute_round_with_plan(round_idx, round_plan)
            self.state.rounds.append(round_data)

            # 发射轮次事件
            if self.emit_callback:
                await self._emit_round_event(round_data)

            # AI 评估信息充足性
            try:
                assessment = await self._ai_assess_sufficiency()
                round_data.coverage = assessment.coverage
                round_data.summary = assessment.summary  # 保存 AI 生成的总结
                round_data.next_action = assessment.next_action  # 保存 AI 生成的下一步行动
                reachable_missing, unreachable_missing = self._filter_unreachable_missing(assessment.missing)
                requires_unreachable = _requires_unreachable_items(self.target_task)
                if unreachable_missing:
                    note = "已忽略不可达缺失项：" + "、".join(unreachable_missing[:3])
                    if requires_unreachable:
                        note = "存在不可达缺失项（已标记，不再继续检索）：" + "、".join(unreachable_missing[:3])
                    if round_data.coverage:
                        round_data.coverage = f"{round_data.coverage}（{note}）"
                    else:
                        round_data.coverage = note
                if assessment.sufficient:
                    stop_reason = f"AI 判断信息充足: {assessment.coverage}"
                    round_data.sufficient = True
                    round_data.missing_items = []
                    break
                else:
                    if requires_unreachable and unreachable_missing:
                        stop_reason = "存在不可达缺失项"
                        round_data.sufficient = False
                        round_data.missing_items = reachable_missing + unreachable_missing
                        break
                    if not reachable_missing:
                        stop_reason = "可达信息已覆盖（存在不可达缺失项）"
                        round_data.sufficient = True
                        round_data.missing_items = []
                        break
                    round_data.missing_items = reachable_missing
                    # V3: 更新缺失项，用于下一轮规划
                    self.missing_items_from_assessment = reachable_missing
            except Exception as e:
                logger.warning(f"[ContentExplorer] AI 充足性评估失败: {e}")
                # V3: AI 评估失败时，不使用数量判断，继续循环直到收敛或达到最大轮次
                # 设置兜底信息，让循环继续
                round_data.coverage = f"AI 评估失败，当前 {len(self.state.evidences)} 条证据"
                round_data.missing_items = ["AI 评估失败，继续探索"]

            # 检查是否收敛（连续无新信息）
            if self.state.check_convergence():
                if not round_data.missing_items:
                    stop_reason = "信息收敛"
                    break
                stop_reason = "连续无新增信息（覆盖不足）"
                break

        if stop_reason == "达到最大轮次" and self.state.rounds:
            last_round = self.state.rounds[-1]
            if last_round.missing_items:
                stop_reason = "达到最大轮次（覆盖不足）"

        # 生成分析
        analysis = await self._generate_analysis()

        # 计算总耗时
        total_duration_ms = int((get_utc_now() - self.start_time).total_seconds() * 1000)

        result = ExploreResult(
            evidences=self.state.evidences,
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

    async def _execute_round(self, round_idx: int) -> ExploreRound:
        """执行一轮探索"""
        from app.services.agent.langgraph_tools import search_content, get_writing_context

        tool_calls = []
        new_evidences = 0
        new_paragraphs = 0
        missing_items = []

        # 1. 首轮：获取基础信息
        if round_idx == 1:
            # 获取世界观
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

        # 2. 执行搜索
        search_queries = self._generate_search_queries(round_idx)
        for query in search_queries:
            if not self.state.should_search(query):
                continue

            start = get_utc_now()
            try:
                result = await search_content.ainvoke({
                    "work_id": self.work_id,
                    "query": query,
                    "top_k": 5
                })
                result_data = json.loads(result) if isinstance(result, str) else result
                self.state.record_search(query)

                # 添加证据
                for item in result_data.get("results", []):
                    if self.state.add_evidence(
                        item,
                        query,
                        round_idx,
                        require_paragraph_index=self.require_paragraph_index,
                        chapter_scope_filter=self._is_chapter_in_scope if self.chapter_scopes else None
                    ):
                        new_evidences += 1

                duration = int((get_utc_now() - start).total_seconds() * 1000)
                tool_calls.append(ToolCall(
                    tool_name="search_content",
                    params={"query": query},
                    result=result_data,
                    duration_ms=duration
                ))
            except Exception as e:
                logger.warning(f"[ContentExplorer] 搜索失败: {e}")

        # 3. 读取相关章节
        chapters_to_read = self._filter_chapters_for_reading(
            self._determine_chapters_to_read(),
            limit=2
        )
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

                # 添加章节
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

        # 4. 评估信息充足性
        sufficient, missing = self._evaluate_sufficiency(round_idx)
        missing_items = missing

        return ExploreRound(
            round_idx=round_idx,
            title=_get_round_title(round_idx),
            reason="",  # 旧规则方法无 AI 决策理由
            tool_calls=tool_calls,
            new_evidences_count=new_evidences,
            new_paragraphs_count=new_paragraphs,
            missing_items=missing_items,
            sufficient=sufficient
        )

    # ==================== AI 决策方法 ====================

    async def _ai_understand_task(self) -> ExplorationPlan:
        """
        AI 理解任务，生成探索计划（第0步）

        使用 DEEP_ANALYSIS 任务类型确保理解质量
        """
        from app.services.agent.model_selector import TaskType

        ai_service = _get_ai_service()

        prompt = f"""你是一个信息收集专家。请分析以下任务，理解需要收集哪些信息。

目标任务：{self.target_task}

请分析这个任务：
1. 识别关键实体（人物、地点、物品、概念等）
2. 确定需要了解的方面（关系、事件、状态、背景等）
3. 设计初始搜索策略

请输出 JSON 格式（不要包含其他内容）：
{{
  "key_entities": ["实体1", "实体2"],
  "aspects_to_find": ["方面1", "方面2"],
  "initial_queries": ["搜索词1", "搜索词2"],
  "understanding": "对任务的理解（一句话）"
}}"""

        try:
            response = await ai_service.call_ai(
                system_prompt="你是信息收集专家，擅长分析任务并制定搜索策略。只输出 JSON，不要有其他内容。",
                user_prompt=prompt,
                max_tokens=500,
                temperature=0.3,
                task_type=TaskType.DEEP_ANALYSIS
            )

            # 解析 JSON
            result = self._parse_json_response(response)

            return ExplorationPlan(
                key_entities=result.get("key_entities", []),
                aspects_to_find=result.get("aspects_to_find", []),
                initial_queries=result.get("initial_queries", [self.target_task[:30]]),
                understanding=result.get("understanding", self.target_task)
            )
        except Exception as e:
            logger.warning(f"[ContentExplorer] AI 任务理解解析失败: {e}")
            raise

    async def _ai_plan_round(self, round_idx: int) -> RoundPlan:
        """
        AI 决定本轮行动计划（V3.1：仅语义搜索，删除精确搜索）

        V3.1 改动说明：
        - AI 补充阶段只用语义搜索，不再用精确搜索
        - 精确搜索在阶段1已完成，AI 补充阶段的目的是找"语义相关但字面不同"的内容
        - 删除 exact_keywords 字段，只保留 semantic_queries

        使用 SIMPLE_QA 任务类型优化成本
        """
        from app.services.agent.model_selector import TaskType

        ai_service = _get_ai_service()

        # 构建已收集信息摘要
        collected_summary = self._build_collected_summary()

        # V3: 参考阶段2评估的缺失项
        missing_hint = ""
        if self.missing_items_from_assessment:
            missing_hint = f"\n缺失信息（需重点补充）：{', '.join(self.missing_items_from_assessment[:5])}"

        # 首轮提示 AI 参考 initial_queries
        initial_hint = ""
        if round_idx == 1 and self.exploration_plan and self.exploration_plan.initial_queries:
            initial_hint = f"\n建议的初始搜索词（供参考）：{', '.join(self.exploration_plan.initial_queries)}"

        scope_hint = ""
        if self.chapter_scopes_raw:
            scope_hint = f"\n章节范围约束：仅限{_format_scope_ranges(self.chapter_scopes_raw)}，禁止跨章扩展。"

        # V3.1: 只用语义搜索，删除精确搜索
        example_payload = {
            "semantic_queries": ["某人的性格特点", "两人之间的关系发展", "某事件的具体经过"],
            "chapters_to_read": [],
            "paragraphs_to_read": [{"chapter": 3, "paragraph": 15}],
            "reason": "决策理由"
        }
        example_json = json.dumps(example_payload, ensure_ascii=False, indent=2)

        prompt = f"""你是信息收集专家。请根据当前状态决定本轮行动。

目标任务：{self.target_task}
任务理解：{self.exploration_plan.understanding if self.exploration_plan else self.target_task}
需要了解：{', '.join(self.exploration_plan.aspects_to_find) if self.exploration_plan else '未知'}{missing_hint}{initial_hint}{scope_hint}

当前轮次：第 {round_idx} 轮
已收集信息：
{collected_summary}

已搜索过的关键词（避免重复）：{', '.join(list(self.state.searched_queries)[:10])}

请决定本轮要搜索什么内容：

【搜索策略】使用语义搜索（semantic_queries）：
- 生成 1-3 个语义查询，用于查找缺失的信息
- 查询应该是完整的语义短语，如"女主与主角的关系发展"
- 避免与已搜索过的关键词重复

其他字段说明：
- chapters_to_read: 需要读取哪些章节？（仅在任务明确要求整章/全文时填写，否则留空）
- paragraphs_to_read: 需要精确读取哪些段落？（优先使用，格式为 {{"chapter": 章节号, "paragraph": 段落号}}）

请输出 JSON 格式（不要包含其他内容）：
{example_json}"""

        try:
            response = await ai_service.call_ai(
                system_prompt="你是信息收集专家。只输出 JSON，不要有其他内容。",
                user_prompt=prompt,
                max_tokens=400,
                temperature=0.2,
                task_type=TaskType.SIMPLE_QA
            )

            result = self._parse_json_response(response)

            # V3.1: 只处理语义搜索，删除精确搜索
            semantic_queries = [
                q for q in result.get("semantic_queries", [])
                if q and self.state.should_search(q)
            ]

            # 兼容旧格式：如果 AI 返回 search_queries，当作语义搜索处理
            if not semantic_queries and "search_queries" in result:
                semantic_queries = [
                    q for q in result.get("search_queries", [])
                    if q and self.state.should_search(q)
                ]

            # 过滤已读取的章节
            chapters_to_read = [
                c for c in result.get("chapters_to_read", [])
                if isinstance(c, int) and self.state.should_read_chapter(c)
            ]

            return RoundPlan(
                exact_keywords=[],  # V3.1: AI 补充阶段不再使用精确搜索
                semantic_queries=semantic_queries[:3],  # 最多3个语义搜索
                chapters_to_read=chapters_to_read[:2],  # 最多2个章节
                paragraphs_to_read=result.get("paragraphs_to_read", [])[:3],
                reason=result.get("reason", "")
            )
        except Exception as e:
            logger.warning(f"[ContentExplorer] AI 轮次规划解析失败: {e}")
            raise

    def _calculate_keyword_coverage(self) -> float:
        """
        计算关键词覆盖率（V3.3：用于规则判断）

        Returns:
            float: 覆盖率 0.0-1.0
        """
        if not self.search_keywords:
            return 1.0  # 无关键词时默认充足

        covered = 0
        for kw in self.search_keywords:
            for e in self.state.evidences:
                if kw in e.text or kw in e.query:
                    covered += 1
                    break

        return covered / len(self.search_keywords)

    def _generate_rule_based_summary(self, evidence_count: int, chapter_count: int, keyword_coverage: float) -> str:
        """生成规则判断时的总结"""
        # 收集章节信息
        chapter_orders = sorted(set(e.chapter_order for e in self.state.evidences if e.chapter_order > 0))
        chapter_range = f"第{min(chapter_orders)}-{max(chapter_orders)}章" if chapter_orders else "未知章节"

        # 收集关键词信息
        covered_keywords = []
        if self.search_keywords:
            for kw in self.search_keywords[:5]:
                for e in self.state.evidences:
                    if kw in e.text or kw in e.query:
                        covered_keywords.append(kw)
                        break

        keyword_info = f"，涉及{', '.join(covered_keywords[:3])}等关键内容" if covered_keywords else ""

        return f"通过精确搜索，收集到 {evidence_count} 条证据，覆盖 {chapter_count} 个章节（{chapter_range}）{keyword_info}。"

    def _rule_based_sufficiency(self) -> Optional[SufficiencyAssessment]:
        """
        规则优先的充足性判断（V3.3：减少 AI 不稳定性）

        判断规则：
        1. 证据 ≥ 30 条 且 章节 ≥ 3 个 → 直接充足
        2. 关键词覆盖率 ≥ 80% 且 证据 ≥ 20 条 → 直接充足
        3. 证据 < 5 条 → 直接不足
        4. 其他情况 → 返回 None，交给 AI 判断

        Returns:
            SufficiencyAssessment 或 None（需要 AI 判断）
        """
        evidence_count = len(self.state.evidences)
        chapter_count = len(set(e.chapter_order for e in self.state.evidences if e.chapter_order > 0))
        keyword_coverage = self._calculate_keyword_coverage()

        logger.info(
            "[ContentExplorer] 规则判断: 证据=%d, 章节=%d, 关键词覆盖=%.1f%%",
            evidence_count, chapter_count, keyword_coverage * 100
        )

        # 规则1：数量充足 → 直接通过
        if evidence_count >= 30 and chapter_count >= 3:
            logger.info("[ContentExplorer] 规则1命中: 证据≥30 且 章节≥3 → 直接充足")
            return SufficiencyAssessment(
                sufficient=True,
                coverage=f"证据充足：{evidence_count}条证据，覆盖{chapter_count}个章节",
                missing=[],
                summary=self._generate_rule_based_summary(evidence_count, chapter_count, keyword_coverage),
                next_action="基于充足的背景信息，将执行后续任务。"
            )

        # 规则2：关键词高覆盖 → 直接通过
        if keyword_coverage >= 0.8 and evidence_count >= 20:
            logger.info("[ContentExplorer] 规则2命中: 关键词覆盖≥80%% 且 证据≥20 → 直接充足")
            return SufficiencyAssessment(
                sufficient=True,
                coverage=f"关键词覆盖率：{keyword_coverage:.0%}，证据{evidence_count}条",
                missing=[],
                summary=self._generate_rule_based_summary(evidence_count, chapter_count, keyword_coverage),
                next_action="关键信息已覆盖，将执行后续任务。"
            )

        # 规则3：证据极少 → 直接不足
        if evidence_count < 5:
            logger.info("[ContentExplorer] 规则3命中: 证据<5 → 直接不足")
            return SufficiencyAssessment(
                sufficient=False,
                coverage=f"证据不足：仅{evidence_count}条",
                missing=["需要更多相关信息"],
                summary=f"当前仅收集到 {evidence_count} 条证据，信息量不足。",
                next_action="需要继续探索以收集更多背景信息。"
            )

        # 其他情况：返回 None，交给 AI 判断
        logger.info("[ContentExplorer] 边界情况: 证据=%d, 章节=%d → 交给AI判断", evidence_count, chapter_count)
        return None

    async def _ai_assess_sufficiency(self) -> SufficiencyAssessment:
        """
        AI 评估信息充足性（V3.4：分离提取与判断）

        核心改进：
        - AI 只做客观指标提取（关键词覆盖、内容质量等）
        - 代码规则做确定性判断（基于提取结果）
        - 消除 AI 主观判断的不稳定性

        流程：
        1. AI 提取客观指标 → EvidenceExtraction
        2. 代码规则判断 → SufficiencyAssessment
        """
        # 第一步：AI 提取客观指标
        extraction = await self._ai_extract_evidence_metrics()

        # 第二步：代码规则判断
        return self._evaluate_from_extraction(extraction)

    async def _ai_extract_evidence_metrics(self) -> EvidenceExtraction:
        """
        AI 提取客观指标（不做主观判断）

        V3.4 核心：让 AI 只回答"是什么"，不回答"够不够"
        """
        from app.services.agent.model_selector import TaskType

        ai_service = _get_ai_service()

        collected_summary = self._build_collected_summary()
        evidence_count = len(self.state.evidences)
        chapter_count = len(set(e.chapter_order for e in self.state.evidences if e.chapter_order > 0))

        # 构建关键词列表（用于 AI 检查覆盖情况）
        keywords_to_check = self.search_keywords[:10] if self.search_keywords else []
        keywords_json = ", ".join([f'"{kw}"' for kw in keywords_to_check])

        prompt = f"""你是信息提取专家。请从已收集的信息中提取客观指标，不要做主观判断。

目标任务：{self.target_task}
任务理解：{self.exploration_plan.understanding if self.exploration_plan else self.target_task}
需要了解的方面：{', '.join(self.exploration_plan.aspects_to_find) if self.exploration_plan else '未知'}

已收集信息：
{collected_summary}

【你的任务】提取以下客观指标：

1. **关键词覆盖**：检查以下关键词在证据中是否有相关内容
   关键词列表：[{keywords_json}]
   对每个关键词，判断证据中是否有相关描述（true/false）

2. **章节覆盖**：列出有证据的章节编号

3. **内容质量**：
   - has_direct_quotes: 是否有直接引用原文对话或描述？
   - has_character_interactions: 是否有人物之间的互动描写？
   - has_plot_details: 是否有具体的情节细节？

4. **探索总结**：用2-3句话客观描述收集到的内容（不评价够不够）

5. **下一步行动**：假设信息已经足够，描述将如何完成任务

6. **可能的缺口**（可选）：如果发现某些方面完全没有证据，列出来（最多3项）

请输出 JSON 格式（不要包含其他内容）：
{{
  "keyword_coverage": {{"{keywords_json.replace('"', '').replace(', ', '": true, "')}": true}},
  "chapters_with_evidence": [1, 5, 10],
  "has_direct_quotes": true,
  "has_character_interactions": true,
  "has_plot_details": true,
  "summary": "收集到关于XXX的描述，包括...",
  "next_action": "基于这些信息，将执行...",
  "potential_gaps": ["某方面完全无证据"]
}}"""

        try:
            response = await ai_service.call_ai(
                system_prompt="你是信息提取专家。只提取客观指标，不做主观判断。只输出 JSON。",
                user_prompt=prompt,
                max_tokens=600,
                temperature=0,  # V3.4: 使用 temperature=0 确保提取稳定
                task_type=TaskType.DEEP_ANALYSIS
            )

            logger.info(
                "[ContentExplorer] V3.4 指标提取原始响应(截断): %s",
                _truncate_text(response)
            )

            result = self._parse_json_response(response)

            # 解析关键词覆盖
            keyword_coverage = result.get("keyword_coverage", {})
            if not isinstance(keyword_coverage, dict):
                keyword_coverage = {}

            # 解析章节覆盖
            chapters = result.get("chapters_with_evidence", [])
            if not isinstance(chapters, list):
                chapters = []

            extraction = EvidenceExtraction(
                keyword_coverage=keyword_coverage,
                chapters_with_evidence=chapters,
                has_direct_quotes=bool(result.get("has_direct_quotes", False)),
                has_character_interactions=bool(result.get("has_character_interactions", False)),
                has_plot_details=bool(result.get("has_plot_details", False)),
                summary=result.get("summary", ""),
                next_action=result.get("next_action", ""),
                potential_gaps=result.get("potential_gaps", [])
            )

            logger.info(
                "[ContentExplorer] V3.4 指标提取结果: 关键词覆盖=%d/%d, 章节=%s, 质量=[引用=%s,互动=%s,情节=%s]",
                sum(1 for v in keyword_coverage.values() if v),
                len(keyword_coverage),
                chapters[:5],
                extraction.has_direct_quotes,
                extraction.has_character_interactions,
                extraction.has_plot_details
            )

            return extraction

        except Exception as e:
            logger.warning(f"[ContentExplorer] V3.4 指标提取失败: {e}")
            # 返回默认提取结果，让规则判断兜底
            # 生成兜底的 summary 和 next_action
            evidence_count = len(self.state.evidences)
            chapter_count = len(set(e.chapter_order for e in self.state.evidences if e.chapter_order > 0))
            fallback_summary = f"收集到 {evidence_count} 条证据，覆盖 {chapter_count} 个章节。"
            fallback_action = "基于已收集的信息继续执行任务。"

            return EvidenceExtraction(
                keyword_coverage={},
                chapters_with_evidence=[],
                has_direct_quotes=False,
                has_character_interactions=False,
                has_plot_details=False,
                summary=fallback_summary,
                next_action=fallback_action,
                potential_gaps=[]
            )

    def _evaluate_from_extraction(self, extraction: EvidenceExtraction) -> SufficiencyAssessment:
        """
        基于提取结果进行确定性规则判断（V3.4 核心）

        判断规则（全部用代码实现，100% 确定性）：
        1. 证据 ≥ 30 条 → 充足
        2. 关键词覆盖率 ≥ 70% 且 证据 ≥ 15 条 → 充足
        3. 章节 ≥ 3 个 且 内容质量 ≥ 2/3 → 充足
        4. 证据 < 5 条 → 不足
        5. 其他 → 不足（保守策略）

        注意：关键词覆盖率使用代码计算（_calculate_keyword_coverage），确保 100% 确定性
        """
        evidence_count = len(self.state.evidences)
        chapter_count = len(set(e.chapter_order for e in self.state.evidences if e.chapter_order > 0))

        # V3.4 修正：使用代码计算的关键词覆盖率，确保 100% 确定性
        # 不再依赖 AI 提取的 keyword_coverage，避免潜在的不稳定性
        coverage_rate = self._calculate_keyword_coverage()

        # 计算内容质量分数（仍使用 AI 提取，因为这是语义判断）
        quality_score = sum([
            extraction.has_direct_quotes,
            extraction.has_character_interactions,
            extraction.has_plot_details
        ])

        logger.info(
            "[ContentExplorer] V3.4 规则判断: 证据=%d, 章节=%d, 关键词覆盖=%.1f%%, 质量=%d/3",
            evidence_count, chapter_count, coverage_rate * 100, quality_score
        )

        # ========== 确定性规则判断 ==========

        # 规则0（最高优先级）：关键词覆盖率过低 → 必须继续探索
        # V3.4.1 修复：防止证据多但关键词覆盖低时误判为充足
        if coverage_rate < 0.5 and len(self.search_keywords) >= 3:
            logger.info("[ContentExplorer] V3.4 规则0命中: 关键词覆盖<50%% → 不足（需继续探索）")
            return SufficiencyAssessment(
                sufficient=False,
                coverage=f"关键词覆盖不足：{coverage_rate:.0%}覆盖率，{evidence_count}条证据",
                missing=extraction.potential_gaps[:3] if extraction.potential_gaps else ["关键词覆盖不足，需要继续探索"],
                summary=extraction.summary,
                next_action=extraction.next_action
            )

        # 规则1：证据数量充足 且 关键词覆盖达标
        # V3.4.1 修复：添加覆盖率条件，避免证据多但覆盖低时误判
        if evidence_count >= 30 and coverage_rate >= 0.5:
            logger.info("[ContentExplorer] V3.4 规则1命中: 证据≥30 且 覆盖≥50%% → 充足")
            return SufficiencyAssessment(
                sufficient=True,
                coverage=f"证据充足：{evidence_count}条证据，覆盖{chapter_count}个章节，关键词覆盖{coverage_rate:.0%}",
                missing=[],
                summary=extraction.summary,
                next_action=extraction.next_action
            )

        # 规则2：关键词高覆盖 + 一定证据量
        if coverage_rate >= 0.7 and evidence_count >= 15:
            logger.info("[ContentExplorer] V3.4 规则2命中: 关键词覆盖≥70%% 且 证据≥15 → 充足")
            return SufficiencyAssessment(
                sufficient=True,
                coverage=f"关键词覆盖充足：{coverage_rate:.0%}覆盖率，{evidence_count}条证据",
                missing=[],
                summary=extraction.summary,
                next_action=extraction.next_action
            )

        # 规则3：多章节 + 高质量内容
        if chapter_count >= 3 and quality_score >= 2:
            logger.info("[ContentExplorer] V3.4 规则3命中: 章节≥3 且 质量≥2/3 → 充足")
            return SufficiencyAssessment(
                sufficient=True,
                coverage=f"内容质量充足：覆盖{chapter_count}个章节，质量评分{quality_score}/3",
                missing=[],
                summary=extraction.summary,
                next_action=extraction.next_action
            )

        # 规则4：证据极少
        if evidence_count < 5:
            logger.info("[ContentExplorer] V3.4 规则4命中: 证据<5 → 不足")
            return SufficiencyAssessment(
                sufficient=False,
                coverage=f"证据不足：仅{evidence_count}条",
                missing=extraction.potential_gaps[:3] if extraction.potential_gaps else ["需要更多相关信息"],
                summary=extraction.summary,
                next_action=extraction.next_action
            )

        # 规则5：其他情况（保守判断为不足，进入补充循环）
        logger.info("[ContentExplorer] V3.4 规则5: 边界情况 → 不足（保守策略）")
        return SufficiencyAssessment(
            sufficient=False,
            coverage=f"边界情况：{evidence_count}条证据，{chapter_count}章节，{coverage_rate:.0%}覆盖率",
            missing=extraction.potential_gaps[:3] if extraction.potential_gaps else [],
            summary=extraction.summary,
            next_action=extraction.next_action
        )

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
                                "query": locate_query
                            }
                            if self.chapter_scopes or self.require_paragraph_index:
                                locate_params["allow_global_fallback"] = False
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
                                    "context_after": context_after
                                }, round_idx)
                                if self.require_paragraph_index and target_text:
                                    paragraph_evidence = {
                                        "content": target_text,
                                        "chapter_order": chapter_order,
                                        "paragraph_index": paragraph_index,
                                        "similarity": 1.0,
                                        "source": "paragraph",
                                        "chapter_title": read_data.get("chapter_title", "")
                                    }
                                    if self.state.add_evidence(
                                        paragraph_evidence,
                                        query,
                                        round_idx,
                                        require_paragraph_index=True,
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

                    if self.state.add_evidence(
                        item,
                        query,
                        round_idx,
                        require_paragraph_index=self.require_paragraph_index,
                        chapter_scope_filter=self._is_chapter_in_scope if self.chapter_scopes else None
                    ):
                        new_evidences += 1

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
                        "context_after": context_after
                    }, round_idx)
                    if self.require_paragraph_index and target_text:
                        paragraph_evidence = {
                            "content": target_text,
                            "chapter_order": chapter_order,
                            "paragraph_index": paragraph_index,
                            "similarity": 1.0,
                            "source": "paragraph",
                            "chapter_title": result_data.get("chapter_title", "")
                        }
                        if self.state.add_evidence(
                            paragraph_evidence,
                            "",
                            round_idx,
                            require_paragraph_index=True,
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

    # ==================== 旧规则方法（保留用于兜底）====================

    def _generate_search_queries(self, round_idx: int) -> List[str]:
        """生成搜索查询（旧规则方法，用于兜底）

        改进的查询生成策略：
        1. 首轮：基于目标任务生成查询
        2. 后续轮次：基于目标任务中尚未覆盖的关键词生成查询
        """
        queries = []

        if round_idx == 1:
            # 首轮：基于目标任务生成查询
            # 提取目标任务中的关键词
            keywords = self._extract_target_keywords()
            if keywords:
                # 组合前 3 个关键词作为第一个查询
                queries.append(" ".join(keywords[:3]))
                # 每个关键词单独作为查询
                for kw in keywords[:2]:
                    if kw not in queries[0] or len(kw) >= 4:
                        queries.append(kw)
            # 添加目标任务的前 30 字符作为兜底查询
            queries.append(self.target_task[:30])
        else:
            # 后续轮次：基于未覆盖的关键词生成查询
            target_keywords = self._extract_target_keywords()
            covered_keywords = self._check_keyword_coverage(target_keywords)
            uncovered = [kw for kw in target_keywords if kw not in covered_keywords]

            if uncovered:
                # 优先搜索未覆盖的关键词
                for kw in uncovered[:3]:
                    queries.append(kw)
            else:
                # 如果所有关键词都已覆盖，尝试更细粒度的搜索
                # 使用目标任务中的不同片段
                task_parts = self.target_task.split('。')
                for part in task_parts[:2]:
                    if len(part) >= 5:
                        queries.append(part[:20])

            # 兜底：使用目标任务的不同片段
            if not queries:
                queries.append(self.target_task[20:50] if len(self.target_task) > 50 else self.target_task)

        # 去重并限制数量
        seen = set()
        unique_queries = []
        for q in queries:
            q_clean = q.strip()
            if q_clean and q_clean not in seen and len(q_clean) >= 2:
                seen.add(q_clean)
                unique_queries.append(q_clean)

        return unique_queries[:3]  # 最多3个查询

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

    def _evaluate_sufficiency(self, round_idx: int) -> Tuple[bool, List[str]]:
        """评估信息是否充足

        改进的评估逻辑：
        1. 首轮不能判断为充足（强制多轮探索）
        2. 需要考虑目标任务中的关键词覆盖度
        3. 证据需要来自多个不同章节
        """
        missing = []

        # 规则 1：首轮强制不充足，确保多轮探索
        if round_idx == 1:
            missing.append("首轮探索，需要继续深入")
            return False, missing

        # 规则 2：至少有 5 条证据
        if len(self.state.evidences) < 5:
            missing.append("需要更多证据")

        # 规则 3：章节/段落读取要求
        if self.require_full_chapter:
            if len(self.state.chapters) < 1:
                missing.append("需要读取章节原文")
        else:
            if len(self.state.chapters) < 1 and len(self.state.paragraphs) < 1:
                missing.append("需要读取段落原文")

        # 规则 4：证据需要来自多个章节（多样性检查）
        evidence_chapters = set(e.chapter_order for e in self.state.evidences if e.chapter_order > 0)
        if len(evidence_chapters) < 2 and len(self.state.evidences) >= 5:
            missing.append("证据来源单一，需要从更多章节获取信息")

        # 规则 5：检查目标任务中的关键词覆盖度
        target_keywords = self._extract_target_keywords()
        covered_keywords = self._check_keyword_coverage(target_keywords)
        uncovered = [kw for kw in target_keywords if kw not in covered_keywords]
        if uncovered and len(uncovered) > len(target_keywords) * 0.5:
            missing.append(f"未覆盖关键信息：{', '.join(uncovered[:3])}")

        # 规则 6：3轮后强制认为充足
        if round_idx >= 3:
            logger.info(f"[ContentExplorer] 达到 {round_idx} 轮，强制判断为充足")
            return True, []

        return len(missing) == 0, missing

    def _extract_target_keywords(self) -> List[str]:
        """从目标任务中提取关键词"""
        import re
        # 提取中文词汇和英文词汇
        # 过滤常见停用词
        stopwords = {'的', '了', '是', '在', '和', '与', '以及', '需要', '包括', '所有', '这些', '物品', '信息', '情况'}

        # 提取所有词汇（中文按字符，英文按空格）
        words = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+', self.target_task)

        # 过滤停用词和短词
        keywords = [w for w in words if len(w) >= 2 and w not in stopwords]

        return keywords[:10]  # 最多 10 个关键词

    def _check_keyword_coverage(self, keywords: List[str]) -> Set[str]:
        """检查关键词在证据中的覆盖情况"""
        covered = set()

        # 收集所有证据文本
        all_text = ""
        for e in self.state.evidences:
            all_text += e.text + " "
        for ch in self.state.chapters.values():
            all_text += ch.content[:1000] + " "  # 只取前 1000 字符

        # 检查每个关键词
        for kw in keywords:
            if kw in all_text:
                covered.add(kw)

        return covered

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
        coverage_label = "未知"
        if last_round and last_round.coverage:
            coverage_label = "充足" if last_round.sufficient else "覆盖不足"
        stats = {
            "worldview": sum(len(items) for items in result.worldview.values()),
            "chapters": _format_chapters_range(result.chapters),
            "evidences": len(result.evidences),
            "coverage": coverage_label
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
            sufficient=last_round.sufficient if last_round and last_round.coverage else None,
            coverage=last_round.coverage if last_round and last_round.coverage else None
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
    user_id: Optional[str] = None,
    conversation_id: Optional[str] = None
) -> str:
    """深度探索内容，收集完成任务所需的所有信息

    Args:
        work_id: 作品ID（UUID格式，必需）
        target_task: 目标任务描述（如"续写第6章，需要了解主角性格和当前剧情"）
        search_keywords: 搜索关键词列表（由规划阶段直接提供，优先使用）
        max_rounds: 最大探索轮次（默认10轮）
        user_id: 用户ID（可选）
        conversation_id: 会话ID（可选，用于共享缓存）

    Returns:
        JSON格式的探索结果
    """
    logger.info(f"[explore_content] 开始: work_id={work_id}, target={target_task[:50]}...")
    if search_keywords:
        logger.info(f"[explore_content] 规划传入关键词: {search_keywords[:10]}")

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
        search_keywords=search_keywords
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
        if not chapters_list and result.evidences:
            fallback_chapters: Dict[int, Dict[str, Any]] = {}
            for e in result.evidences:
                chapter_order = e.chapter_order
                if not chapter_order:
                    continue
                entry = fallback_chapters.get(chapter_order)
                if not entry:
                    entry = {
                        "id": "",
                        "title": "",
                        "order": chapter_order,
                        "content": "",
                        "word_count": 0
                    }
                if not entry["id"] and e.chapter_id:
                    entry["id"] = e.chapter_id
                if not entry["title"] and e.chapter_title:
                    entry["title"] = e.chapter_title
                fallback_chapters[chapter_order] = entry

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

            chapters_list = [
                fallback_chapters[chapter_order]
                for chapter_order in sorted(fallback_chapters)
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

        frontend_display = to_frontend_display(result)
        search_results = _build_search_results(result)
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
            # 2026-01-18: 添加兼容字段，支持 $ref 引用
            "chapters": chapters_list,
            "worldview": worldview_dict
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"[explore_content] 失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "work_id": work_id
        }, ensure_ascii=False)
