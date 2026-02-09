# -*- coding: utf-8 -*-
"""Keyword governance helpers for Explore planning/execution.

Design notes:
- Remove built-in domain dictionaries to avoid rigid hardcoded behavior.
- Keep output schema stable for upstream callers.
- Use structural signals only (quoted spans, token shape, informativeness).
"""

from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Optional, Sequence, Tuple

KEYWORD_SPLIT_PATTERN = re.compile(r"[,\s，。；;：:、|｜/]+")
QUOTE_PATTERN = re.compile(r"[\"'“”‘’「」『』《》](.+?)[\"'“”‘’「」『』《》]")
TASK_TERM_PATTERN = re.compile(r"[\u4e00-\u9fffA-Za-z0-9]{2,24}")
STRUCTURAL_CONNECTOR_PATTERN = re.compile(r"(?:关于|围绕|针对|有关|以及|并且|并|和|与|及|是否|的)")
INSTRUCTION_PREFIX_PATTERN = re.compile(r"^(?:查找|寻找|检索|搜索|定位|确认|分析|核查|提取)")


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


def _load_alias_table_from_env() -> Dict[str, List[str]]:
    raw = os.getenv("EXPLORE_GOVERN_ALIAS_TABLE", "").strip()
    if not raw:
        return {}
    try:
        payload = json.loads(raw)
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}

    alias_table: Dict[str, List[str]] = {}
    for key, values in payload.items():
        root = _normalize_text(key)
        if len(root) < 2:
            continue

        candidates: List[str] = [root]
        if isinstance(values, list):
            candidates.extend(str(item) for item in values)
        elif isinstance(values, str):
            candidates.extend(_parse_env_terms(values))

        normalized: List[str] = []
        seen = set()
        for item in candidates:
            norm = _normalize_text(item)
            if len(norm) < 2 or norm in seen:
                continue
            seen.add(norm)
            normalized.append(norm)
        if normalized:
            alias_table[root] = normalized

    return alias_table


def _load_keyword_set_from_env(env_name: str) -> set[str]:
    raw = os.getenv(env_name, "")
    if not raw:
        return set()
    loaded = set()
    for item in _parse_env_terms(raw):
        norm = _normalize_text(item)
        if norm:
            loaded.add(norm)
    return loaded


ALIAS_TABLE = _load_alias_table_from_env()
INSTRUCTION_KEYWORDS = _load_keyword_set_from_env("EXPLORE_GOVERN_INSTRUCTION_KEYWORDS")
WIDE_KEYWORDS = _load_keyword_set_from_env("EXPLORE_GOVERN_WIDE_KEYWORDS")
FUNCTION_KEYWORDS = _load_keyword_set_from_env("EXPLORE_GOVERN_FUNCTION_KEYWORDS")
KEYWORD_RULES_SOURCE = "runtime_structural"
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


def _dedupe_keep_order(values: Sequence[str], limit: int) -> List[str]:
    out: List[str] = []
    seen = set()
    cap = max(1, int(limit or 1))
    for raw in values:
        value = _normalize_text(raw)
        if not value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(value)
        if len(out) >= cap:
            break
    return out


def _split_keyword_text(text: str) -> List[str]:
    if not isinstance(text, str):
        return []
    return [part.strip() for part in KEYWORD_SPLIT_PATTERN.split(text) if part and part.strip()]


def _extract_quoted_segments(target_task: str) -> List[str]:
    if not isinstance(target_task, str) or not target_task.strip():
        return []
    segments: List[str] = []
    seen = set()
    for match in QUOTE_PATTERN.findall(target_task):
        seg = _normalize_text(match)
        if len(seg) < 2 or seg in seen:
            continue
        seen.add(seg)
        segments.append(seg)
    return segments


def _is_structural_noise(term: str) -> bool:
    value = _normalize_text(term)
    if len(value) < 2:
        return True
    if len(value) > 32:
        return True
    if re.fullmatch(r"\d+", value):
        return True
    if re.fullmatch(r"[\W_]+", value):
        return True
    if re.fullmatch(r"第?\d+章", value):
        return True
    if not re.search(r"[\u4e00-\u9fffA-Za-z0-9]", value):
        return True
    return False


def _term_informativeness(term: str) -> float:
    value = _normalize_text(term)
    if not value:
        return 0.0
    length = len(value)
    unique_ratio = len(set(value)) / max(length, 1)
    cjk_count = len(re.findall(r"[\u4e00-\u9fff]", value))
    latin_count = len(re.findall(r"[A-Za-z]", value))
    digit_count = len(re.findall(r"\d", value))
    script_mix = int(cjk_count > 0) + int(latin_count > 0) + int(digit_count > 0)

    length_score = max(0.1, 1.0 - (abs(length - 5) * 0.08))
    mix_bonus = 0.08 * max(0, script_mix - 1)
    return (unique_ratio * 0.55) + (length_score * 0.45) + mix_bonus


