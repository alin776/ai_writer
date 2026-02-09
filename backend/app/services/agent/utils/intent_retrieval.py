# -*- coding: utf-8 -*-
"""Intent-driven retrieval helpers for Explore V3.

V3 目标：
1) 从“任务语义槽位”而不是整句拆词生成检索计划；
2) 强化关系/时序/结果等事件约束，减少关键词换序空转；
3) 在保留词法检索执行层的前提下，提供可解释的覆盖裁判与自适应改写。
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

try:
    from app.services.agent.utils.query_governor import govern_search_keywords
except Exception:
    _query_governor_path = Path(__file__).resolve().with_name("query_governor.py")
    _query_governor_spec = importlib.util.spec_from_file_location(
        "query_governor_fallback",
        _query_governor_path,
    )
    if not _query_governor_spec or not _query_governor_spec.loader:
        raise
    _query_governor_module = importlib.util.module_from_spec(_query_governor_spec)
    _query_governor_spec.loader.exec_module(_query_governor_module)
    govern_search_keywords = _query_governor_module.govern_search_keywords


TERM_SPLIT_PATTERN = re.compile(r"[,\s，。；;：:、|｜/]+")
QUOTE_PATTERN = re.compile(r"[\"'“”‘’「」『』《》](.+?)[\"'“”‘’「」『』《》]")
TASK_TERM_PATTERN = re.compile(r"[\u4e00-\u9fffA-Za-z0-9]{2,24}")
STRUCTURAL_CONNECTOR_PATTERN = re.compile(r"(?:关于|围绕|针对|有关|以及|并且|并|和|与|及|是否|的)")
INSTRUCTION_PREFIX_PATTERN = re.compile(r"^(?:查找|寻找|检索|搜索|定位|确认|分析|核查|提取)")

# Structural exclusion markers (no domain word dictionaries).
EXCLUSION_MARKER_PATTERN = re.compile(r"(?:^|[\s,，;；])[-!~]([\u4e00-\u9fffA-Za-z0-9]{2,24})")
EXCLUSION_NOT_PATTERN = re.compile(r"\bNOT\s+([A-Za-z0-9_\-]{2,24})\b", re.IGNORECASE)


@dataclass
class RelationAnchor:
    left: str
    action: str
    right: str = ""
    window: int = 18

    def terms(self) -> List[str]:
        values = [self.left, self.action]
        if self.right:
            values.append(self.right)
        return _dedupe_keep_order(values, limit=3)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "left": self.left,
            "action": self.action,
            "right": self.right,
            "window": int(self.window),
        }


@dataclass
class IntentSpec:
    intent_id: str
    goal: str
    must_have: List[str] = field(default_factory=list)
    nice_to_have: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    exclusions: List[str] = field(default_factory=list)
    evidence_shape: str = "paragraph"
    stop_rule: Dict[str, Any] = field(default_factory=dict)
    source_keywords: List[str] = field(default_factory=list)

    # V3 semantic slots
    entity_terms: List[str] = field(default_factory=list)
    action_terms: List[str] = field(default_factory=list)
    timeline_terms: List[str] = field(default_factory=list)
    risk_terms: List[str] = field(default_factory=list)
    relation_anchors: List[RelationAnchor] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intent_id": self.intent_id,
            "goal": self.goal,
            "must_have": list(self.must_have),
            "nice_to_have": list(self.nice_to_have),
            "constraints": dict(self.constraints),
            "exclusions": list(self.exclusions),
            "evidence_shape": self.evidence_shape,
            "stop_rule": dict(self.stop_rule),
            "source_keywords": list(self.source_keywords),
            "entity_terms": list(self.entity_terms),
            "action_terms": list(self.action_terms),
            "timeline_terms": list(self.timeline_terms),
            "risk_terms": list(self.risk_terms),
            "relation_anchors": [item.to_dict() for item in self.relation_anchors],
        }


@dataclass
class ProbeSpec:
    probe_id: str
    probe_type: str
    terms_required: List[str] = field(default_factory=list)
    terms_optional: List[str] = field(default_factory=list)
    terms_excluded: List[str] = field(default_factory=list)
    chapter_scope: Optional[Tuple[int, int]] = None
    match_mode: str = "any"
    hypothesis: str = ""
    strategy: str = ""
    priority: int = 0
    signature: str = ""

    def all_terms(self, limit: int = 8) -> List[str]:
        return _dedupe_keep_order(list(self.terms_required) + list(self.terms_optional), limit=limit)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "probe_id": self.probe_id,
            "probe_type": self.probe_type,
            "terms_required": list(self.terms_required),
            "terms_optional": list(self.terms_optional),
            "terms_excluded": list(self.terms_excluded),
            "chapter_scope": list(self.chapter_scope) if self.chapter_scope else None,
            "match_mode": self.match_mode,
            "hypothesis": self.hypothesis,
            "strategy": self.strategy,
            "priority": self.priority,
            "signature": self.signature,
        }


@dataclass
class QueryProgram:
    intent_id: str
    probes: List[ProbeSpec] = field(default_factory=list)
    budget: Dict[str, int] = field(default_factory=dict)
    novelty_rule: str = "next probe must add new semantic slot coverage"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intent_id": self.intent_id,
            "probes": [probe.to_dict() for probe in self.probes],
            "budget": dict(self.budget),
            "novelty_rule": self.novelty_rule,
        }


@dataclass
class EvidenceCard:
    location: Dict[str, Any]
    text: str
    matched_terms: List[str]
    judge_score: float
    judge_reason: str
    covers_must_have: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "location": dict(self.location),
            "text": self.text,
            "matched_terms": list(self.matched_terms),
            "judge_score": round(float(self.judge_score), 4),
            "judge_reason": self.judge_reason,
            "covers_must_have": list(self.covers_must_have),
        }


@dataclass
class IterationState:
    seen_probe_signatures: Set[str] = field(default_factory=set)
    failed_reason_histogram: Dict[str, int] = field(default_factory=dict)
    novel_evidence_ratio: float = 0.0
    covered_must_have_set: Set[str] = field(default_factory=set)
    last_probe_signature: str = ""
    must_have_total: int = 0

    def clone(self) -> "IterationState":
        return IterationState(
            seen_probe_signatures=set(self.seen_probe_signatures),
            failed_reason_histogram=dict(self.failed_reason_histogram),
            novel_evidence_ratio=float(self.novel_evidence_ratio),
            covered_must_have_set=set(self.covered_must_have_set),
            last_probe_signature=self.last_probe_signature,
            must_have_total=int(self.must_have_total or 0),
        )

    def merge_from(self, other: Optional["IterationState"]) -> None:
        if not isinstance(other, IterationState):
            return
        self.seen_probe_signatures |= other.seen_probe_signatures
        for reason, count in other.failed_reason_histogram.items():
            self.failed_reason_histogram[reason] = self.failed_reason_histogram.get(reason, 0) + int(count or 0)
        self.covered_must_have_set |= other.covered_must_have_set
        self.must_have_total = max(self.must_have_total, other.must_have_total)
        if other.last_probe_signature:
            self.last_probe_signature = other.last_probe_signature
        self.novel_evidence_ratio = max(self.novel_evidence_ratio, other.novel_evidence_ratio)

    def mark_probe(self, signature: str) -> None:
        sign = str(signature or "").strip()
        if not sign:
            return
        self.seen_probe_signatures.add(sign)
        self.last_probe_signature = sign

    def mark_failure(self, reason: str) -> None:
        key = str(reason or "").strip().lower() or "unknown"
        self.failed_reason_histogram[key] = self.failed_reason_histogram.get(key, 0) + 1

    def update_coverage(self, covered_terms: Iterable[str], total_must_have: int) -> None:
        for term in covered_terms:
            normalized = _normalize_term(term)
            if normalized:
                self.covered_must_have_set.add(normalized)
        self.must_have_total = max(self.must_have_total, int(total_must_have or 0))
        if self.must_have_total > 0:
            self.novel_evidence_ratio = min(1.0, len(self.covered_must_have_set) / self.must_have_total)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "seen_probe_signatures": sorted(self.seen_probe_signatures),
            "failed_reason_histogram": dict(sorted(self.failed_reason_histogram.items())),
            "novel_evidence_ratio": round(float(self.novel_evidence_ratio), 4),
            "covered_must_have_set": sorted(self.covered_must_have_set),
            "last_probe_signature": self.last_probe_signature,
            "must_have_total": self.must_have_total,
        }


def _normalize_term(text: Any) -> str:
    value = str(text or "").strip()
    if not value:
        return ""
    value = value.strip("\"'“”‘’《》()[]{}")
    value = re.sub(r"\s+", "", value)
    return value


def _split_terms(text: str) -> List[str]:
    if not isinstance(text, str):
        return []
    return [part.strip() for part in TERM_SPLIT_PATTERN.split(text) if part and part.strip()]


def _safe_scope_tuple(scope: Any) -> Optional[Tuple[int, int]]:
    if isinstance(scope, tuple) and len(scope) == 2:
        start, end = scope
    elif isinstance(scope, list) and len(scope) == 2:
        start, end = scope[0], scope[1]
    else:
        return None
    try:
        start_int = int(start)
        end_int = int(end)
    except Exception:
        return None
    if start_int > end_int:
        start_int, end_int = end_int, start_int
    return (start_int, end_int)


def _dedupe_keep_order(values: Iterable[Any], limit: int = 0) -> List[str]:
    out: List[str] = []
    seen: Set[str] = set()
    for raw in values:
        value = _normalize_term(raw)
        if not value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(value)
        if limit > 0 and len(out) >= limit:
            break
    return out


def _term_informativeness(term: str) -> float:
    value = _normalize_term(term)
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


def _derive_core_chunks(term: str, max_chunks: int = 3) -> List[str]:
    raw = str(term or "")
    base = _normalize_term(raw)
    if len(base) < 2:
        return []

    is_composite = bool(re.search(r"[\s,，。；;：:、|｜/\"'“”‘’「」『』《》]", raw))
    quoted_chunks = [_normalize_term(item) for item in QUOTE_PATTERN.findall(raw)]
    quoted_chunks = [item for item in quoted_chunks if _is_quality_term(item)]
    if is_composite and quoted_chunks:
        return _dedupe_keep_order(quoted_chunks, limit=max(1, max_chunks))

    candidates: List[str] = [] if is_composite else [base]
    candidates.extend(quoted_chunks)
    candidates.extend(_split_terms(base))
    candidates.extend(part for part in STRUCTURAL_CONNECTOR_PATTERN.split(base) if part)
    candidates.extend(_normalize_term(item) for item in TASK_TERM_PATTERN.findall(base))

    scored: List[Tuple[float, str]] = []
    seen = set()
    for raw in candidates:
        value = _normalize_term(raw)
        if not value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        if not _is_quality_term(value):
            continue
        score = _term_informativeness(value)
        if STRUCTURAL_CONNECTOR_PATTERN.search(value):
            score -= 0.22
        if INSTRUCTION_PREFIX_PATTERN.match(value):
            score -= 0.28
        if score <= 0:
            continue
        scored.append((score, value))

    scored.sort(key=lambda item: (-item[0], len(item[1]), item[1]))
    return [item for _, item in scored[: max(1, max_chunks)]]


def _is_quality_term(term: str) -> bool:
    value = _normalize_term(term)
    if len(value) < 2 or len(value) > 24:
        return False
    if re.fullmatch(r"\d+", value):
        return False
    if re.fullmatch(r"[\W_]+", value):
        return False
    if value.count("'") + value.count('"') > 0:
        return False
    if any(char in value for char in ("。", "，", "；", "：", "?", "？", "!", "！")):
        return False
    if len(set(value)) <= 1:
        return False
    return True


def _is_instruction_shell(term: str) -> bool:
    value = _normalize_term(term)
    if not value:
        return False
    if INSTRUCTION_PREFIX_PATTERN.match(value):
        return True
    if len(value) >= 8 and STRUCTURAL_CONNECTOR_PATTERN.search(value) and value.endswith("描述"):
        return True
    return False


def _canonical_probe_terms(values: Iterable[Any]) -> List[str]:
    tokens: List[str] = []
    for raw in values:
        value = _normalize_term(raw)
        if not value:
            continue
        chunks = _derive_core_chunks(value, max_chunks=3)
        if chunks:
            tokens.append(chunks[0].lower())
        else:
            tokens.append(value.lower())

    deduped = sorted(set(tokens))
    return deduped[:16]


def _is_relation_hit(text_lower: str, relation: RelationAnchor) -> bool:
    left = relation.left.lower()
    action = relation.action.lower() if relation.action else ""
    right = relation.right.lower() if relation.right else ""
    if action:
        negation_pattern = re.compile(
            rf"(?:没有|并未|未|没|不|not|never)[^，。；;:：!！?？]{{0,6}}{re.escape(action)}"
        )
        if negation_pattern.search(text_lower):
            return False
    if left not in text_lower:
        return False

    left_pos = text_lower.find(left)
    action_pos = text_lower.find(action) if action else left_pos
    if left_pos < 0 or action_pos < 0:
        return False
    if abs(left_pos - action_pos) > int(relation.window or 18):
        return False

    if right:
        right_pos = text_lower.find(right)
        if right_pos < 0:
            return False
        if abs(right_pos - action_pos) > int(relation.window or 18):
            return False
    return True


class IntentCompiler:
    """Compile target task into semantic slots + lexical anchors."""

    def sanitize_external_keywords(self, raw_keywords: Sequence[Any], target_task: str, limit: int = 8) -> List[str]:
        values = _dedupe_keep_order(raw_keywords or [], limit=24)
        if not values:
            return []

        governed = govern_search_keywords(
            keywords=values,
            target_task=target_task or "",
            max_keywords=max(limit, 1),
            min_keywords=1,
            enable_alias_expand=True,
        )
        structural_backfill: List[str] = []
        for value in values:
            chunks = _derive_core_chunks(value, max_chunks=3)
            if chunks:
                structural_backfill.append(chunks[0])
        normalized = _dedupe_keep_order((governed.get("keywords") or []) + structural_backfill, limit=24)
        filtered = [item for item in normalized if _is_quality_term(item) and not _is_instruction_shell(item)]
        return _dedupe_keep_order(filtered or normalized, limit=max(limit, 1))

    def compile(
        self,
        target_task: str,
        seed_keywords: Optional[Sequence[str]] = None,
        recent_keywords: Optional[Sequence[str]] = None,
        chapter_scope: Optional[Tuple[int, int]] = None,
    ) -> IntentSpec:
        goal = str(target_task or "").strip()

        quoted_terms = self._extract_quoted_terms(goal)
        task_terms = self._extract_task_terms(goal)
        seed_terms = self.sanitize_external_keywords(seed_keywords or [], goal, limit=10)
        recent_terms = self.sanitize_external_keywords(recent_keywords or [], goal, limit=10)

        base_terms = _dedupe_keep_order(quoted_terms + seed_terms + task_terms + recent_terms, limit=24)
        relation_anchors = self._extract_relation_anchors(goal, base_terms)
        action_terms = self._extract_actions(goal, relation_anchors, seed_terms, task_terms)
        timeline_terms = self._extract_timeline_terms(goal)
        risk_terms = self._extract_risk_terms(goal)

        entity_candidates = [
            term
            for term in (quoted_terms + seed_terms + task_terms)
            if term not in action_terms and term not in timeline_terms and term not in risk_terms
        ]
        entity_terms = _dedupe_keep_order([term for term in entity_candidates if _is_quality_term(term)], limit=8)
        entity_terms = [term for term in entity_terms if not _is_instruction_shell(term)]

        must_have = self._build_must_have(
            quoted_terms=quoted_terms,
            entity_terms=entity_terms,
            action_terms=action_terms,
            relation_anchors=relation_anchors,
            fallback_terms=seed_terms + task_terms,
        )
        nice_to_have = _dedupe_keep_order(
            recent_terms + timeline_terms + risk_terms + [item for item in entity_terms if item not in must_have],
            limit=10,
        )

        exclusions = self._extract_exclusions(goal)
        evidence_shape = self._detect_evidence_shape(goal)

        scope = _safe_scope_tuple(chapter_scope)
        constraints: Dict[str, Any] = {}
        if scope:
            constraints["chapter_scope"] = [scope[0], scope[1]]

        stop_rule = {
            "min_must_have_coverage": 0.65,
            "min_relation_hits": 1 if relation_anchors else 0,
            "max_zero_growth_rounds": 2,
        }

        intent_id = self._stable_intent_id(
            goal=goal,
            must_have=must_have,
            exclusions=exclusions,
            chapter_scope=scope,
            relation_anchors=relation_anchors,
        )

        return IntentSpec(
            intent_id=intent_id,
            goal=goal[:500],
            must_have=must_have,
            nice_to_have=nice_to_have,
            constraints=constraints,
            exclusions=exclusions,
            evidence_shape=evidence_shape,
            stop_rule=stop_rule,
            source_keywords=_dedupe_keep_order(seed_terms + recent_terms, limit=10),
            entity_terms=entity_terms,
            action_terms=action_terms,
            timeline_terms=timeline_terms,
            risk_terms=risk_terms,
            relation_anchors=relation_anchors,
        )

    def _extract_quoted_terms(self, text: str) -> List[str]:
        terms: List[str] = []
        for match in QUOTE_PATTERN.findall(text or ""):
            normalized = _normalize_term(match)
            if _is_quality_term(normalized):
                terms.append(normalized)
        return _dedupe_keep_order(terms, limit=10)

    def _extract_task_terms(self, text: str) -> List[str]:
        terms: List[str] = []
        for raw in TASK_TERM_PATTERN.findall(text or ""):
            chunks = _derive_core_chunks(raw, max_chunks=1)
            if not chunks:
                continue
            normalized = chunks[0]
            if re.fullmatch(r"第?\d+章", normalized):
                continue
            if _is_instruction_shell(normalized):
                continue
            terms.append(normalized)
        return _dedupe_keep_order(terms, limit=20)

    def _extract_actions(
        self,
        goal: str,
        relation_anchors: Sequence[RelationAnchor],
        seed_terms: Sequence[str],
        task_terms: Sequence[str],
    ) -> List[str]:
        values: List[str] = []
        for relation in relation_anchors:
            if _is_quality_term(relation.action):
                values.append(relation.action)

        # Backfill with concise, informative seed/task terms (no fixed verb dictionary).
        candidates = _dedupe_keep_order(list(seed_terms) + list(task_terms), limit=24)
        scored: List[Tuple[float, str]] = []
        for term in candidates:
            value = _normalize_term(term)
            if not _is_quality_term(value):
                continue
            if len(value) > 8:
                continue
            if value and value in (goal or ""):
                scored.append((_term_informativeness(value), value))
        scored.sort(key=lambda item: (-item[0], len(item[1]), item[1]))
        values.extend(item for _, item in scored[:4])
        return _dedupe_keep_order(values, limit=6)

    def _extract_timeline_terms(self, goal: str) -> List[str]:
        values: List[str] = []
        source = str(goal or "")
        values.extend(re.findall(r"第[一二三四五六七八九十百千万0-9]+[次章回幕步]", source))
        values.extend(
            re.findall(
                r"\b(first|second|third|initial|before|after|previous|next)\b",
                source,
                flags=re.IGNORECASE,
            )
        )
        return _dedupe_keep_order(values, limit=4)

    def _extract_risk_terms(self, goal: str) -> List[str]:
        return []

    def _extract_relation_anchors(
        self,
        goal: str,
        candidate_terms: Sequence[str],
    ) -> List[RelationAnchor]:
        anchors: List[RelationAnchor] = []
        source = str(goal or "")
        if not source:
            return anchors

        normalized_candidates: List[str] = []
        for raw in _dedupe_keep_order(candidate_terms, limit=24):
            chunks = _derive_core_chunks(raw, max_chunks=2)
            if chunks:
                normalized_candidates.append(chunks[0])
            elif _is_quality_term(raw):
                normalized_candidates.append(raw)
        terms = [item for item in _dedupe_keep_order(normalized_candidates, limit=16) if _is_quality_term(item)]

        occurrences: List[Tuple[int, int, str]] = []
        for term in terms:
            start = source.find(term)
            if start < 0:
                continue
            occurrences.append((start, start + len(term), term))
        occurrences.sort(key=lambda item: item[0])

        # 优先从紧邻三元组抽取关系（left-action-right），避免把整句壳词当 action。
        compact_occurrences = [
            item
            for item in sorted(occurrences, key=lambda it: (it[0], (it[1] - it[0])))
            if 2 <= len(item[2]) <= 8 and not INSTRUCTION_PREFIX_PATTERN.match(item[2])
        ]
        pruned_occurrences: List[Tuple[int, int, str]] = []
        for item in compact_occurrences:
            if pruned_occurrences and item[0] < pruned_occurrences[-1][1]:
                prev = pruned_occurrences[-1]
                prev_len = prev[1] - prev[0]
                cur_len = item[1] - item[0]
                if cur_len < prev_len:
                    pruned_occurrences[-1] = item
                continue
            pruned_occurrences.append(item)

        for idx in range(len(pruned_occurrences) - 2):
            left_item = pruned_occurrences[idx]
            action_item = pruned_occurrences[idx + 1]
            right_item = pruned_occurrences[idx + 2]
            left_term = left_item[2]
            action_term = action_item[2]
            right_term = right_item[2]
            if (
                not _is_quality_term(left_term)
                or not _is_quality_term(action_term)
                or not _is_quality_term(right_term)
            ):
                continue
            if INSTRUCTION_PREFIX_PATTERN.match(left_term) or INSTRUCTION_PREFIX_PATTERN.match(action_term):
                continue
            span = right_item[1] - left_item[0]
            if span > 30:
                continue
            anchors.append(
                RelationAnchor(
                    left=left_term,
                    action=action_term,
                    right=right_term,
                    window=max(10, min(30, span + 6)),
                )
            )

        for idx in range(len(occurrences) - 1):
            left_start, left_end, left_term = occurrences[idx]
            right_start, right_end, right_term = occurrences[idx + 1]
            if left_term == right_term:
                continue
            between = source[left_end:right_start]
            action_candidates = _derive_core_chunks(between, max_chunks=2)
            action_term = action_candidates[0] if action_candidates else ""
            if not _is_quality_term(action_term):
                continue
            span = max(8, min(36, right_end - left_start + 8))
            anchors.append(
                RelationAnchor(
                    left=left_term,
                    action=action_term,
                    right=right_term,
                    window=span,
                )
            )

        compact_terms = [item for item in terms if 2 <= len(item) <= 8]
        pruned_compact_terms: List[str] = []
        for term in compact_terms:
            if any(other != term and len(other) <= len(term) and other in term for other in compact_terms):
                continue
            pruned_compact_terms.append(term)
        fallback_terms = pruned_compact_terms or compact_terms

        if not anchors and len(fallback_terms) >= 3:
            anchors.append(RelationAnchor(left=fallback_terms[0], action=fallback_terms[1], right=fallback_terms[2], window=18))
        elif not anchors and len(fallback_terms) == 2:
            anchors.append(RelationAnchor(left=fallback_terms[0], action=fallback_terms[1], right="", window=16))
        elif not anchors and len(terms) >= 3:
            anchors.append(RelationAnchor(left=terms[0], action=terms[1], right=terms[2], window=18))
        elif not anchors and len(terms) == 2:
            anchors.append(RelationAnchor(left=terms[0], action=terms[1], right="", window=16))

        deduped: List[RelationAnchor] = []
        seen: Set[str] = set()
        for anchor in anchors:
            sign = "|".join(anchor.terms()).lower()
            if sign in seen:
                continue
            seen.add(sign)
            deduped.append(anchor)
            if len(deduped) >= 3:
                break
        return deduped

    def _build_must_have(
        self,
        *,
        quoted_terms: Sequence[str],
        entity_terms: Sequence[str],
        action_terms: Sequence[str],
        relation_anchors: Sequence[RelationAnchor],
        fallback_terms: Sequence[str],
    ) -> List[str]:
        must_terms: List[str] = []
        must_terms.extend(list(quoted_terms)[:3])

        for anchor in relation_anchors[:2]:
            must_terms.extend(anchor.terms())

        must_terms.extend(list(action_terms)[:2])
        must_terms.extend(list(entity_terms)[:3])

        if not must_terms:
            must_terms.extend(list(fallback_terms)[:4])

        filtered = [term for term in must_terms if _is_quality_term(term)]
        filtered = [term for term in filtered if not _is_instruction_shell(term)]
        return _dedupe_keep_order(filtered, limit=8)

    def _extract_exclusions(self, text: str) -> List[str]:
        exclusions: List[str] = []
        source = str(text or "")
        for match in EXCLUSION_MARKER_PATTERN.findall(source):
            normalized = _normalize_term(match)
            if _is_quality_term(normalized):
                exclusions.append(normalized)
        for match in EXCLUSION_NOT_PATTERN.findall(source):
            normalized = _normalize_term(match)
            if _is_quality_term(normalized):
                exclusions.append(normalized)
        return _dedupe_keep_order(exclusions, limit=6)

    def _detect_evidence_shape(self, text: str) -> str:
        return "paragraph"

    def _stable_intent_id(
        self,
        *,
        goal: str,
        must_have: Sequence[str],
        exclusions: Sequence[str],
        chapter_scope: Optional[Tuple[int, int]],
        relation_anchors: Sequence[RelationAnchor],
    ) -> str:
        relation_sign = ",".join("/".join(item.terms()) for item in relation_anchors)
        digest_payload = "|".join(
            [
                goal[:300],
                ",".join(must_have),
                ",".join(exclusions),
                str(chapter_scope or ""),
                relation_sign,
            ]
        )
        return hashlib.sha1(digest_payload.encode("utf-8")).hexdigest()[:16]


class QueryProgramBuilder:
    """Build slot-driven lexical probes from IntentSpec."""

    def build(
        self,
        intent: IntentSpec,
        manual_keywords: Optional[Sequence[str]],
        requested_match_mode: str,
        chapter_scope: Optional[Tuple[int, int]],
        iteration_state: IterationState,
        max_probes: int = 8,
    ) -> QueryProgram:
        mode = str(requested_match_mode or "").strip().lower()
        if mode not in ("any", "all", "phrase"):
            mode = "all" if len(intent.must_have) > 1 else "phrase"

        manual_terms = _dedupe_keep_order(manual_keywords or [], limit=10)
        manual_terms = [item for item in manual_terms if _is_quality_term(item)]

        anchor_terms = _dedupe_keep_order(
            list(manual_terms)
            + list(intent.must_have)
            + list(intent.entity_terms)
            + list(intent.action_terms),
            limit=12,
        )
        source_backfill = [item for item in intent.source_keywords if item not in anchor_terms]
        anchor_terms = _dedupe_keep_order(anchor_terms + source_backfill[:3], limit=12)
        anchor_terms = [item for item in anchor_terms if _is_quality_term(item)]

        safe_scope = _safe_scope_tuple(chapter_scope)
        probes: List[ProbeSpec] = []

        for relation in intent.relation_anchors[:2]:
            required = relation.terms()
            optional = _dedupe_keep_order(intent.timeline_terms + intent.risk_terms + anchor_terms, limit=4)
            probes.append(
                self._new_probe(
                    probe_type="relation",
                    required=required,
                    optional=[item for item in optional if item not in required],
                    excluded=intent.exclusions,
                    scope=safe_scope,
                    match_mode="all" if len(required) > 1 else "phrase",
                    hypothesis=f"验证关系链：{'/'.join(required)}",
                    strategy="relation_probe",
                    priority=1,
                )
            )

        if anchor_terms:
            required = anchor_terms[:2]
            optional = anchor_terms[2:5]
            probes.append(
                self._new_probe(
                    probe_type="core_boolean",
                    required=required,
                    optional=optional,
                    excluded=intent.exclusions,
                    scope=safe_scope,
                    match_mode=mode,
                    hypothesis="验证核心语义槽位共现",
                    strategy="core_probe",
                    priority=2,
                )
            )

        if len(anchor_terms) >= 2:
            probes.append(
                self._new_probe(
                    probe_type="proximity",
                    required=anchor_terms[:2],
                    optional=anchor_terms[2:4],
                    excluded=intent.exclusions,
                    scope=safe_scope,
                    match_mode="any",
                    hypothesis=f"验证邻近关系：{anchor_terms[0]} ~ {anchor_terms[1]}",
                    strategy="proximity_probe",
                    priority=2,
                )
            )

        if intent.timeline_terms:
            probes.append(
                self._new_probe(
                    probe_type="timeline",
                    required=anchor_terms[:1] or intent.must_have[:1],
                    optional=_dedupe_keep_order(intent.timeline_terms + anchor_terms[1:3], limit=4),
                    excluded=intent.exclusions,
                    scope=safe_scope,
                    match_mode="any",
                    hypothesis="补强时序约束（第一次/先后）",
                    strategy="timeline_probe",
                    priority=3,
                )
            )

        if intent.risk_terms:
            probes.append(
                self._new_probe(
                    probe_type="risk",
                    required=anchor_terms[:1] or intent.must_have[:1],
                    optional=_dedupe_keep_order(intent.risk_terms + anchor_terms[1:3], limit=4),
                    excluded=intent.exclusions,
                    scope=safe_scope,
                    match_mode="any",
                    hypothesis="补强潜在影响约束",
                    strategy="risk_probe",
                    priority=3,
                )
            )

        for term in intent.must_have[:3]:
            probes.append(
                self._new_probe(
                    probe_type="anchor_fallback",
                    required=[term],
                    optional=[],
                    excluded=intent.exclusions,
                    scope=safe_scope,
                    match_mode="phrase",
                    hypothesis=f"单锚点回查：{term}",
                    strategy="anchor_probe",
                    priority=4,
                )
            )

        deduped: List[ProbeSpec] = []
        seen_signatures: Set[str] = set()
        seen_semantic_terms: List[Set[str]] = []
        for probe in sorted(probes, key=lambda item: (item.priority, item.probe_type)):
            if not probe.signature or probe.signature in seen_signatures:
                continue
            if probe.signature in iteration_state.seen_probe_signatures:
                continue
            canonical_terms = set(
                _canonical_probe_terms(list(probe.terms_required) + list(probe.terms_optional))
            )
            semantic_duplicate = False
            if canonical_terms:
                for existing in seen_semantic_terms:
                    union = canonical_terms | existing
                    if not union:
                        continue
                    overlap = len(canonical_terms & existing) / len(union)
                    if overlap >= 0.82:
                        semantic_duplicate = True
                        break
            if semantic_duplicate:
                continue
            seen_signatures.add(probe.signature)
            if canonical_terms:
                seen_semantic_terms.append(canonical_terms)
            probe.probe_id = f"probe_{len(deduped) + 1}"
            deduped.append(probe)
            if len(deduped) >= max(1, max_probes):
                break

        budget = {
            "max_rounds": max(3, len(deduped)),
            "max_probes_per_round": 1,
        }
        return QueryProgram(
            intent_id=intent.intent_id,
            probes=deduped,
            budget=budget,
            novelty_rule="next probe must add uncovered slot terms or stronger constraints",
        )

    def pick_next_probe(self, program: QueryProgram, iteration_state: IterationState) -> Optional[ProbeSpec]:
        for probe in program.probes:
            if probe.signature not in iteration_state.seen_probe_signatures:
                return probe
        return None

    def probe_to_search_payload(self, probe: ProbeSpec, limit: int = 100) -> Dict[str, Any]:
        proximity_terms: List[str] = []
        proximity_window = 12
        if probe.probe_type in ("relation", "proximity"):
            proximity_terms = _dedupe_keep_order(list(probe.terms_required) + list(probe.terms_optional[:1]), limit=3)
            proximity_window = 16 if probe.probe_type == "relation" else 10

        payload: Dict[str, Any] = {
            "keywords": probe.all_terms(limit=8),
            "terms_required": list(probe.terms_required),
            "terms_optional": list(probe.terms_optional),
            "terms_excluded": list(probe.terms_excluded),
            "proximity_terms": proximity_terms,
            "proximity_window": proximity_window,
            "match_mode": probe.match_mode or "any",
            "limit": int(limit if isinstance(limit, int) and limit > 0 else 100),
            "strategy": probe.strategy or probe.probe_type,
            "probe_signature": probe.signature,
            "probe_hypothesis": probe.hypothesis,
            "probe_type": probe.probe_type,
            "search_intent": probe.hypothesis[:120],
        }
        if probe.chapter_scope:
            payload["chapter_range"] = [probe.chapter_scope[0], probe.chapter_scope[1]]
        return payload

    def _new_probe(
        self,
        probe_type: str,
        required: Sequence[str],
        optional: Sequence[str],
        excluded: Sequence[str],
        scope: Optional[Tuple[int, int]],
        match_mode: str,
        hypothesis: str,
        strategy: str,
        priority: int,
    ) -> ProbeSpec:
        terms_required = _dedupe_keep_order([item for item in required if _is_quality_term(str(item))], limit=6)
        terms_optional = _dedupe_keep_order([item for item in optional if _is_quality_term(str(item))], limit=6)
        terms_excluded = _dedupe_keep_order([item for item in excluded if _is_quality_term(str(item))], limit=6)
        signature = self._build_signature(
            probe_type=probe_type,
            terms_required=terms_required,
            terms_optional=terms_optional,
            terms_excluded=terms_excluded,
            scope=scope,
            match_mode=match_mode,
        )
        return ProbeSpec(
            probe_id="",
            probe_type=probe_type,
            terms_required=terms_required,
            terms_optional=terms_optional,
            terms_excluded=terms_excluded,
            chapter_scope=scope,
            match_mode=match_mode,
            hypothesis=hypothesis,
            strategy=strategy,
            priority=priority,
            signature=signature,
        )

    @staticmethod
    def _build_signature(
        probe_type: str,
        terms_required: Sequence[str],
        terms_optional: Sequence[str],
        terms_excluded: Sequence[str],
        scope: Optional[Tuple[int, int]],
        match_mode: str,
    ) -> str:
        normalized_required = sorted({_normalize_term(term).lower() for term in terms_required if _normalize_term(term)})
        canonical_required = _canonical_probe_terms(terms_required)
        if canonical_required:
            normalized_required = sorted(set(canonical_required))
        normalized_optional = sorted({_normalize_term(term).lower() for term in terms_optional if _normalize_term(term)})
        canonical_optional = _canonical_probe_terms(terms_optional)
        if canonical_optional:
            normalized_optional = sorted(set(canonical_optional))
        normalized_excluded = sorted({_normalize_term(term).lower() for term in terms_excluded if _normalize_term(term)})
        scope_text = "all"
        if scope:
            scope_text = f"{scope[0]}-{scope[1]}"
        raw = "|".join(
            [
                str(probe_type or ""),
                str(match_mode or ""),
                ",".join(normalized_required),
                ",".join(normalized_optional),
                ",".join(normalized_excluded),
                scope_text,
            ]
        )
        return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


class EvidenceJudge:
    """Judge lexical hits with slot-aware coverage scoring."""

    def judge(
        self,
        results: Sequence[Dict[str, Any]],
        intent: IntentSpec,
        active_keywords: Sequence[str],
        min_score: float = 0.2,
    ) -> Dict[str, Any]:
        must_terms = _dedupe_keep_order(intent.must_have, limit=8)
        keyword_terms = _dedupe_keep_order(active_keywords, limit=8)
        relation_anchors = list(intent.relation_anchors)
        timeline_terms = _dedupe_keep_order(intent.timeline_terms, limit=4)
        risk_terms = _dedupe_keep_order(intent.risk_terms, limit=4)

        cards: List[EvidenceCard] = []
        covered_terms: Set[str] = set()
        score_total = 0.0
        relation_hits = 0
        timeline_hits = 0

        for item in results:
            if not isinstance(item, dict):
                continue
            text = str(item.get("text") or item.get("content") or item.get("snippet") or "")
            if not text:
                continue
            lowered = text.lower()

            matched_must = [term for term in must_terms if term.lower() in lowered]
            matched_keywords = [term for term in keyword_terms if term.lower() in lowered]

            relation_hit = any(_is_relation_hit(lowered, relation) for relation in relation_anchors)
            timeline_hit = any(term.lower() in lowered for term in timeline_terms)
            risk_hit = any(term.lower() in lowered for term in risk_terms)

            if relation_hit:
                relation_hits += 1
            if timeline_hit:
                timeline_hits += 1

            locator_bonus = 0.1 if isinstance(item.get("chapter_order"), int) and isinstance(item.get("paragraph_index"), int) else 0.0
            must_ratio = (len(matched_must) / len(must_terms)) if must_terms else 0.0
            keyword_ratio = (len(matched_keywords) / len(keyword_terms)) if keyword_terms else 0.0
            relation_bonus = 0.2 if relation_hit else 0.0
            timeline_bonus = 0.05 if timeline_hit else 0.0
            risk_bonus = 0.05 if risk_hit else 0.0

            score = (must_ratio * 0.55) + (keyword_ratio * 0.15) + relation_bonus + timeline_bonus + risk_bonus + locator_bonus
            score_total += score

            if relation_hit:
                reason = "relation anchor matched"
            elif matched_must:
                reason = "matched intent anchors"
            else:
                reason = "weak lexical hit"

            card = EvidenceCard(
                location={
                    "chapter_order": item.get("chapter_order"),
                    "paragraph_index": item.get("paragraph_index"),
                    "chapter_id": item.get("chapter_id") or "",
                    "node_id": item.get("node_id") or "",
                },
                text=text[:400],
                matched_terms=_dedupe_keep_order(matched_keywords, limit=6),
                judge_score=float(score),
                judge_reason=reason,
                covers_must_have=_dedupe_keep_order(matched_must, limit=6),
            )
            cards.append(card)

            if score >= min_score or (relation_hit and matched_must):
                covered_terms.update(card.covers_must_have)

        avg_score = (score_total / len(cards)) if cards else 0.0
        coverage_ratio = (len(covered_terms) / len(must_terms)) if must_terms else 0.0

        min_required_coverage = float((intent.stop_rule or {}).get("min_must_have_coverage") or 0.6)
        min_relation_hits = int((intent.stop_rule or {}).get("min_relation_hits") or 0)

        if not cards:
            failure_reason = "lexical_miss"
        elif coverage_ratio >= min_required_coverage and relation_hits >= min_relation_hits:
            failure_reason = ""
        elif relation_anchors and relation_hits == 0:
            failure_reason = "relation_miss"
        elif timeline_terms and timeline_hits == 0:
            failure_reason = "timeline_miss"
        elif avg_score < min_score:
            failure_reason = "semantic_mismatch"
        else:
            failure_reason = "insufficient_coverage"

        return {
            "cards": [card.to_dict() for card in cards],
            "covered_terms": sorted(covered_terms),
            "coverage_ratio": round(float(coverage_ratio), 4),
            "failure_reason": failure_reason,
            "avg_score": round(float(avg_score), 4),
            "relation_hits": int(relation_hits),
            "timeline_hits": int(timeline_hits),
        }


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
    """Generate deterministic rewrites from judge failure reasons (V3)."""

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
        reason = str(failure_reason or "").strip().lower() or "lexical_miss"

        intent_data = intent_spec or {}
        state_data = iteration_state or {}

        must_have = _dedupe_keep_order(intent_data.get("must_have") or [], limit=8)
        timeline_terms = _dedupe_keep_order(intent_data.get("timeline_terms") or [], limit=4)
        risk_terms = _dedupe_keep_order(intent_data.get("risk_terms") or [], limit=4)
        source_keywords = _dedupe_keep_order(intent_data.get("source_keywords") or [], limit=8)

        relation_raw = intent_data.get("relation_anchors") or []
        relation_terms: List[str] = []
        if isinstance(relation_raw, list):
            for item in relation_raw:
                if not isinstance(item, dict):
                    continue
                relation_terms.extend([item.get("left"), item.get("action"), item.get("right")])
        relation_terms = _dedupe_keep_order(relation_terms, limit=6)

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
            + list(uncovered),
            limit=10,
        )
        excluded = _dedupe_keep_order(latest_terms_excluded, limit=6)

        lexical_miss_count = int((state_data.get("failed_reason_histogram") or {}).get("lexical_miss", 0) or 0)
        scope = self._rewrite_scope(latest_scope, reason=reason, lexical_miss_count=lexical_miss_count)

        if reason == "relation_miss" and relation_terms:
            required = _dedupe_keep_order(relation_terms[:3], limit=3)
            optional = _dedupe_keep_order(timeline_terms + risk_terms + anchors, limit=4)
            return AdaptiveRewrite(
                strategy="adaptive_relation_focus",
                reason="已有字面命中但关系不成立，改为关系槽位聚焦",
                search_intent="聚焦关系约束重搜",
                keywords=_dedupe_keep_order(required + optional, limit=7),
                terms_required=required,
                terms_optional=[item for item in optional if item not in required],
                terms_excluded=excluded,
                proximity_terms=_dedupe_keep_order(required[:3], limit=3),
                match_mode="all" if len(required) > 1 else "phrase",
                proximity_window=18,
                chapter_range=scope,
                limit=120,
            )

        if reason == "timeline_miss" and timeline_terms:
            required = _dedupe_keep_order(list(latest_terms_required) or must_have[:1] or anchors[:1], limit=2)
            optional = _dedupe_keep_order(timeline_terms + list(latest_terms_optional) + anchors, limit=5)
            return AdaptiveRewrite(
                strategy="adaptive_timeline_focus",
                reason="缺少时序证据，补强首次/先后约束",
                search_intent="补强时序线索重搜",
                keywords=_dedupe_keep_order(required + optional, limit=7),
                terms_required=required,
                terms_optional=[item for item in optional if item not in required],
                terms_excluded=excluded,
                proximity_terms=_dedupe_keep_order(required[:1] + timeline_terms[:1], limit=2),
                match_mode="any",
                proximity_window=12,
                chapter_range=scope,
                limit=120,
            )

        if reason in ("semantic_mismatch", "insufficient_coverage"):
            required = _dedupe_keep_order(uncovered or anchors[:2], limit=2)
            optional = _dedupe_keep_order(list(latest_terms_optional) + timeline_terms + risk_terms + anchors, limit=5)
            return AdaptiveRewrite(
                strategy="adaptive_coverage_focus",
                reason="命中覆盖不足，聚焦未覆盖 must_have",
                search_intent="围绕未覆盖要素重搜",
                keywords=_dedupe_keep_order(required + optional, limit=7),
                terms_required=required,
                terms_optional=[item for item in optional if item not in required],
                terms_excluded=excluded,
                proximity_terms=_dedupe_keep_order(required[:2], limit=2),
                match_mode="all" if len(required) > 1 else "phrase",
                proximity_window=10,
                chapter_range=scope,
                limit=120,
            )

        required = _dedupe_keep_order(list(latest_terms_required) or anchors[:2] or must_have[:2], limit=2)
        optional = _dedupe_keep_order(list(latest_terms_optional) + anchors + timeline_terms + risk_terms, limit=6)
        proximity_terms = _dedupe_keep_order(list(latest_proximity_terms) + required + optional[:1], limit=3)
        return AdaptiveRewrite(
            strategy="adaptive_recall_expand",
            reason="召回不足，扩展语义槽位并放宽匹配",
            search_intent=f"扩展召回：{target_task[:32]}",
            keywords=_dedupe_keep_order(required + optional, limit=7),
            terms_required=required,
            terms_optional=[item for item in optional if item not in required],
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
        if reason in ("scope_miss", "lexical_miss") and lexical_miss_count >= 2:
            return (max(1, start - 2), end + 2)
        return (start, end)


__all__ = [
    "RelationAnchor",
    "IntentSpec",
    "ProbeSpec",
    "QueryProgram",
    "EvidenceCard",
    "IterationState",
    "IntentCompiler",
    "QueryProgramBuilder",
    "EvidenceJudge",
    "AdaptiveRewrite",
    "AdaptiveController",
]
