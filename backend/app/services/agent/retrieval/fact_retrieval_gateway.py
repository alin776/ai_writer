# -*- coding: utf-8 -*-
"""Fact retrieval gateway (V6).

LightRAG 直连网关：查询 + 文档插入。
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_gateway_instance: Optional["FactRetrievalGateway"] = None


def get_gateway() -> "FactRetrievalGateway":
    """模块级单例，避免重复解析环境变量和创建连接。"""
    global _gateway_instance
    if _gateway_instance is None:
        _gateway_instance = FactRetrievalGateway()
    return _gateway_instance


@dataclass
class FactRetrievalGateway:
    """Gateway for LightRAG queries and document insertion."""

    lightrag_base_url: str = ""
    lightrag_query_path: str = ""
    lightrag_insert_path: str = ""
    lightrag_api_key: str = ""
    lightrag_timeout_seconds: int = 0
    lightrag_mode: str = ""
    lightrag_top_k: int = 20
    lightrag_max_retries: int = 0
    lightrag_retry_delay: float = 0.0
    lightrag_enable_rerank: bool = True

    def __post_init__(self) -> None:
        self.lightrag_base_url = (
            self.lightrag_base_url
            or os.getenv("LIGHTRAG_BASE_URL", "http://127.0.0.1:9621")
        ).strip()
        self.lightrag_query_path = (
            self.lightrag_query_path
            or os.getenv("LIGHTRAG_QUERY_PATH", "/query")
        ).strip() or "/query"
        self.lightrag_insert_path = (
            self.lightrag_insert_path
            or os.getenv("LIGHTRAG_INSERT_PATH", "/documents/text")
        ).strip() or "/documents/text"
        self.lightrag_api_key = (self.lightrag_api_key or os.getenv("LIGHTRAG_API_KEY", "")).strip()

        if not isinstance(self.lightrag_timeout_seconds, int) or self.lightrag_timeout_seconds <= 0:
            raw_timeout = os.getenv("LIGHTRAG_TIMEOUT_SECONDS", "300")
            try:
                self.lightrag_timeout_seconds = int(raw_timeout)
            except Exception:
                self.lightrag_timeout_seconds = 300
        self.lightrag_timeout_seconds = max(5, min(int(self.lightrag_timeout_seconds), 600))

        self.lightrag_mode = (
            self.lightrag_mode
            or os.getenv("LIGHTRAG_MODE", "hybrid")
        ).strip().lower() or "hybrid"

        if not isinstance(self.lightrag_top_k, int) or self.lightrag_top_k <= 0:
            raw_top_k = os.getenv("LIGHTRAG_TOP_K", "20")
            try:
                self.lightrag_top_k = int(raw_top_k)
            except Exception:
                self.lightrag_top_k = 20
        self.lightrag_top_k = max(5, min(int(self.lightrag_top_k), 200))

        if not isinstance(self.lightrag_max_retries, int) or self.lightrag_max_retries <= 0:
            raw_retries = os.getenv("LIGHTRAG_MAX_RETRIES", "3")
            try:
                self.lightrag_max_retries = int(raw_retries)
            except Exception:
                self.lightrag_max_retries = 3
        self.lightrag_max_retries = max(0, min(int(self.lightrag_max_retries), 10))

        if not isinstance(self.lightrag_retry_delay, (int, float)) or self.lightrag_retry_delay <= 0:
            raw_delay = os.getenv("LIGHTRAG_RETRY_DELAY", "2.0")
            try:
                self.lightrag_retry_delay = float(raw_delay)
            except Exception:
                self.lightrag_retry_delay = 2.0
        self.lightrag_retry_delay = max(0.1, min(float(self.lightrag_retry_delay), 60.0))

        # rerank 开关
        raw_rerank = os.getenv("LIGHTRAG_ENABLE_RERANK", "true")
        self.lightrag_enable_rerank = raw_rerank.lower().strip() in ("true", "1", "yes")

    # ------------------------------------------------------------------
    # 查询
    # ------------------------------------------------------------------

    async def query_lightrag_raw(
        self,
        query: str,
        *,
        top_k: int = 20,
        mode: str = "",
        only_need_context: bool = True,
    ) -> List[Dict[str, Any]]:
        """直连 LightRAG 查询。返回含 chapter_id 的 chunk 列表。

        Args:
            only_need_context: True 跳过内部 LLM（快），False 启用 KG 推理（慢但含实体关系）。
        """
        endpoint = self._resolve_endpoint(self.lightrag_query_path)
        payload: Dict[str, Any] = {
            "query": query,
            "mode": mode or self.lightrag_mode or "hybrid",
            "top_k": max(5, min(int(top_k), 200)),
            "only_need_context": only_need_context,
            "include_references": True,
            "enable_rerank": self.lightrag_enable_rerank,
        }
        raw = await self._request_lightrag(endpoint=endpoint, payload=payload)

        if not isinstance(raw, dict):
            raw = {"response": str(raw or "")}

        # 从 references 构建 reference_id → chapter_id 映射
        ref_to_chapter = self._build_ref_chapter_map(raw.get("references") or [])

        # 解析 context chunks（含 reference_id）
        context_text = str(raw.get("response") or raw.get("answer") or raw.get("text") or "").strip()
        parsed_chunks = self._parse_context_chunks(context_text)

        results: List[Dict[str, Any]] = []
        for chunk in parsed_chunks:
            text = chunk.get("content") or ""
            if not text:
                continue
            # 通过 reference_id 查找 chapter_id
            ref_id = chunk.get("reference_id") or ""
            chapter_id = ref_to_chapter.get(ref_id, "")

            snippet = text[:220] + "..." if len(text) > 220 else text
            results.append({
                "chapter_id": chapter_id,
                "text": text,
                "snippet": snippet,
                "reference_id": ref_id,
                "retrieval_mode": "lightrag_context",
            })

        logger.info(
            "[FactRetrieval] query_lightrag_raw query=%s hits=%d located=%d",
            query[:60], len(results),
            sum(1 for r in results if r["chapter_id"]),
        )
        return results

    # ------------------------------------------------------------------
    # 文档插入
    # ------------------------------------------------------------------

    async def insert_document(
        self,
        text: str,
        *,
        file_source: str = "",
    ) -> Dict[str, Any]:
        """插入文档到 LightRAG。file_source 用于标识来源（如 chapter_{chapter_id}）。"""
        endpoint = self._resolve_endpoint(self.lightrag_insert_path)
        payload: Dict[str, Any] = {"text": text}
        if file_source:
            payload["file_source"] = file_source

        result = await self._request_lightrag(endpoint=endpoint, payload=payload)
        logger.info(
            "[FactRetrieval] insert_document file_source=%s status=%s",
            file_source[:60],
            result.get("status") if isinstance(result, dict) else "unknown",
        )
        return result if isinstance(result, dict) else {"status": "unknown", "raw": result}

    # ------------------------------------------------------------------
    # 内部方法
    # ------------------------------------------------------------------

    @staticmethod
    def _build_ref_chapter_map(references: List[Any]) -> Dict[str, str]:
        """从 references 数组构建 reference_id → chapter_id 映射。

        references 格式: [{"reference_id": "doc-hash", "file_path": "chapter_{uuid}"}, ...]
        """
        mapping: Dict[str, str] = {}
        for ref in references:
            if not isinstance(ref, dict):
                continue
            ref_id = str(ref.get("reference_id") or "").strip()
            file_path = str(ref.get("file_path") or "").strip()
            if ref_id and file_path.startswith("chapter_"):
                chapter_id = file_path[len("chapter_"):]
                if chapter_id:
                    mapping[ref_id] = chapter_id
        return mapping

    def _resolve_endpoint(self, path: str) -> str:
        base_url = str(self.lightrag_base_url or "").strip()
        if not base_url:
            raise RuntimeError("LIGHTRAG_BASE_URL_EMPTY")
        path = str(path or "/query").strip() or "/query"
        return f"{base_url.rstrip('/')}/{path.lstrip('/')}"

    async def _request_lightrag(self, *, endpoint: str, payload: Dict[str, Any]) -> Any:
        import httpx

        headers = {"Content-Type": "application/json"}
        api_key = str(self.lightrag_api_key or "").strip()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
            headers["X-API-Key"] = api_key

        timeout_seconds = max(5, min(int(self.lightrag_timeout_seconds or 300), 600))
        timeout = httpx.Timeout(timeout_seconds, connect=min(10, timeout_seconds))
        max_retries = int(self.lightrag_max_retries or 0)
        retry_delay = float(self.lightrag_retry_delay or 2.0)

        last_exc: Optional[Exception] = None
        for attempt in range(max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=timeout, trust_env=False) as client:
                    response = await client.post(endpoint, json=payload, headers=headers)
                    response.raise_for_status()
                    content_type = str(response.headers.get("content-type") or "").lower()
                    if "application/json" not in content_type:
                        text = str(response.text or "").strip()
                        return {"response": text}
                    try:
                        return response.json()
                    except Exception:
                        text = str(response.text or "").strip()
                        return {"response": text}
            except (httpx.TimeoutException, httpx.ConnectError, httpx.ReadError) as exc:
                last_exc = exc
                if attempt < max_retries:
                    wait = retry_delay * (2 ** attempt)
                    logger.warning(
                        "[FactRetrieval] _request_lightrag 重试 %d/%d, 等待 %.1fs: %s",
                        attempt + 1, max_retries, wait, exc,
                    )
                    await asyncio.sleep(wait)
                else:
                    logger.error(
                        "[FactRetrieval] _request_lightrag 重试耗尽 (%d次): %s",
                        max_retries, exc,
                    )

        raise last_exc  # type: ignore[misc]

    @staticmethod
    def _parse_context_chunks(response_text: str) -> List[Dict[str, str]]:
        """解析 only_need_context=True 返回的 Document Chunks。

        返回 [{"reference_id": "...", "content": "..."}] 列表。
        """
        import json as _json

        if not response_text or not response_text.strip():
            return []
        text = response_text.strip()

        # 策略 1：提取 Document Chunks 中的 JSON 对象（含 reference_id + content）
        dc_marker = "Document Chunks"
        dc_idx = text.find(dc_marker)
        if dc_idx >= 0:
            after_dc = text[dc_idx:]
            backtick3 = "```"
            json_marker = backtick3 + "json"
            js_start = after_dc.find(json_marker)
            if js_start >= 0:
                js_start += len(json_marker)
                js_end = after_dc.find(backtick3, js_start)
                if js_end < 0:
                    js_end = len(after_dc)
                json_block = after_dc[js_start:js_end]
                chunks: List[Dict[str, str]] = []
                for line in json_block.split("\n"):
                    line = line.strip()
                    if not line or not line.startswith("{"):
                        continue
                    try:
                        obj = _json.loads(line)
                        content = str(obj.get("content") or "").strip()
                        ref_id = str(obj.get("reference_id") or "").strip()
                        if content:
                            chunks.append({"reference_id": ref_id, "content": content})
                    except (_json.JSONDecodeError, ValueError):
                        continue
                if chunks:
                    return chunks

        # 策略 2 回退：按分隔符切分（兼容旧版 LightRAG）
        for sep in ["-----Sources-----", "\n\n---\n\n", "\n---\n"]:
            if sep in text:
                parts = [chunk.strip() for chunk in text.split(sep) if chunk.strip()]
                if parts:
                    return [{"reference_id": "", "content": p} for p in parts]

        # 策略 3：整段作为单个 chunk
        return [{"reference_id": "", "content": text}] if text else []