def _is_two_char_cjk(term: str) -> bool:
    value = _normalize_text(term)
    return bool(re.fullmatch(r"[\u4e00-\u9fff]{2}", value))


def _derive_core_chunks(term: str, max_chunks: int = 3) -> List[str]:
    """Derive compact lexical chunks from a raw term without fixed dictionaries."""
    raw = str(term or "")
    base = _normalize_text(raw)
    if len(base) < 2:
        return []

    is_composite = bool(re.search(r"[\s,，。；;：:、|｜/\"'“”‘’「」『』《》]", raw))
    quoted_chunks = [_normalize_text(item) for item in QUOTE_PATTERN.findall(raw)]
    quoted_chunks = [item for item in quoted_chunks if not _is_structural_noise(item)]
    if is_composite and quoted_chunks:
        return _dedupe_keep_order(quoted_chunks, limit=max(1, max_chunks))

    candidates: List[str] = [] if is_composite else [base]
    candidates.extend(quoted_chunks)
    tokenized = [item for item in _split_keyword_text(base) if len(_normalize_text(item)) >= 2]
    candidates.extend(tokenized)
    candidates.extend(part for part in STRUCTURAL_CONNECTOR_PATTERN.split(base) if part)

    dense_parts = [
        _normalize_text(part)
        for part in TASK_TERM_PATTERN.findall(base)
        if len(_normalize_text(part)) >= 2
    ]
    candidates.extend(dense_parts)

    deduped = _dedupe_keep_order(candidates, limit=64)
    scored: List[Tuple[float, str]] = []
    for item in deduped:
        if _is_structural_noise(item):
            continue
        score = _term_informativeness(item)
        if STRUCTURAL_CONNECTOR_PATTERN.search(item):
            score -= 0.22
        if INSTRUCTION_PREFIX_PATTERN.match(item):
            score -= 0.28
        if score <= 0:
            continue
        scored.append((score, item))

    scored.sort(key=lambda pair: (-pair[0], len(pair[1]), pair[1]))
    return _dedupe_keep_order([item for _, item in scored], limit=max(1, max_chunks))


def _extract_task_terms(target_task: str, limit: int = 16) -> List[str]:
    if not isinstance(target_task, str) or not target_task.strip():
        return []

    candidates: List[str] = []
    for quoted in _extract_quoted_segments(target_task):
        candidates.extend(_derive_core_chunks(quoted, max_chunks=3))

    for token in TASK_TERM_PATTERN.findall(target_task):
        norm = _normalize_text(token)
        if len(norm) < 2:
            continue
        if re.fullmatch(r"第?\d+章", norm):
            continue
        candidates.extend(_derive_core_chunks(norm, max_chunks=2))

    return _dedupe_keep_order(candidates, limit=max(1, int(limit or 1)))


def _build_clusters(keywords: List[str], enable_alias_expand: bool) -> List[Dict[str, Any]]:
    clusters: List[Dict[str, Any]] = []
    for keyword in keywords:
        root = _normalize_text(keyword)
        if not root:
            continue

        variants = [root]
        variants.extend(item for item in _derive_core_chunks(root, max_chunks=3) if item != root)

        if enable_alias_expand:
            for alias_root, aliases in ALIAS_TABLE.items():
                alias_root_norm = _normalize_text(alias_root)
                if not alias_root_norm:
                    continue
                if alias_root_norm == root or root in aliases or alias_root_norm in root:
                    variants.extend(_normalize_text(alias) for alias in aliases)

        variants = _dedupe_keep_order(variants, limit=4)
        clusters.append({"root": root, "variants": variants})

    return clusters


