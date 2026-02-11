# -*- coding: utf-8 -*-
"""
Explore V6：AI 单查询生成 + LightRAG 直连

流程：
1. AI 生成 1 条 LightRAG 查询（1 次 LLM）
2. 单次调用 LightRAG（0 次 LLM）
3. 通过 references 中的 file_path 关联 chapter_id（0 次 LLM）
4. 组装 ExploreResult 返回
"""

import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from app.services.agent.model_selector import TaskType

logger = logging.getLogger(__name__)


@dataclass
class ExploreV6Result:
    """V6 探索结果"""
    success: bool
    evidences: List[Dict[str, Any]]
    worldview: Dict[str, list]
    chapters_info: List[Dict[str, Any]]
    stats: Dict[str, Any]
    stop_reason: str
    total_duration_ms: int


class ExploreV6:
    """Explore V6 核心引擎"""

    def __init__(
        self,
        work_id: str,
        target_task: str,
        retrieval_intent: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        top_k: int = 20,
    ):
        self.work_id = work_id
        self.target_task = target_task
        self.retrieval_intent = retrieval_intent or {}
        self.user_id = user_id
        self.top_k = top_k

    # ------------------------------------------------------------------
    # 步骤 1：AI 生成单条查询
    # ------------------------------------------------------------------

    async def generate_query(
        self,
        chapters: List[Dict[str, Any]],
        worldview_summary: str = "",
    ) -> str:
        """1 次 LLM 调用，将用户任务转化为 1 条 LightRAG 查询字符串。"""
        ai_service = _get_ai_service()

        chapter_list = "\n".join(
            f"  第{ch.get('order', '?')}章: {ch.get('title', '无标题')} ({ch.get('word_count', 0)}字)"
            for ch in chapters[:30]
        )

        prompt = f"""你是搜索查询生成器。根据用户任务生成 1 条搜索查询，用于从小说原文中检索相关片段。

用户任务：{self.target_task}

小说章节列表：
{chapter_list}

{f"世界观摘要：{worldview_summary[:500]}" if worldview_summary else ""}

规则：
- 生成 1 条简短的搜索查询（10-30 字）
- 聚焦任务核心信息需求，不要堆砌多个维度
- 用关键词 + 短语，不要写长句子

只返回查询文本，不要其他内容。"""

        try:
            response = await ai_service.call_ai(
                system_prompt="你是搜索查询生成器，只返回一条查询文本。",
                user_prompt=prompt,
                task_type=TaskType.TEXT_CLASSIFICATION,
            )
            query = str(response or "").strip().strip('"').strip("'").strip()
            if query:
                return query
        except Exception as exc:
            logger.warning("[ExploreV6] generate_query 失败: %s", exc)

        # 回退：直接用 target_task
        return self.target_task

    # ------------------------------------------------------------------
    # 步骤 2：单次调用 LightRAG
    # ------------------------------------------------------------------

    async def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """单次调用 LightRAG，返回 chunk 列表。"""
        from app.services.agent.retrieval.fact_retrieval_gateway import get_gateway

        gateway = get_gateway()
        try:
            chunks = await gateway.query_lightrag_raw(query, top_k=self.top_k)
        except Exception as exc:
            logger.warning("[ExploreV6] LightRAG 查询失败: query=%s err=%s", query[:40], exc)
            chunks = []

        logger.info("[ExploreV6] 查询完成: query=%s, hits=%d", query[:60], len(chunks))
        return chunks

    # ------------------------------------------------------------------
    # 步骤 3：通过 chapter_id 补全章节元数据
    # ------------------------------------------------------------------

    async def enrich_chunks(
        self,
        chunks: List[Dict[str, Any]],
        chapters: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """根据 gateway 返回的 chapter_id，补全 chapter_order / chapter_title。"""
        # 构建 chapter_id → 元数据映射
        ch_map: Dict[str, Dict[str, Any]] = {}
        for ch in chapters:
            ch_map[str(ch.get("id") or "")] = ch

        located = 0
        for chunk in chunks:
            cid = str(chunk.get("chapter_id") or "")
            if cid and cid in ch_map:
                ch = ch_map[cid]
                chunk["chapter_order"] = ch.get("order")
                chunk["chapter_title"] = ch.get("title") or ""
                located += 1

        logger.info("[ExploreV6] 定位完成: %d/%d chunks", located, len(chunks))
        return chunks

    # ------------------------------------------------------------------
    # 主入口
    # ------------------------------------------------------------------

    async def run(self) -> Dict[str, Any]:
        """执行 V6 探索流程，返回与 explore_content 兼容的结果字典。"""
        t0 = time.time()

        # ---- 获取章节列表 ----
        chapters = await self._get_chapters()
        if not chapters:
            return self._build_result(
                evidences=[], chapters_info=[], worldview={},
                stop_reason="无可用章节", duration_ms=0,
            )

        # ---- 获取世界观小包 ----
        worldview = await self._get_worldview()
        worldview_summary = self._summarize_worldview(worldview)

        # ---- 步骤 1：AI 生成查询 ----
        query = await self.generate_query(chapters, worldview_summary)
        logger.info("[ExploreV6] 生成查询: %s", query)

        # ---- 步骤 2：调用 LightRAG ----
        chunks = await self.execute_query(query)

        # ---- 步骤 3：补全章节元数据 ----
        chunks = await self.enrich_chunks(chunks, chapters)

        # ---- 步骤 4：组装结果 ----
        duration_ms = int((time.time() - t0) * 1000)

        # 构建 evidences
        evidences = []
        for idx, chunk in enumerate(chunks):
            evidences.append({
                "text": str(chunk.get("text") or ""),
                "chapter_order": chunk.get("chapter_order"),
                "chapter_id": chunk.get("chapter_id") or "",
                "chapter_title": chunk.get("chapter_title") or "",
                "similarity": max(0.05, 0.9 - idx * 0.02),
                "source_type": "lightrag_v6",
            })

        stop_reason = "V6 探索完成"

        result = self._build_result(
            evidences=evidences,
            chapters_info=chapters,
            worldview=worldview,
            stop_reason=stop_reason,
            duration_ms=duration_ms,
            extra_stats={
                "query": query,
                "total_chunks": len(chunks),
            },
        )

        logger.info(
            "[ExploreV6] 完成: %d evidences, 耗时=%dms",
            len(evidences), duration_ms,
        )
        return result

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    async def _get_chapters(self) -> List[Dict[str, Any]]:
        """获取章节列表。"""
        try:
            from app.services.chapter_service import ChapterService
            from app.core.database import AsyncSessionLocal

            async with AsyncSessionLocal() as db:
                service = ChapterService(db)
                chapters = await service.get_chapters_by_work(self.work_id)
                return [
                    {
                        "id": str(ch.id),
                        "order": ch.order,
                        "title": ch.title or "",
                        "word_count": ch.word_count or 0,
                    }
                    for ch in (chapters or [])
                ]
        except Exception as exc:
            logger.warning("[ExploreV6] 获取章节列表失败: %s", exc)
            return []

    async def _get_worldview(self) -> Dict[str, list]:
        """获取世界观小包。"""
        try:
            from app.services.agent.langgraph_tools import get_worldview_pack

            keywords = []
            entities = self.retrieval_intent.get("entities") or []
            keywords = list(dict.fromkeys(entities))[:8]

            wv_result = await get_worldview_pack.ainvoke({
                "work_id": self.work_id,
                "user_id": self.user_id or "",
                "keywords": keywords,
                "top_k": 5,
                "include_guidelines": True,
                "task_hint": self.target_task or "",
                "chapter_orders": "",
            })
            wv_data = json.loads(wv_result) if isinstance(wv_result, str) else wv_result
            worldview: Dict[str, list] = {}
            for cat in ("characters", "locations", "settings", "glossary"):
                items = wv_data.get(cat)
                if isinstance(items, list) and items:
                    worldview[cat] = items
            return worldview
        except Exception as exc:
            logger.warning("[ExploreV6] 获取世界观失败: %s", exc)
            return {}

    @staticmethod
    def _summarize_worldview(worldview: Dict[str, list]) -> str:
        """将世界观数据压缩为简短摘要供 prompt 使用。"""
        parts = []
        for cat, items in worldview.items():
            if not items:
                continue
            names = [str(item.get("name") or item.get("title") or "") for item in items[:5]]
            names = [n for n in names if n]
            if names:
                parts.append(f"{cat}: {'、'.join(names)}")
        return "; ".join(parts) if parts else ""

    def _build_result(
        self,
        *,
        evidences: list,
        chapters_info: list,
        worldview: dict,
        stop_reason: str,
        duration_ms: int,
        extra_stats: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """构建与 explore_content V5 兼容的输出字典。"""
        located_chapters = sorted(set(
            e["chapter_order"] for e in evidences
            if isinstance(e.get("chapter_order"), int)
        ))
        stats = {
            "total_evidences": len(evidences),
            "located_chapters": located_chapters,
            "total_chapters": len(chapters_info),
            "explore_version": "v6",
        }
        if extra_stats:
            stats.update(extra_stats)

        # 构建 chapters list（从 chapters_info 元数据）
        chapters_list = [
            {
                "id": str(ch.get("id") or ""),
                "order": ch.get("order"),
                "title": str(ch.get("title") or ""),
                "word_count": ch.get("word_count", 0),
            }
            for ch in chapters_info
            if isinstance(ch, dict)
        ]

        # 构建 locate_targets（从 evidences 按 chapter_id 去重）
        seen_chapter_ids: set = set()
        locate_targets: list = []
        for e in evidences:
            cid = e.get("chapter_id") or ""
            if not cid or cid in seen_chapter_ids:
                continue
            seen_chapter_ids.add(cid)
            locate_targets.append({
                "chapter_id": cid,
                "chapter_order": e.get("chapter_order"),
            })

        return {
            "success": True,
            "evidences": evidences,
            "paragraphs": [],
            "chapters": chapters_list,
            "locate_targets": locate_targets,
            "worldview": worldview,
            "explore_summary": "",
            "context_for_task": "\n\n".join(
                str(e.get("text") or "") for e in evidences[:20]
            ),
            "stats": stats,
            "stop_reason": stop_reason,
            "total_duration_ms": duration_ms,
        }


# ------------------------------------------------------------------
# 模块级辅助
# ------------------------------------------------------------------

_ai_service_v6 = None


def _get_ai_service():
    """获取 AI 服务（懒初始化，使用 flash 模型降低成本）。"""
    global _ai_service_v6
    if _ai_service_v6 is None:
        from app.services.ai.http_ai_service import HTTPAIService
        _ai_service_v6 = HTTPAIService(model="gemini-2.5-flash", enable_model_selector=False)
    return _ai_service_v6


# ------------------------------------------------------------------
# 注册函数（供 langgraph_tools 导入）
# ------------------------------------------------------------------

try:
    from langchain_core.tools import tool as _lc_tool
    from .tool_registry import register_as_tool as _register
except ImportError:
    # 单元测试通过 importlib 直接加载时，相对导入不可用
    _lc_tool = None
    _register = None


def _define_tools():
    """延迟定义工具函数，避免模块级相对导入失败。"""
    if _lc_tool is None or _register is None:
        return

    @_lc_tool
    @_register("explore_content", "explore", "深度探索内容收集相关信息")
    async def explore_content(
        work_id: str,
        target_task: str,
        retrieval_intent: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        **_kwargs: Any,
    ) -> str:
        """深度探索内容，收集完成任务所需的所有信息

        Args:
            work_id: 作品ID（UUID格式，必需）
            target_task: 目标任务描述
            retrieval_intent: 结构化检索意图
            user_id: 用户ID（可选）
        """
        v6 = ExploreV6(
            work_id=work_id,
            target_task=target_task,
            retrieval_intent=retrieval_intent,
            user_id=user_id,
        )
        result = await v6.run()
        return json.dumps(result, ensure_ascii=False, indent=2)

    @_register("load_explore_artifact", "explore", "读取已保存的探索结果")
    async def load_explore_artifact(
        artifact_id: str,
        work_id: str,
        user_id: Optional[str] = None,
        mode: str = "full",
        max_chars: Optional[int] = None,
    ) -> str:
        """按 artifact_id 读取 Explore 结果"""
        from app.services.agent.utils.explore_artifact import load_explore_artifact as _load

        result = await _load(
            artifact_id=artifact_id,
            work_id=work_id,
            user_id=user_id,
            mode=mode,
            max_chars=max_chars,
        )
        return json.dumps(result, ensure_ascii=False, indent=2)

    # 暴露到模块级
    import sys
    current_module = sys.modules[__name__]
    current_module.explore_content = explore_content
    current_module.load_explore_artifact = load_explore_artifact


_define_tools()
