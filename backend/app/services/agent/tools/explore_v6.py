# -*- coding: utf-8 -*-
"""
Explore V6：AI 单查询生成 + LightRAG 直连

流程：
1. AI 生成 1 条 LightRAG 查询（1 次 LLM）
2. 单次调用 LightRAG（0 次 LLM）
3. 通过 references 中的 file_path 关联 chapter_id（0 次 LLM）
3b. 加载章节 HTML，用 _split_paragraphs() 做段落级定位（0 次 LLM）
4. 组装 ExploreResult 返回（含 paragraph_index / node_id）
"""

import json
import logging
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Annotated

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
- 生成 1 条搜索查询（30-80 字）
- 聚焦任务核心信息需求，包含关键人物、事件、设定等要素
- 用关键词 + 短语组合，覆盖任务涉及的主要维度

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
    # 步骤 3b：段落级定位（chunk → paragraph_index）
    # ------------------------------------------------------------------

    async def locate_in_chapters(
        self,
        chunks: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """对每个有 chapter_id 的 chunk，在章节内做段落级定位。

        通过 _split_paragraphs() 解析章节 HTML，然后将 chunk 文本与段落
        做子串匹配。当 chunk 跨多段时，用 self.target_task（用户请求）
        做偏好选择，优先返回与查询最相关的段落。
        """
        from app.services.agent.tools.locate_tools import _split_paragraphs

        # 按 chapter_id 分组，每个章节只加载一次
        chapter_paragraphs: Dict[str, List[Dict[str, Any]]] = {}

        located = 0
        for chunk in chunks:
            cid = str(chunk.get("chapter_id") or "")
            if not cid:
                continue
            chunk_text = str(chunk.get("text") or "").strip()
            if not chunk_text:
                continue

            # 懒加载章节段落
            if cid not in chapter_paragraphs:
                content = await self._load_chapter_content(cid)
                chapter_paragraphs[cid] = _split_paragraphs(content) if content else []

            paragraphs = chapter_paragraphs[cid]
            if not paragraphs:
                continue

            match_idx = self._match_paragraph(chunk_text, paragraphs, self.target_task)
            if match_idx is not None:
                para = paragraphs[match_idx]
                chunk["paragraph_index"] = para["index"]
                chunk["node_id"] = para.get("node_id") or ""
                chunk["located_text"] = para["text"]
                if match_idx > 0:
                    chunk["before_anchor"] = paragraphs[match_idx - 1]["text"]
                if match_idx < len(paragraphs) - 1:
                    chunk["after_anchor"] = paragraphs[match_idx + 1]["text"]
                located += 1

        logger.info("[ExploreV6] 段落定位完成: %d/%d chunks", located, len(chunks))
        return chunks

    @staticmethod
    def _match_paragraph(
        chunk_text: str,
        paragraphs: List[Dict[str, Any]],
        query_hint: str = "",
    ) -> Optional[int]:
        """在 chunk 覆盖的所有段落中，找与查询最相关的那个。

        LightRAG chunk 通常跨 3-50 个段落（~1200 token），盲选第一个或
        最长的都不靠谱。用 query_hint（用户请求/搜索查询）做偏好：
        1. 收集 chunk 中所有完整包含的段落
        2. 如有 query_hint，优先选与查询字符重叠最多的段落
        3. 无 query_hint 或无重叠时，回退到最长段落（最具体的匹配）
        """
        norm_chunk = re.sub(r"\s+", "", chunk_text)
        if not norm_chunk:
            return None

        # 收集所有匹配段落 (index_in_list, norm_text_len)
        candidates: List[Tuple[int, str]] = []
        for i, para in enumerate(paragraphs):
            norm_para = re.sub(r"\s+", "", para.get("text") or "")
            if not norm_para or len(norm_para) < 6:
                continue
            if norm_para in norm_chunk:
                candidates.append((i, norm_para))

        if not candidates:
            return None
        if len(candidates) == 1:
            return candidates[0][0]

        # 有 query_hint 时，按与查询的字符重叠量排序
        norm_query = re.sub(r"\s+", "", query_hint) if query_hint else ""
        if norm_query:
            def _overlap(para_text: str) -> int:
                """查询与段落的公共字符数（简单集合交集）"""
                return len(set(norm_query) & set(para_text))

            best = max(candidates, key=lambda c: (_overlap(c[1]), len(c[1])))
            if _overlap(best[1]) > 0:
                return best[0]

        # 回退：最长段落
        best = max(candidates, key=lambda c: len(c[1]))
        return best[0]

    async def _load_chapter_content(self, chapter_id: str) -> str:
        """加载章节 HTML 内容。"""
        try:
            from app.services.chapter_service import ChapterService
            from app.core.database import AsyncSessionLocal

            async with AsyncSessionLocal() as db:
                service = ChapterService(db)
                chapter = await service.get_chapter_by_id(chapter_id)
                if chapter and chapter.content:
                    return str(chapter.content)
        except Exception as exc:
            logger.warning("[ExploreV6] 加载章节内容失败: %s, err=%s", chapter_id[:8], exc)
        return ""

    # ------------------------------------------------------------------
    # 主入口
    # ------------------------------------------------------------------

    async def run(self) -> Dict[str, Any]:
        """执行 V6 探索流程，按下游工具分路获取上下文。"""
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

        # ---- 按下游工具分路 ----
        downstream = (self.retrieval_intent.get("downstream_tool") or "").strip()
        logger.info("[ExploreV6] downstream_tool=%s", downstream or "(未指定)")

        if downstream in ("smart_insert", "smart_rewrite"):
            return await self._run_locate(chapters, worldview, t0)
        elif downstream == "smart_continue":
            return await self._run_continue(chapters, worldview, t0)
        elif downstream == "smart_create":
            return await self._run_create(chapters, worldview, t0)
        else:
            # 新建章节 / 未知 → LightRAG KG 模式（兼容旧逻辑）
            return await self._run_create(chapters, worldview, t0)

    # ------------------------------------------------------------------
    # 路径 1：续写（纯 DB 读取）
    # ------------------------------------------------------------------

    async def _run_continue(self, chapters, worldview, t0) -> Dict[str, Any]:
        """续写路径：读当前章末尾 + 前一章末尾。"""
        chapter_id, chapter_order = self._resolve_target_chapter(chapters)

        # ---- 安全阀：用户指定了章节但该章节不存在 → 走 _run_create ----
        if not chapter_id:
            m = re.search(r'第(\d+)章', self.target_task)
            if m:
                logger.info("[ExploreV6] 续写目标第%s章不存在，升级为 _run_create", m.group(1))
                return await self._run_create(chapters, worldview, t0)

        # 找不到指定章节时，默认续写最后一章
        if not chapter_id and chapters:
            last_ch = max(chapters, key=lambda c: c.get("order", 0))
            chapter_id = str(last_ch["id"])
            chapter_order = last_ch.get("order")

        evidences = []

        # 读当前章末尾 2000 字
        if chapter_id:
            current_content = await self._load_chapter_content(chapter_id)
            current_tail = current_content[-2000:] if current_content else ""
            if current_tail:
                ch = next((c for c in chapters if str(c.get("id")) == chapter_id), None)
                evidences.append({
                    "text": current_tail,
                    "chapter_id": chapter_id,
                    "chapter_order": chapter_order,
                    "chapter_title": (ch or {}).get("title", ""),
                    "source_type": "db_chapter_tail",
                    "similarity": 0.95,
                })

        # 读前一章末尾 500 字
        if chapter_order and chapter_order > 1:
            prev_ch = next((c for c in chapters if c.get("order") == chapter_order - 1), None)
            if prev_ch:
                prev_content = await self._load_chapter_content(str(prev_ch["id"]))
                prev_tail = prev_content[-500:] if prev_content else ""
                if prev_tail:
                    evidences.append({
                        "text": prev_tail,
                        "chapter_id": str(prev_ch["id"]),
                        "chapter_order": prev_ch.get("order"),
                        "chapter_title": prev_ch.get("title", ""),
                        "source_type": "db_prev_chapter_tail",
                        "similarity": 0.80,
                    })

        duration_ms = int((time.time() - t0) * 1000)
        logger.info("[ExploreV6] 续写上下文就绪: chapter=%s, evidences=%d, 耗时=%dms",
                    chapter_id[:8] if chapter_id else "?", len(evidences), duration_ms)

        return self._build_result(
            evidences=evidences, chapters_info=chapters, worldview=worldview,
            stop_reason="续写上下文就绪", duration_ms=duration_ms,
            extra_stats={"downstream_tool": "smart_continue", "target_chapter": chapter_id},
        )

    # ------------------------------------------------------------------
    # 路径 2：插入/改写（reranker 精确定位段落）
    # ------------------------------------------------------------------

    async def _run_locate(self, chapters, worldview, t0) -> Dict[str, Any]:
        """插入/改写路径：reranker 精确定位段落 + 读前后文。"""
        from app.services.agent.tools.locate_tools import _split_paragraphs

        # 1. 确定章节（缓存 LightRAG 查询结果供回退复用）
        chapter_id, chapter_order = self._resolve_target_chapter(chapters)
        _cached_lightrag_chunks = None  # 缓存 LightRAG 结果，避免重复调用

        # 回退：用 LightRAG 粗筛获取 chapter_id
        if not chapter_id:
            worldview_summary = self._summarize_worldview(worldview)
            query = await self.generate_query(chapters, worldview_summary)
            _cached_lightrag_chunks = await self.execute_query(query)
            if _cached_lightrag_chunks:
                for chunk in _cached_lightrag_chunks:
                    cid = str(chunk.get("chapter_id") or "")
                    ch = next((c for c in chapters if str(c.get("id")) == cid), None)
                    if ch:
                        chapter_id = cid
                        chapter_order = ch.get("order")
                        break

        if not chapter_id:
            duration_ms = int((time.time() - t0) * 1000)
            logger.warning("[ExploreV6] 插入/改写定位失败：无法确定章节")
            return self._build_result(
                evidences=[], chapters_info=chapters, worldview=worldview,
                stop_reason="无法定位章节", duration_ms=duration_ms,
            )

        # 2. 加载章节，拆段落
        content = await self._load_chapter_content(chapter_id)
        paragraphs = _split_paragraphs(content) if content else []

        # 3. reranker 定位段落
        para_texts = [p["text"] for p in paragraphs if len(p.get("text", "")) >= 6]
        ranked = await self._rerank(self.target_task, para_texts)

        evidences = []
        ch_meta = next((c for c in chapters if str(c.get("id")) == chapter_id), {})

        if ranked:
            # 取 reranker 返回的 top 结果
            best_ranked = ranked[0]
            best_para_text = best_ranked.get("text") or ""
            # 在完整段落列表中找到对应段落
            best_idx = None
            for i, p in enumerate(paragraphs):
                if p.get("text", "") == best_para_text:
                    best_idx = i
                    break
            # 回退：用 index
            if best_idx is None and "index" in best_ranked:
                # ranked 的 index 是在 para_texts 中的位置，需要映射回 paragraphs
                ranked_idx = best_ranked["index"]
                filtered_paras = [p for p in paragraphs if len(p.get("text", "")) >= 6]
                if ranked_idx < len(filtered_paras):
                    target_text = filtered_paras[ranked_idx]["text"]
                    for i, p in enumerate(paragraphs):
                        if p.get("text", "") == target_text:
                            best_idx = i
                            break

            if best_idx is not None:
                para = paragraphs[best_idx]
                # 核心定位段落（唯一带 paragraph_index 的 evidence，作为 locate_target）
                evidences.append({
                    "text": para["text"],
                    "chapter_id": chapter_id,
                    "chapter_order": chapter_order,
                    "chapter_title": ch_meta.get("title", ""),
                    "paragraph_index": para["index"],
                    "node_id": para.get("node_id") or "",
                    "located_text": para["text"],
                    "before_anchor": paragraphs[best_idx - 1]["text"] if best_idx > 0 else "",
                    "after_anchor": paragraphs[best_idx + 1]["text"] if best_idx < len(paragraphs) - 1 else "",
                    "source_type": "reranker_locate",
                    "similarity": best_ranked.get("score", 0.9),
                })
                # 添加前后 2-3 段作为纯上下文（不设 paragraph_index，不进 locate_targets）
                context_range = range(max(0, best_idx - 3), min(len(paragraphs), best_idx + 4))
                for ci in context_range:
                    if ci == best_idx:
                        continue
                    cp = paragraphs[ci]
                    if len(cp.get("text", "")) < 6:
                        continue
                    evidences.append({
                        "text": cp["text"],
                        "chapter_id": chapter_id,
                        "chapter_order": chapter_order,
                        "chapter_title": ch_meta.get("title", ""),
                        "source_type": "reranker_context",
                        "similarity": max(0.1, 0.7 - abs(ci - best_idx) * 0.1),
                    })

        # 4. reranker 失败回退：用旧的 LightRAG + 子串匹配流程（复用缓存的查询结果）
        if not evidences:
            logger.warning("[ExploreV6] reranker 定位无结果，回退到 LightRAG + 子串匹配")
            if _cached_lightrag_chunks is not None:
                chunks = _cached_lightrag_chunks
            else:
                worldview_summary = self._summarize_worldview(worldview)
                query = await self.generate_query(chapters, worldview_summary)
                chunks = await self.execute_query(query)
            # 过滤非法 chapter_id
            _uuid_re = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
            chunks = [c for c in chunks if _uuid_re.match(str(c.get("chapter_id") or ""))]
            chunks = await self.enrich_chunks(chunks, chapters)
            chunks = await self.locate_in_chapters(chunks)
            for idx, chunk in enumerate(chunks):
                evidences.append({
                    "text": str(chunk.get("text") or ""),
                    "chapter_order": chunk.get("chapter_order"),
                    "chapter_id": chunk.get("chapter_id") or "",
                    "chapter_title": chunk.get("chapter_title") or "",
                    "paragraph_index": chunk.get("paragraph_index"),
                    "node_id": chunk.get("node_id") or "",
                    "located_text": chunk.get("located_text") or "",
                    "before_anchor": chunk.get("before_anchor") or "",
                    "after_anchor": chunk.get("after_anchor") or "",
                    "similarity": max(0.05, 0.9 - idx * 0.02),
                    "source_type": "lightrag_fallback",
                })

        duration_ms = int((time.time() - t0) * 1000)
        logger.info("[ExploreV6] 定位上下文就绪: chapter=%s, evidences=%d, 耗时=%dms",
                    chapter_id[:8], len(evidences), duration_ms)

        return self._build_result(
            evidences=evidences, chapters_info=chapters, worldview=worldview,
            stop_reason="定位上下文就绪", duration_ms=duration_ms,
            extra_stats={"downstream_tool": "smart_insert/smart_rewrite", "target_chapter": chapter_id},
        )

    async def _rerank(self, query: str, documents: List[str], top_n: int = 5) -> List[Dict]:
        """调用本地 reranker 服务（bge-reranker-base）。"""
        if not documents:
            return []
        import httpx
        from app.core.config import settings
        base_url = settings.RERANKER_BASE_URL.rstrip("/")
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(f"{base_url}/rerank", json={
                    "query": query, "documents": documents, "top_n": top_n,
                })
                resp.raise_for_status()
                results = resp.json().get("results", [])
                # 补充原始文本到结果中
                for r in results:
                    idx = r.get("index")
                    if isinstance(idx, int) and 0 <= idx < len(documents):
                        r["text"] = documents[idx]
                return results
        except Exception as exc:
            logger.warning("[ExploreV6] reranker 调用失败: %s", exc)
            return []

    # ------------------------------------------------------------------
    # 路径 3：新建章节（LightRAG KG + 上一章末尾）
    # ------------------------------------------------------------------

    async def _run_create(self, chapters, worldview, t0) -> Dict[str, Any]:
        """新建章节路径：LightRAG KG 推理 + 上一章末尾。"""
        evidences = []

        # 1. 读上一章末尾 2000 字
        last_ch = max(chapters, key=lambda c: c.get("order", 0)) if chapters else None
        if last_ch:
            prev_content = await self._load_chapter_content(str(last_ch["id"]))
            prev_tail = prev_content[-2000:] if prev_content else ""
            if prev_tail:
                evidences.append({
                    "text": prev_tail,
                    "chapter_id": str(last_ch["id"]),
                    "chapter_order": last_ch.get("order"),
                    "chapter_title": last_ch.get("title", ""),
                    "source_type": "db_prev_chapter_tail",
                    "similarity": 0.95,
                })

        # 2. LightRAG KG 查询（mix 模式，不跳过内部 LLM）
        worldview_summary = self._summarize_worldview(worldview)
        query = await self.generate_query(chapters, worldview_summary)
        logger.info("[ExploreV6] 新建章节 KG 查询: %s", query)

        kg_summary = ""
        from app.services.agent.retrieval.fact_retrieval_gateway import get_gateway
        gateway = get_gateway()
        try:
            kg_results = await gateway.query_lightrag_raw(
                query, mode="mix", only_need_context=False, raw_mode=True,
            )
            # raw_mode 返回 [{"kg_summary": "...", "retrieval_mode": "lightrag_kg_raw"}]
            if kg_results and kg_results[0].get("kg_summary"):
                kg_summary = kg_results[0]["kg_summary"]
        except Exception as exc:
            logger.warning("[ExploreV6] LightRAG KG 查询失败: %s", exc)

        logger.info("[ExploreV6] KG 推理摘要长度: %d 字", len(kg_summary))

        duration_ms = int((time.time() - t0) * 1000)
        logger.info("[ExploreV6] 新建章节上下文就绪: evidences=%d, kg_summary=%d字, 耗时=%dms",
                    len(evidences), len(kg_summary), duration_ms)

        return self._build_result(
            evidences=evidences, chapters_info=chapters, worldview=worldview,
            stop_reason="新建章节上下文就绪", duration_ms=duration_ms,
            extra_stats={"downstream_tool": "create_chapter", "query": query},
            kg_summary=kg_summary,
        )

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    def _resolve_target_chapter(self, chapters: List[Dict[str, Any]]) -> Tuple[str, Optional[int]]:
        """从 retrieval_intent 或 target_task 推断目标章节。

        返回 (chapter_id, chapter_order)。找不到返回 ("", None)。
        """
        # 1. 检查 constraints.chapter_scope
        scope = (self.retrieval_intent.get("constraints") or {}).get("chapter_scope")
        if scope and isinstance(scope, list) and len(scope) >= 1:
            order = scope[0] if isinstance(scope[0], int) else None
            if order is not None:
                ch = next((c for c in chapters if c.get("order") == order), None)
                if ch:
                    return str(ch["id"]), order

        # 2. 从 target_task 提取"第X章"
        m = re.search(r'第(\d+)章', self.target_task)
        if m:
            order = int(m.group(1))
            ch = next((c for c in chapters if c.get("order") == order), None)
            if ch:
                return str(ch["id"]), order

        return "", None

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
        kg_summary: str = "",
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

        # 构建 locate_targets（按 chapter_id + paragraph_index 去重）
        # 只包含有段落级定位信息的 evidence，避免噪声导致 ambiguous_locator
        seen_keys: set = set()
        locate_targets: list = []
        for e in evidences:
            cid = e.get("chapter_id") or ""
            if not cid:
                continue
            pi = e.get("paragraph_index")
            nid = e.get("node_id") or ""
            # 没有 paragraph_index 也没有 node_id → 仅章节级，不作为定位目标
            if pi is None and not nid:
                continue
            key = f"{cid}:{pi}" if pi is not None else f"{cid}:nid:{nid}"
            if key in seen_keys:
                continue
            seen_keys.add(key)
            locate_targets.append({
                "chapter_id": cid,
                "chapter_order": e.get("chapter_order"),
                "paragraph_index": pi,
                "node_id": e.get("node_id") or "",
                "text": e.get("located_text") or "",
                "before_anchor": e.get("before_anchor") or "",
                "after_anchor": e.get("after_anchor") or "",
            })

        return {
            "success": True,
            "evidences": evidences,
            "paragraphs": [],
            "chapters": chapters_list,
            "locate_targets": locate_targets,
            "worldview": worldview,
            "explore_summary": "",
            "kg_summary": kg_summary,
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

    from langgraph.prebuilt import InjectedState

    @_lc_tool
    @_register("explore_content", "explore", "深度探索内容收集相关信息")
    async def explore_content(
        work_id: str,
        target_task: str,
        retrieval_intent: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        step_reasoning: Optional[str] = None,
        state: Annotated[dict, InjectedState] = None,
        **_kwargs: Any,
    ) -> str:
        """深度探索内容，收集完成任务所需的所有信息

        Args:
            work_id: 作品ID（UUID格式，必需）
            target_task: 目标任务描述
            retrieval_intent: 结构化检索意图
            user_id: 用户ID（可选）
        """
        # 从 state 读 downstream_tool，注入 retrieval_intent
        if state and state.get("downstream_tool"):
            if retrieval_intent is None:
                retrieval_intent = {}
            retrieval_intent.setdefault("downstream_tool", state["downstream_tool"])

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
        step_reasoning: Optional[str] = None,
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