def govern_search_keywords(
    keywords: Optional[List[str]],
    target_task: str = "",
    max_keywords: int = 8,
    min_keywords: int = 2,
    enable_alias_expand: bool = True,
) -> Dict[str, Any]:
    """Normalize/clean/rank keywords for retrieval behavior without fixed word lists."""
    max_kw = max(1, int(max_keywords or 1))
    min_kw = max(1, int(min_keywords or 1))

    explicit_terms: List[str] = []
    for item in keywords or []:
        explicit_terms.extend(_derive_core_chunks(str(item), max_chunks=4))

    quoted_terms = _extract_quoted_segments(target_task)
    task_terms = _extract_task_terms(target_task, limit=max(max_kw * 3, 12))

    merged_pool = list(explicit_terms)
    if len(merged_pool) < min_kw:
        merged_pool.extend(task_terms)

    blocked: List[Dict[str, str]] = []
    candidates: List[str] = []
    weak_unanchored: List[str] = []
    first_seen: Dict[str, int] = {}
    target_text = str(target_task or "")
    task_set = {item.lower() for item in task_terms}

    for idx, raw in enumerate(merged_pool):
        norm = _normalize_text(raw)
        if not norm:
            continue
        if len(norm) < 2:
            blocked.append({"keyword": norm, "reason": "too_short"})
            continue
        if len(norm) > 24:
            norm = norm[:24]
        if _is_structural_noise(norm):
            blocked.append({"keyword": norm, "reason": "structural_noise"})
            continue
        if norm in INSTRUCTION_KEYWORDS:
            blocked.append({"keyword": norm, "reason": "instruction_keyword"})
            continue
        if norm in FUNCTION_KEYWORDS:
            blocked.append({"keyword": norm, "reason": "function_keyword"})
            continue
        key = norm.lower()
        anchored = (norm in target_text) or (key in task_set)
        configured_wide = norm in WIDE_KEYWORDS
        if configured_wide or (_is_two_char_cjk(norm) and not anchored):
            weak_unanchored.append(norm)
            if key not in first_seen:
                first_seen[key] = idx
            continue
        if key not in first_seen:
            first_seen[key] = idx
            candidates.append(norm)

    anchored_terms = [
        term
        for term in candidates
        if (term in target_text) or (term.lower() in task_set)
    ]
    if anchored_terms:
        anchored_keys = {item.lower() for item in anchored_terms}
        filtered_candidates: List[str] = []
        for term in candidates:
            key = term.lower()
            if key in anchored_keys:
                filtered_candidates.append(term)
                continue
            if any(anchor in term or term in anchor for anchor in anchored_terms):
                filtered_candidates.append(term)
                continue
            weak_unanchored.append(term)
        candidates = _dedupe_keep_order(filtered_candidates, limit=max_kw * 4)

    score_rows: List[Tuple[float, int, str]] = []
    quoted_set = {item.lower() for item in quoted_terms}
    explicit_set = {item.lower() for item in explicit_terms}

    for candidate in candidates:
        key = candidate.lower()
        score = _term_informativeness(candidate)
        if key in quoted_set:
            score += 0.45
        if key in explicit_set:
            score += 0.25
        score_rows.append((score, first_seen.get(key, 0), candidate))

    score_rows.sort(key=lambda row: (-row[0], row[1]))
    final_keywords = _dedupe_keep_order([item for _, __, item in score_rows], max_kw)

    weak_unanchored = _dedupe_keep_order(weak_unanchored, max_kw)
    suppressed_wide_terms: List[str] = []
    if final_keywords and weak_unanchored:
        suppressed_wide_terms = list(weak_unanchored)
    elif not final_keywords and weak_unanchored:
        anchor_candidates = [term for term in task_terms if not _is_two_char_cjk(term)]
        if anchor_candidates:
            final_keywords = _dedupe_keep_order(anchor_candidates[:1] + weak_unanchored[:1], max_kw)
            if len(weak_unanchored) > 1:
                suppressed_wide_terms.extend(weak_unanchored[1:])
        else:
            for term in weak_unanchored:
                blocked.append({"keyword": term, "reason": "wide_without_anchor"})

    if len(final_keywords) < min_kw:
        backfill = _dedupe_keep_order(task_terms, max_kw)
        final_keywords = _dedupe_keep_order(final_keywords + backfill, max_kw)

    clusters = _build_clusters(final_keywords, enable_alias_expand=enable_alias_expand)
    expanded_alias_terms = _dedupe_keep_order(
        [alias for cluster in clusters for alias in cluster.get("variants", [])[1:]],
        max_kw * 2,
    )

    return {
        "keywords": final_keywords,
        "clusters": clusters,
        "blocked": blocked,
        "suppressed_wide_terms": _dedupe_keep_order(suppressed_wide_terms, max_kw),
        "expanded_alias_terms": expanded_alias_terms,
        "derived_terms": _dedupe_keep_order(task_terms, max_kw),
        "rule_source": KEYWORD_RULES_SOURCE,
        "rule_sizes": {
            "instruction": len(INSTRUCTION_KEYWORDS),
            "wide": len(WIDE_KEYWORDS),
            "function": len(FUNCTION_KEYWORDS),
            "alias_roots": len(ALIAS_TABLE),
        },
    }


def expand_cluster_keywords(clusters: Optional[List[Dict[str, Any]]], max_keywords: int = 8) -> List[str]:
    """Flatten keyword clusters (root + first variant) with stable order."""
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

    return _dedupe_keep_order(out, max(1, int(max_keywords or 1)))
