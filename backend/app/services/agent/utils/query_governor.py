# -*- coding: utf-8 -*-
"""Keyword governance helpers for Explore planning/execution."""

from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Optional

KEYWORD_SPLIT_PATTERN = re.compile(r"[,\s，。；;：:、|｜/]+")

DEFAULT_INSTRUCTION_KEYWORDS = {
    "检索",
    "搜索",
    "查询",
    "提取",
    "定位",
    "关键词",
    "策略",
    "段落",
    "章节",
    "内容",
    "信息",
    "分析",
    "精确",
    "精准",
    "匹配",
    "结果",
    "命中",
}

DEFAULT_WIDE_KEYWORDS = {
    "主角",
    "配角",
    "反派",
    "剧情",
    "冲突",
    "设定",
    "情节",
    "人物",
    "故事",
    "数据",
    "信息",
    "内容",
    "证据",
    "材料",
    "文本",
    "描述",
    "细节",
    "情况",
    "逻辑",
    "结论",
}

DEFAULT_FUNCTION_KEYWORDS = {
    "以及",
    "还有",
    "或者",
    "然后",
    "因为",
    "所以",
    "如果",
    "但是",
    "并且",
    "需要",
    "相关",
    "内容",
    "所有",
    "全部",
    "这个",
    "那个",
    "这些",
    "那些",
    "其中",
    "用于",
    "是否",
    "已经",
    "没有",
}

DEFAULT_ALIAS_TABLE: Dict[str, List[str]] = {
    "器灵": ["器灵", "灵体", "灵魄"],
    "吞噬": ["吞噬", "吸收", "炼化"],
    "桩功": ["桩功", "站桩", "浑圆桩"],
    "刀法": ["刀法", "刀势", "五虎群羊刀"],
    "精神力": ["精神力", "神识", "识海"],
}


def _normalize_text(text: Any) -> str:
    value = str(text or "").strip()
    if not value:
        return ""
    value = value.strip("\"'“”‘’《》()[]{}")
    value = re.sub(r"\s+", "", value)
    return value


def _parse_env_terms(raw_value: str) -> List[str]:
    text = str(raw_value or "").strip()
    if not text:
        return []
    parsed: List[str] = []
    if text.startswith("["):
        try:
            payload = json.loads(text)
            if isinstance(payload, list):
                parsed.extend(str(item) for item in payload if str(item).strip())
        except Exception:
            parsed = []
    if not parsed:
        parsed.extend(part.strip() for part in re.split(r"[,\n\r;；、|]+", text) if part.strip())
    return parsed


def _load_keyword_set_from_env(env_name: str, defaults: set[str]) -> set[str]:
    raw = os.getenv(env_name, "")
    if not raw:
        return set(defaults)
    loaded = set()
    for item in _parse_env_terms(raw):
        norm = _normalize_text(item)
        if norm:
            loaded.add(norm)
    return loaded or set(defaults)


def _load_alias_table_from_env(defaults: Dict[str, List[str]]) -> Dict[str, List[str]]:
    raw = os.getenv("EXPLORE_GOVERN_ALIAS_TABLE", "").strip()
    if not raw:
        return {k: list(v) for k, v in defaults.items()}
    try:
        payload = json.loads(raw)
    except Exception:
        return {k: list(v) for k, v in defaults.items()}
    if not isinstance(payload, dict):
        return {k: list(v) for k, v in defaults.items()}
    alias_table: Dict[str, List[str]] = {}
    for key, values in payload.items():
        root = _normalize_text(key)
        if len(root) < 2:
            continue
        candidates: List[str] = []
        if isinstance(values, list):
            candidates.extend(str(item) for item in values)
        elif isinstance(values, str):
            candidates.extend(_parse_env_terms(values))
        variants: List[str] = []
        seen = set()
        for item in [root] + candidates:
            norm = _normalize_text(item)
            if len(norm) < 2 or norm in seen:
                continue
            seen.add(norm)
            variants.append(norm)
        if variants:
            alias_table[root] = variants
    return alias_table or {k: list(v) for k, v in defaults.items()}


