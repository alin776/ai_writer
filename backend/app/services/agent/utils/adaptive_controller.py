# -*- coding: utf-8 -*-
"""Adaptive rewrite policy for Explore lexical retrieval."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple


def _normalize_term(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    text = text.strip("\"'“”‘’《》()[]{}")
    return text


def _dedupe_keep_order(values: Iterable[Any], limit: int = 0) -> List[str]:
    out: List[str] = []
    seen: Set[str] = set()
    for item in values:
        term = _normalize_term(item)
        if not term:
            continue
        key = term.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(term)
        if limit > 0 and len(out) >= limit:
            break
    return out


@dataclass
class AdaptiveRewrite:
    strategy: str
    reason: str
    search_intent: str
    keywords: List[str]
    terms_required: List[str]
    terms_optional: List[str]
    terms_excluded: List[str]
    proximity_terms: List[str]
    match_mode: str = "any"
    proximity_window: int = 12
    chapter_range: Optional[Tuple[int, int]] = None
    limit: int = 100

    def to_search_args(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "keywords": list(self.keywords),
            "terms_required": list(self.terms_required),
            "terms_optional": list(self.terms_optional),
            "terms_excluded": list(self.terms_excluded),
            "proximity_terms": list(self.proximity_terms),
            "match_mode": self.match_mode,
            "proximity_window": int(self.proximity_window),
            "strategy": self.strategy,
            "search_intent": self.search_intent,
            "limit": int(self.limit),
            "adaptive_reason": self.reason,
        }
        if self.chapter_range:
            payload["chapter_range"] = [self.chapter_range[0], self.chapter_range[1]]
        return payload


class AdaptiveController:
    """Generate deterministic rewrite args from failure reasons."""

    def build_rewrite(
        self,
        *,
        failure_reason: str,
        target_task: str,
        intent_spec: Optional[Dict[str, Any]],
        iteration_state: Optional[Dict[str, Any]],
        latest_keywords: Sequence[str],
        latest_terms_required: Sequence[str],
        latest_terms_optional: Sequence[str],
        latest_terms_excluded: Sequence[str],
        latest_proximity_terms: Sequence[str],
        latest_scope: Optional[Tuple[int, int]],
        seed_keywords: Sequence[str],
    ) -> Optional[AdaptiveRewrite]:
        reason = str(failure_reason or "").strip().lower()
        if not reason:
            reason = "lexical_miss"

        intent_data = intent_spec or {}
        state_data = iteration_state or {}

        must_have = _dedupe_keep_order(intent_data.get("must_have") or [], limit=8)
        nice_to_have = _dedupe_keep_order(intent_data.get("nice_to_have") or [], limit=8)
        source_keywords = _dedupe_keep_order(intent_data.get("source_keywords") or [], limit=8)

        covered = {
            str(item).strip()
            for item in (state_data.get("covered_must_have_set") or [])
            if str(item).strip()
        }
        uncovered = [term for term in must_have if term not in covered]

        anchors = _dedupe_keep_order(
            list(latest_terms_required)
            + list(latest_keywords)
            + list(seed_keywords)
            + list(source_keywords)
            + list(uncovered)
            + list(nice_to_have),
            limit=10,
        )
        excluded = _dedupe_keep_order(latest_terms_excluded, limit=6)

        lexical_miss_count = int((state_data.get("failed_reason_histogram") or {}).get("lexical_miss", 0) or 0)
        scope = self._rewrite_scope(latest_scope, reason=reason, lexical_miss_count=lexical_miss_count)

        if reason in ("semantic_mismatch", "insufficient_coverage"):
            required = _dedupe_keep_order(uncovered or anchors[:2], limit=2)
            optional = _dedupe_keep_order(
                list(latest_terms_optional) + [item for item in anchors if item not in required],
                limit=4,
            )
            return AdaptiveRewrite(
                strategy="adaptive_semantic_focus",
                reason="已有命中但覆盖不足，改为聚焦未覆盖 must_have",
                search_intent=f"围绕未覆盖目标要素重搜：{','.join(required[:2])}" if required else "围绕未覆盖目标要素重搜",
                keywords=_dedupe_keep_order(required + optional, limit=6),
                terms_required=required,
                terms_optional=optional,
                terms_excluded=excluded,
                proximity_terms=_dedupe_keep_order(required[:2], limit=2),
                match_mode="all" if len(required) > 1 else "phrase",
                proximity_window=8,
                chapter_range=scope,
                limit=120,
            )

        if reason == "locator_drop":
            required = _dedupe_keep_order(latest_terms_required or anchors[:2], limit=2)
            optional = _dedupe_keep_order(
                list(latest_terms_optional) + [item for item in anchors if item not in required],
                limit=4,
            )
            return AdaptiveRewrite(
                strategy="adaptive_locator_repair",
                reason="命中被定位过滤，优先补可定位段落",
                search_intent="优先搜索带明确章节和段落定位的命中",
                keywords=_dedupe_keep_order(required + optional, limit=6),
                terms_required=required,
                terms_optional=optional,
                terms_excluded=excluded,
                proximity_terms=_dedupe_keep_order(latest_proximity_terms or required, limit=2),
                match_mode="any",
                proximity_window=10,
                chapter_range=scope,
                limit=140,
            )

        required = _dedupe_keep_order(
            list(latest_terms_required) or anchors[:1] or must_have[:1],
            limit=2,
        )
        optional = _dedupe_keep_order(
            list(latest_terms_optional)
            + [item for item in anchors if item not in required],
            limit=5,
        )
        proximity_terms = _dedupe_keep_order(
            list(latest_proximity_terms) + required + optional[:1],
            limit=3,
        )
        return AdaptiveRewrite(
            strategy="adaptive_recall_expand",
            reason="词面召回不足，扩大锚点和召回层",
            search_intent=f"围绕任务核心锚点扩展召回：{target_task[:40]}",
            keywords=_dedupe_keep_order(required + optional, limit=7),
            terms_required=required,
            terms_optional=optional,
            terms_excluded=excluded,
            proximity_terms=proximity_terms,
            match_mode="any",
            proximity_window=12,
            chapter_range=scope,
            limit=140,
        )

    def _rewrite_scope(
        self,
        scope: Optional[Tuple[int, int]],
        *,
        reason: str,
        lexical_miss_count: int,
    ) -> Optional[Tuple[int, int]]:
        if not scope:
            return None
        start, end = scope
        if start > end:
            start, end = end, start
        if reason == "scope_miss" or lexical_miss_count >= 2:
            return (max(1, start - 2), end + 2)
        return (start, end)
