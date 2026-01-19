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

logger = logging.getLogger(__name__)

MIN_EVIDENCE_SIMILARITY = 0.35
AUTO_LOCATE_LIMIT = 3
AUTO_READ_LIMIT = 3
AUTO_LOCATE_LIMIT_STRICT = 12
AUTO_READ_LIMIT_STRICT = 12

PARAGRAPH_REQUIRED_KEYWORDS = (
    "段落号",
    "章节号+段落号",
    "章节号＋段落号",
    "章节号及段落号",
    "段落编号",
    "段落索引",
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


def _requires_paragraph_index(target_task: str) -> bool:
    if not target_task:
        return False
    return any(keyword in target_task for keyword in PARAGRAPH_REQUIRED_KEYWORDS)


def _requires_unreachable_items(target_task: str) -> bool:
    if not target_task:
        return False
    return any(keyword in target_task for keyword in UNREACHABLE_MISSING_KEYWORDS)


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
    """AI 生成的单轮行动计划"""
    search_queries: List[str]         # 本轮搜索词
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

    def should_search(self, query: str) -> bool:
        """判断是否应该执行搜索"""
        return query not in self.searched_queries

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

    def should_read_chapter(self, chapter_order: int) -> bool:
        """判断是否应该读取章节"""
        return chapter_order not in self.read_chapter_orders

    def record_chapter_read(self, chapter_order: int):
        """记录已读取的章节"""
        self.read_chapter_orders.add(chapter_order)

    def should_read_worldview(self, category: str) -> bool:
        """判断是否应该读取世界观分类"""
        return category not in self.read_worldview_categories

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
        require_paragraph_index: bool = False
    ) -> bool:
        """添加搜索结果（去重 + 相似度过滤）"""
        paragraph_index = result.get("paragraph_index")
        if require_paragraph_index and paragraph_index is None:
            text_preview = result.get("snippet", result.get("content", "")) or ""
            logger.info(
                "[ContentExplorer] 严格段落号模式发现无段落号证据: query=%s, preview=%s",
                query,
                _truncate_text(text_preview, 80)
            )
            self.skipped_evidences_strict += 1
        if isinstance(paragraph_index, str) and paragraph_index.isdigit():
            paragraph_index = int(paragraph_index)
        similarity = result.get("similarity")
        if isinstance(similarity, (int, float)) and 0 < similarity <= 1:
            if similarity < MIN_EVIDENCE_SIMILARITY:
                return False

        evidence_key = self._build_evidence_key(result, query)
        if evidence_key in self.evidence_keys:
            return False
        self.evidence_keys.add(evidence_key)

        evidence = Evidence(
            text=result.get("snippet", result.get("content", ""))[:200],
            chapter_order=result.get("chapter_order", 0),
            paragraph_index=paragraph_index,
            similarity=result.get("similarity", 0),
            source_type=result.get("source", "hybrid"),
            query=query,
            round_idx=round_idx
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
        self.chapters[order] = ChapterRead(
            id=chapter.get("id", ""),  # 2026-01-18: 添加章节ID
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
            for e in evidences_to_show[:10]:  # 最多显示 10 条
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
    summary_parts.append(f"- 读取章节: {stats.get('total_chapters', 0)} 章")
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
            for e in evidences[:3]:  # 每章最多 3 条
                # 截断证据文本，避免 summary 过长
                text_preview = e.text[:200] + "..." if len(e.text) > 200 else e.text
                para_label = f"{e.paragraph_index}段" if isinstance(e.paragraph_index, int) else "段落未知"
                summary_parts.append(f"  - [{para_label}] {text_preview}")
        summary_parts.append("")

    # 5. AI 分析
    if result.analysis:
        summary_parts.append("【AI 分析】")
        summary_parts.append(result.analysis)

    return "\n".join(summary_parts)


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
        elif tc.tool_name in ["read_paragraph", "get_chapter_by_order_tool"]:
            chapter = tc.params.get("chapter_order", "?")
            tags.append({
                "type": "ReadRaw",
                "value": f"第{chapter}章"
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
        step_id: Optional[int] = None
    ):
        """
        初始化内容探索器

        Args:
            work_id: 作品ID
            target_task: 目标任务描述
            max_rounds: 最大探索轮次（安全上限，AI 会自主决定何时停止）
            emit_callback: 事件发射回调
        """
        self.work_id = work_id
        self.target_task = target_task
        self.chapter_scope = _parse_chapter_scope(target_task)
        self.scope_chapter_id: Optional[str] = None
        self.scope_look_ahead = 0
        self.scope_resolution_attempted = False
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
        if self.require_paragraph_index:
            logger.info("[ContentExplorer] 启用严格段落号模式")
        if self.chapter_scope:
            logger.info("[ContentExplorer] 章节范围锁定: 第%s-%s章", self.chapter_scope[0], self.chapter_scope[1])

    async def _ensure_scope_context(self) -> Tuple[str, int]:
        if not self.chapter_scope:
            return "", 0
        if self.scope_resolution_attempted:
            return self.scope_chapter_id or "", self.scope_look_ahead
        self.scope_resolution_attempted = True
        start, end = self.chapter_scope
        try:
            from app.services.agent.langgraph_tools import resolve_chapter_id
            chapter_id, error_json = await resolve_chapter_id(self.work_id, str(start))
            if error_json:
                logger.warning(f"[ContentExplorer] 章节范围解析失败: {error_json}")
            else:
                self.scope_chapter_id = chapter_id
                # look_ahead=0 会导致不限制范围，单章场景至少给 1
                self.scope_look_ahead = max(1, end - start)
        except Exception as e:
            logger.warning(f"[ContentExplorer] 章节范围解析异常: {e}")
        return self.scope_chapter_id or "", self.scope_look_ahead

    def _is_chapter_in_scope(self, chapter_order: Optional[int]) -> bool:
        if not self.chapter_scope:
            return True
        if not isinstance(chapter_order, int):
            return False
        start, end = self.chapter_scope
        return start <= chapter_order <= end

    def _filter_results_in_scope(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not self.chapter_scope:
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

    async def explore(self) -> ExploreResult:
        """
        执行探索（AI 驱动版本）

        Returns:
            ExploreResult: 探索结果
        """
        logger.info(f"[ContentExplorer] 开始探索: work_id={self.work_id}, target={self.target_task[:50]}...")

        stop_reason = "达到最大轮次"

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

        for round_idx in range(1, self.max_rounds + 1):
            round_start = get_utc_now()

            # AI 决定本轮行动
            try:
                round_plan = await self._ai_plan_round(round_idx)
            except Exception as e:
                logger.warning(f"[ContentExplorer] AI 轮次规划失败，使用默认策略: {e}")
                # 首轮优先使用 exploration_plan.initial_queries
                default_queries = []
                if round_idx == 1:
                    if self.exploration_plan and self.exploration_plan.initial_queries:
                        default_queries = self.exploration_plan.initial_queries[:3]
                    else:
                        default_queries = [self.target_task[:30]]
                round_plan = RoundPlan(
                    search_queries=default_queries,
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
            except Exception as e:
                logger.warning(f"[ContentExplorer] AI 充足性评估失败: {e}")
                # 使用简单规则兜底
                if len(self.state.evidences) >= 5 and len(self.state.chapters) >= 1:
                    stop_reason = "规则判断信息充足"
                    round_data.sufficient = True
                    round_data.coverage = "规则判断信息充足"
                    round_data.missing_items = []
                    # 设置兜底的 summary 和 next_action
                    stats = self.state.get_stats()
                    round_data.summary = f"经过 {stats['rounds_count']} 轮探索，收集到 {stats['total_evidences']} 条证据和 {stats['total_chapters']} 个章节的背景信息。"
                    round_data.next_action = "基于这些背景信息，我将执行后续任务。"
                    break

            # 检查是否收敛（连续无新信息）
            if self.state.check_convergence():
                if not round_data.missing_items:
                    stop_reason = "信息收敛"
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
                        require_paragraph_index=self.require_paragraph_index
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
        chapters_to_read = self._determine_chapters_to_read()
        for chapter_order in chapters_to_read[:2]:  # 最多读2章
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
        AI 决定本轮行动计划

        使用 SIMPLE_QA 任务类型优化成本
        """
        from app.services.agent.model_selector import TaskType

        ai_service = _get_ai_service()

        # 构建已收集信息摘要
        collected_summary = self._build_collected_summary()

        # 首轮提示 AI 参考 initial_queries
        initial_hint = ""
        if round_idx == 1 and self.exploration_plan and self.exploration_plan.initial_queries:
            initial_hint = f"\n建议的初始搜索词（供参考）：{', '.join(self.exploration_plan.initial_queries)}"

        scope_hint = ""
        if self.chapter_scope:
            scope_hint = f"\n章节范围约束：仅限第{self.chapter_scope[0]}-{self.chapter_scope[1]}章，禁止跨章扩展。"

        prompt = f"""你是信息收集专家。请根据当前状态决定本轮行动。

目标任务：{self.target_task}
任务理解：{self.exploration_plan.understanding if self.exploration_plan else self.target_task}
需要了解：{', '.join(self.exploration_plan.aspects_to_find) if self.exploration_plan else '未知'}{initial_hint}{scope_hint}

当前轮次：第 {round_idx} 轮
已收集信息：
{collected_summary}

已搜索过的关键词（避免重复）：{', '.join(list(self.state.searched_queries)[:10])}

请决定本轮行动：
1. 需要搜索什么关键词？（避免重复已搜索的）
2. 需要读取哪些章节？（基于搜索结果中的章节号）
3. 需要精确读取哪些段落？（可选）

请输出 JSON 格式（不要包含其他内容）：
{{
  "search_queries": ["搜索词1", "搜索词2"],
  "chapters_to_read": [1, 2],
  "paragraphs_to_read": [],
  "reason": "决策理由"
}}"""

        try:
            response = await ai_service.call_ai(
                system_prompt="你是信息收集专家。只输出 JSON，不要有其他内容。",
                user_prompt=prompt,
                max_tokens=300,
                temperature=0.2,
                task_type=TaskType.SIMPLE_QA
            )

            result = self._parse_json_response(response)

            # 过滤已搜索的查询
            search_queries = [
                q for q in result.get("search_queries", [])
                if q and self.state.should_search(q)
            ]

            # 过滤已读取的章节
            chapters_to_read = [
                c for c in result.get("chapters_to_read", [])
                if isinstance(c, int) and self.state.should_read_chapter(c)
            ]

            return RoundPlan(
                search_queries=search_queries[:3],  # 最多3个搜索
                chapters_to_read=chapters_to_read[:2],  # 最多2个章节
                paragraphs_to_read=result.get("paragraphs_to_read", [])[:3],
                reason=result.get("reason", "")
            )
        except Exception as e:
            logger.warning(f"[ContentExplorer] AI 轮次规划解析失败: {e}")
            raise

    async def _ai_assess_sufficiency(self) -> SufficiencyAssessment:
        """
        AI 判断信息是否充足

        使用 DEEP_ANALYSIS 任务类型
        同时生成探索总结和下一步行动
        """
        from app.services.agent.model_selector import TaskType

        ai_service = _get_ai_service()

        collected_summary = self._build_collected_summary()
        rounds_count = len(self.state.rounds)

        prompt = f"""你是信息收集专家。请评估已收集的信息是否足够完成目标任务。

目标任务：{self.target_task}
任务理解：{self.exploration_plan.understanding if self.exploration_plan else self.target_task}
需要了解的方面：{', '.join(self.exploration_plan.aspects_to_find) if self.exploration_plan else '未知'}
探索轮次：{rounds_count}

已收集信息：
{collected_summary}

注意：只能基于本地作品库可检索内容进行评估，不要要求搜索引擎/外部平台/作者等不可达信息。
如果目标任务限定了章节范围，缺失项必须来自该范围内。

请评估：
1. 信息是否足够完成目标任务？
2. 覆盖了哪些方面？
3. 还缺少什么关键信息？
4. 用自然语言总结探索过程和收集到的关键内容（2-3句话）
5. 基于探索结果，描述下一步将如何完成任务（1-2句话）

请输出 JSON 格式（不要包含其他内容）：
{{
  "sufficient": true或false,
  "coverage": "已覆盖XXX，缺少XXX",
  "missing": ["缺失项1", "缺失项2"],
  "summary": "经过X轮深度探索，我收集到...（具体描述关键信息，如人物、情节、设定等）",
  "next_action": "基于这些背景信息，我将执行 [工具名] [具体行动]，重点描写/处理..."
}}"""

        try:
            response = await ai_service.call_ai(
                system_prompt="你是信息收集专家。只输出 JSON，不要有其他内容。",
                user_prompt=prompt,
                max_tokens=500,  # 增加 token 限制以生成更长的总结
                temperature=0.1,
                task_type=TaskType.DEEP_ANALYSIS
            )

            logger.info(
                "[ContentExplorer] 充足性评估原始响应(截断): %s",
                _truncate_text(response)
            )

            result = self._parse_json_response(response)
            missing_preview = result.get("missing", [])
            if isinstance(missing_preview, list):
                missing_preview = missing_preview[:5]
            logger.info(
                "[ContentExplorer] 充足性评估解析: sufficient=%s, coverage=%s, missing=%s, summary=%s, next_action=%s",
                result.get("sufficient", False),
                result.get("coverage", ""),
                missing_preview,
                _truncate_text(result.get("summary", ""), 100),
                _truncate_text(result.get("next_action", ""), 100)
            )

            return SufficiencyAssessment(
                sufficient=result.get("sufficient", False),
                coverage=result.get("coverage", ""),
                missing=result.get("missing", []),
                summary=result.get("summary", ""),
                next_action=result.get("next_action", "")
            )
        except Exception as e:
            logger.warning(f"[ContentExplorer] AI 充足性评估解析失败: {e}")
            raise

    def _build_collected_summary(self) -> str:
        """构建已收集信息的摘要"""
        lines = []

        if self.chapter_scope:
            lines.append(f"- 任务章节范围：第{self.chapter_scope[0]}-{self.chapter_scope[1]}章")

        # 证据统计
        if self.state.evidences:
            evidence_chapters = set(e.chapter_order for e in self.state.evidences if e.chapter_order > 0)
            lines.append(f"- 证据片段：{len(self.state.evidences)} 条，来自章节：{sorted(evidence_chapters)}")
            # 显示部分证据内容
            for e in self.state.evidences[:3]:
                lines.append(f"  · [{e.chapter_order}章] {e.text[:80]}...")
        else:
            lines.append("- 证据片段：0 条")

        # 章节统计
        if self.state.chapters:
            chapter_info = [f"{ch.order}({ch.title})" for ch in self.state.chapters.values()]
            lines.append(f"- 已读章节：{', '.join(chapter_info)}")
        else:
            lines.append("- 已读章节：无")

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
        from app.services.agent.langgraph_tools import search_content, get_writing_context, read_paragraph, locate_content

        tool_calls = []
        new_evidences = 0
        new_paragraphs = 0
        scope_chapter_id = ""
        scope_look_ahead = 0
        if self.chapter_scope:
            scope_chapter_id, scope_look_ahead = await self._ensure_scope_context()

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

        # 2. 执行 AI 规划的搜索
        auto_locate_used = 0
        auto_read_used = 0
        locate_limit = AUTO_LOCATE_LIMIT_STRICT if self.require_paragraph_index else AUTO_LOCATE_LIMIT
        read_limit = AUTO_READ_LIMIT_STRICT if self.require_paragraph_index else AUTO_READ_LIMIT
        for query in plan.search_queries:
            if not self.state.should_search(query):
                continue

            start = get_utc_now()
            try:
                search_params = {
                    "work_id": self.work_id,
                    "query": query,
                    "top_k": 5
                }
                if scope_chapter_id:
                    search_params["chapter_id"] = scope_chapter_id
                    search_params["look_ahead"] = scope_look_ahead
                result = await search_content.ainvoke(search_params)
                result_data = json.loads(result) if isinstance(result, str) else result
                self.state.record_search(query)

                if self.chapter_scope and isinstance(result_data, dict):
                    result_data["results"] = self._filter_results_in_scope(result_data.get("results", []))

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
                    if self.chapter_scope and not self._is_chapter_in_scope(chapter_order):
                        continue

                    if paragraph_index is None and auto_locate_used < locate_limit and chapter_id:
                        min_snippet_len = 20
                        if self.require_paragraph_index:
                            min_snippet_len = 8
                        locate_queries = []
                        if snippet and len(snippet) >= min_snippet_len:
                            locate_queries.append(snippet)
                        if self.require_paragraph_index and query and len(query.strip()) >= 2 and query not in locate_queries:
                            locate_queries.append(query)
                        for locate_query in locate_queries:
                            if auto_locate_used >= locate_limit:
                                break
                            auto_locate_used += 1
                            locate_start = get_utc_now()
                            locate_params = {
                                "chapter_id": chapter_id,
                                "query": locate_query
                            }
                            if self.chapter_scope or self.require_paragraph_index:
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
                        require_paragraph_index=self.require_paragraph_index
                    ):
                        new_evidences += 1

                duration = int((get_utc_now() - start).total_seconds() * 1000)
                tool_calls.append(ToolCall(
                    tool_name="search_content",
                    params={
                        "query": query,
                        "chapter_id": scope_chapter_id,
                        "look_ahead": scope_look_ahead
                    } if scope_chapter_id else {"query": query},
                    result=result_data,
                    duration_ms=duration
                ))
            except Exception as e:
                logger.warning(f"[ContentExplorer] 搜索失败: {e}")

        # 3. 读取 AI 规划的章节
        chapters_to_read = plan.chapters_to_read
        if chapters_to_read:
            normalized = []
            for c in chapters_to_read:
                if isinstance(c, str) and c.isdigit():
                    normalized.append(int(c))
                elif isinstance(c, int):
                    normalized.append(c)
            chapters_to_read = normalized
        if self.chapter_scope:
            chapters_to_read = [c for c in chapters_to_read if self._is_chapter_in_scope(c)]
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
            if not chapter_order or paragraph_index is None:
                continue
            if self.chapter_scope and not self._is_chapter_in_scope(chapter_order):
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
        if not plan.search_queries and not plan.chapters_to_read:
            chapters_from_evidence = self._determine_chapters_to_read()
            for chapter_order in chapters_from_evidence[:2]:
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
        if self.chapter_scope:
            to_read = [o for o in to_read if self._is_chapter_in_scope(o)]

        return sorted(to_read)

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

        # 规则 3：至少读取 1 个章节
        if len(self.state.chapters) < 1:
            missing.append("需要读取章节原文")

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
    max_rounds: int = 10,
    user_id: Optional[str] = None
) -> str:
    """深度探索内容，收集完成任务所需的所有信息

    Args:
        work_id: 作品ID（UUID格式，必需）
        target_task: 目标任务描述（如"续写第6章，需要了解主角性格和当前剧情"）
        max_rounds: 最大探索轮次（默认10轮）
        user_id: 用户ID（可选）

    Returns:
        JSON格式的探索结果
    """
    logger.info(f"[explore_content] 开始: work_id={work_id}, target={target_task[:50]}...")

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

    explorer = ContentExplorer(
        work_id=work_id,
        target_task=target_task,
        max_rounds=max_rounds,
        emit_callback=emit_callback,
        step_id=step_id_value
    )

    try:
        result = await explorer.explore()

        # 构建 explore_summary - 供后续工具（如 analyze_content）使用的文本摘要
        explore_summary = _build_explore_summary(result)

        # 2026-01-18: 构建兼容 get_writing_context 的 chapters 数组
        chapters_list = [
            {
                "id": ch.id,
                "title": ch.title,
                "order": ch.order,
                "content": ch.content,
                "word_count": ch.word_count
            }
            for order, ch in sorted(result.chapters.items())
        ]

        # 2026-01-18: 构建兼容 get_writing_context 的 worldview 对象
        worldview_dict = {}
        for category, items in result.worldview.items():
            worldview_dict[category] = [
                {"name": item.name, "description": item.description}
                for item in items
            ]

        # 转换为JSON
        return json.dumps({
            "success": True,
            "work_id": work_id,
            "target_task": target_task,
            "analysis": result.analysis,
            "stats": result.stats,
            "stop_reason": result.stop_reason,
            "total_duration_ms": result.total_duration_ms,
            "frontend_display": to_frontend_display(result),
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