INSTRUCTION_KEYWORDS = _load_keyword_set_from_env(
    "EXPLORE_GOVERN_INSTRUCTION_KEYWORDS",
    DEFAULT_INSTRUCTION_KEYWORDS,
)
WIDE_KEYWORDS = _load_keyword_set_from_env(
    "EXPLORE_GOVERN_WIDE_KEYWORDS",
    DEFAULT_WIDE_KEYWORDS,
)
FUNCTION_KEYWORDS = _load_keyword_set_from_env(
    "EXPLORE_GOVERN_FUNCTION_KEYWORDS",
    DEFAULT_FUNCTION_KEYWORDS,
)
ALIAS_TABLE = _load_alias_table_from_env(DEFAULT_ALIAS_TABLE)
KEYWORD_RULES_SOURCE = "defaults"
if any(
    os.getenv(env_name)
    for env_name in (
        "EXPLORE_GOVERN_INSTRUCTION_KEYWORDS",
        "EXPLORE_GOVERN_WIDE_KEYWORDS",
        "EXPLORE_GOVERN_FUNCTION_KEYWORDS",
        "EXPLORE_GOVERN_ALIAS_TABLE",
    )
):
    KEYWORD_RULES_SOURCE = "env_overrides"


def _split_keyword_text(text: str) -> List[str]:
    if not isinstance(text, str):
        return []
    parts = [p.strip() for p in KEYWORD_SPLIT_PATTERN.split(text) if p and p.strip()]
    return parts


def _extract_quoted_segments(target_task: str) -> List[str]:
    if not isinstance(target_task, str) or not target_task.strip():
        return []
    segments: List[str] = []
    seen = set()
    for match in re.findall(r'["“”‘’「」『』《》](.+?)["“”‘’「」『』》]', target_task):
        seg = _normalize_text(match)
        if len(seg) < 2 or seg in seen:
            continue
        seen.add(seg)
        segments.append(seg)
    return segments


def _extract_task_terms(target_task: str, limit: int = 16) -> List[str]:
    if not isinstance(target_task, str) or not target_task.strip():
        return []

    candidates: List[str] = []
    candidates.extend(_extract_quoted_segments(target_task))
    for token in re.findall(r"[\u4e00-\u9fffA-Za-z0-9]{2,20}", target_task):
        norm = _normalize_text(token)
        if len(norm) < 2:
            continue
        # Exclude chapter/range hints.
        if re.fullmatch(r"第?\d+章", norm):
            continue
        candidates.append(norm)

    deduped: List[str] = []
    seen = set()
    for item in candidates:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
        if len(deduped) >= limit:
            break
    return deduped


def _is_instruction_keyword(keyword: str) -> bool:
    if not keyword:
        return True
    if keyword in INSTRUCTION_KEYWORDS:
        return True
    return False


def _is_wide_keyword(keyword: str) -> bool:
    if not keyword:
        return True
    if keyword in WIDE_KEYWORDS:
        return True
    # 单字中文通常语义过宽；两字中文可能是实体名（如“孔斌”），不在这里一刀切拦截。
    if len(keyword) <= 1 and re.fullmatch(r"[\u4e00-\u9fff]{1}", keyword):
        return True
    return False


def _is_function_keyword(keyword: str) -> bool:
    if not keyword:
        return True
    return keyword in FUNCTION_KEYWORDS


def _dedupe_keep_order(values: List[str], limit: int) -> List[str]:
    out: List[str] = []
    seen = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        out.append(value)
        if len(out) >= limit:
            break
    return out


def _build_clusters(keywords: List[str], enable_alias_expand: bool) -> List[Dict[str, Any]]:
    clusters: List[Dict[str, Any]] = []
    for keyword in keywords:
        variants = [keyword]
        if enable_alias_expand:
            for root, aliases in ALIAS_TABLE.items():
                if root in keyword or keyword in aliases:
                    for alias in aliases:
                        alias_norm = _normalize_text(alias)
                        if alias_norm and alias_norm not in variants:
                            variants.append(alias_norm)
        clusters.append(
            {
                "root": keyword,
                "variants": variants[:4],
            }
        )
    return clusters


def govern_search_keywords(
    keywords: Optional[List[str]],
    target_task: str = "",
    max_keywords: int = 8,
    min_keywords: int = 2,
    enable_alias_expand: bool = True,
) -> Dict[str, Any]:
    """Normalize/clean/expand keywords for stable retrieval behavior."""
    raw_candidates: List[str] = []
    for item in keywords or []:
        if isinstance(item, str):
            raw_candidates.extend(_split_keyword_text(item))
        else:
            raw_candidates.extend(_split_keyword_text(str(item)))

    task_terms = _extract_task_terms(target_task, limit=max(max_keywords * 2, 8))
    if not raw_candidates:
        raw_candidates.extend(task_terms)

    blocked: List[Dict[str, str]] = []
    specific: List[str] = []
    wide: List[str] = []
    for item in raw_candidates:
        norm = _normalize_text(item)
        if not norm:
            continue
        if len(norm) < 2:
            blocked.append({"keyword": norm, "reason": "too_short"})
            continue
        if len(norm) > 24:
            norm = norm[:24]
        if _is_instruction_keyword(norm):
            blocked.append({"keyword": norm, "reason": "instruction_keyword"})
            continue
        if _is_function_keyword(norm):
            blocked.append({"keyword": norm, "reason": "function_keyword"})
            continue
        if _is_wide_keyword(norm):
            wide.append(norm)
            continue
        specific.append(norm)

    suppressed_wide_terms: List[str] = []
    if specific and wide:
        suppressed_wide_terms = _dedupe_keep_order(wide, max_keywords)
    elif not specific and wide:
        anchor_candidates: List[str] = []
        for term in task_terms:
            if _is_instruction_keyword(term) or _is_function_keyword(term) or _is_wide_keyword(term):
                continue
            anchor_candidates.append(term)
        if anchor_candidates:
            specific.append(anchor_candidates[0])
            specific.append(wide[0])
            if len(wide) > 1:
                suppressed_wide_terms.extend(wide[1:])
        else:
            for item in wide:
                blocked.append({"keyword": item, "reason": "wide_without_anchor"})

    if len(specific) < min_keywords:
        for term in task_terms:
            if _is_instruction_keyword(term):
                continue
            if _is_function_keyword(term):
                continue
            if _is_wide_keyword(term):
                has_anchor = any(not _is_wide_keyword(item) for item in specific)
                has_wide = any(_is_wide_keyword(item) for item in specific)
                if has_anchor and not has_wide:
                    specific.append(term)
                else:
                    suppressed_wide_terms.append(term)
                continue
            specific.append(term)
            if len(specific) >= min(max_keywords, max(min_keywords, 1)):
                break

    final_keywords = _dedupe_keep_order(specific, max_keywords)
    clusters = _build_clusters(final_keywords, enable_alias_expand=enable_alias_expand)
    expanded_alias_terms = _dedupe_keep_order(
        [alias for cluster in clusters for alias in cluster.get("variants", [])[1:]],
        max_keywords * 2,
    )
    return {
        "keywords": final_keywords,
        "clusters": clusters,
        "blocked": blocked,
        "suppressed_wide_terms": _dedupe_keep_order(suppressed_wide_terms, max_keywords),
        "expanded_alias_terms": expanded_alias_terms,
        "derived_terms": _dedupe_keep_order(task_terms, max_keywords),
        "rule_source": KEYWORD_RULES_SOURCE,
        "rule_sizes": {
            "instruction": len(INSTRUCTION_KEYWORDS),
            "wide": len(WIDE_KEYWORDS),
            "function": len(FUNCTION_KEYWORDS),
            "alias_roots": len(ALIAS_TABLE),
        },
    }


def expand_cluster_keywords(clusters: Optional[List[Dict[str, Any]]], max_keywords: int = 8) -> List[str]:
    """Flatten keyword clusters (root + first alias) with stable order."""
    if not isinstance(clusters, list):
        return []
    out: List[str] = []
    for cluster in clusters:
        if not isinstance(cluster, dict):
            continue
        root = _normalize_text(cluster.get("root"))
        if root:
            out.append(root)
        variants = cluster.get("variants")
        if isinstance(variants, list):
            for variant in variants:
                v = _normalize_text(variant)
                if v and v != root:
                    out.append(v)
                    break
    return _dedupe_keep_order(out, max_keywords)
