# -*- coding: utf-8 -*-
"""Intent-driven lexical retrieval helpers for Explore V2."""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path
from dataclasses import dataclass, field
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
QUOTE_PATTERN = re.compile(r'["“”‘’「」『』《》](.+?)["“”‘’「」『』》]')
TASK_TERM_PATTERN = re.compile(r"[\u4e00-\u9fffA-Za-z0-9]{2,24}")

DEFAULT_STOP_TERMS = {
    "需要",
    "相关",
    "内容",
    "信息",
    "检索",
    "搜索",
    "查询",
    "提取",
    "定位",
    "关键词",
    "策略",
    "章节",
    "段落",
    "原文",
    "是否",
    "已经",
    "没有",
    "请",
    "帮我",
    "然后",
    "以及",
    "还有",
}

EXCLUSION_PATTERNS = (
    r"(?:不要|排除|不含|去掉|忽略)([\u4e00-\u9fffA-Za-z0-9]{2,24})",
    r"(?:excluding|except)\s+([A-Za-z0-9_\-]{2,24})",
)

EVIDENCE_SHAPE_HINTS = {
    "dialogue": ("对话", "台词", "说", "问", "回答"),
    "action": ("动作", "打斗", "追逐", "冲突", "战斗"),
    "description": ("描写", "环境", "心理", "氛围", "细节"),
    "paragraph": ("段落", "段", "句子", "原句"),
    "chapter": ("整章", "全章", "章节原文", "全文"),
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


def _dedupe_keep_order(values: Iterable[str], limit: int = 0) -> List[str]:
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
        terms = _dedupe_keep_order(
            list(self.terms_required) + list(self.terms_optional),
            limit=limit,
        )
        return terms

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
    novelty_rule: str = "next probe must add new lexical anchor or scope constraint"

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


class IntentCompiler:
    """Compile user task + runtime context into a structured lexical intent."""

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
        seed_terms = _dedupe_keep_order(seed_keywords or [], limit=8)
        recent_terms = _dedupe_keep_order(recent_keywords or [], limit=8)

        must_have = _dedupe_keep_order(
            list(quoted_terms) + list(seed_terms) + list(task_terms),
            limit=8,
        )
        if not must_have:
            must_have = _dedupe_keep_order(task_terms, limit=4)

        nice_to_have = _dedupe_keep_order(
            list(recent_terms) + [term for term in task_terms if term not in must_have],
            limit=8,
        )
        exclusions = self._extract_exclusions(goal)
        evidence_shape = self._detect_evidence_shape(goal)

        scope = _safe_scope_tuple(chapter_scope)
        constraints: Dict[str, Any] = {}
        if scope:
            constraints["chapter_scope"] = list(scope)

        stop_rule = {
            "min_must_have_coverage": 0.6,
            "min_evidence_cards": 2,
            "max_zero_growth_rounds": 2,
        }

        digest_payload = "|".join(
            [
                goal[:200],
                ",".join(must_have),
                ",".join(exclusions),
                str(constraints.get("chapter_scope") or ""),
            ]
        )
        intent_id = hashlib.sha1(digest_payload.encode("utf-8")).hexdigest()[:16]

        return IntentSpec(
            intent_id=intent_id,
            goal=goal[:400],
            must_have=must_have,
            nice_to_have=nice_to_have,
            constraints=constraints,
            exclusions=exclusions,
            evidence_shape=evidence_shape,
            stop_rule=stop_rule,
            source_keywords=_dedupe_keep_order(list(seed_terms) + list(recent_terms), limit=10),
        )

    def _extract_quoted_terms(self, text: str) -> List[str]:
        terms: List[str] = []
        for match in QUOTE_PATTERN.findall(text or ""):
            normalized = _normalize_term(match)
            if len(normalized) < 2:
                continue
            terms.append(normalized)
        return _dedupe_keep_order(terms, limit=8)

    def _extract_task_terms(self, text: str) -> List[str]:
        terms: List[str] = []
        for raw in TASK_TERM_PATTERN.findall(text or ""):
            normalized = _normalize_term(raw)
            if len(normalized) < 2:
                continue
            if normalized in DEFAULT_STOP_TERMS:
                continue
            if re.fullmatch(r"第?\d+章", normalized):
                continue
            terms.append(normalized)
        return _dedupe_keep_order(terms, limit=16)

    def _extract_exclusions(self, text: str) -> List[str]:
        exclusions: List[str] = []
        source = str(text or "")
        for pattern in EXCLUSION_PATTERNS:
            for match in re.findall(pattern, source):
                normalized = _normalize_term(match)
                if len(normalized) < 2:
                    continue
                exclusions.append(normalized)
        return _dedupe_keep_order(exclusions, limit=6)

    def _detect_evidence_shape(self, text: str) -> str:
        value = str(text or "")
        for shape, hints in EVIDENCE_SHAPE_HINTS.items():
            if any(hint in value for hint in hints):
                return shape
        return "paragraph"


class QueryProgramBuilder:
    """Build and pick lexical probes from IntentSpec."""

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

        manual_terms = _dedupe_keep_order(manual_keywords or [], limit=8)
        anchor_terms = _dedupe_keep_order(
            list(manual_terms) + list(intent.must_have) + list(intent.nice_to_have),
            limit=10,
        )
        if not anchor_terms and intent.goal:
            anchor_terms = _dedupe_keep_order(_split_terms(intent.goal), limit=6)

        probes: List[ProbeSpec] = []
        safe_scope = _safe_scope_tuple(chapter_scope)

        if anchor_terms:
            required = anchor_terms[:2]
            optional = anchor_terms[2:4]
            probes.append(
                self._new_probe(
                    probe_type="boolean",
                    required=required,
                    optional=optional,
                    excluded=intent.exclusions,
                    scope=safe_scope,
                    match_mode="all" if len(required) > 1 else "phrase",
                    hypothesis="先验证任务主锚点是否同段共现",
                    strategy="intent_probe",
                    priority=1,
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
                    hypothesis=f"验证关系邻近是否成立：{anchor_terms[0]} ~ {anchor_terms[1]}",
                    strategy="proximity_probe",
                    priority=2,
                )
            )

        for term in intent.must_have[:2]:
            probes.append(
                self._new_probe(
                    probe_type="phrase",
                    required=[term],
                    optional=[],
                    excluded=intent.exclusions,
                    scope=safe_scope,
                    match_mode="phrase",
                    hypothesis=f"验证关键短语“{term}”是否出现",
                    strategy="phrase_probe",
                    priority=2,
                )
            )

        if intent.exclusions:
            probes.append(
                self._new_probe(
                    probe_type="exclude_filter",
                    required=anchor_terms[:2] or intent.must_have[:1],
                    optional=anchor_terms[2:4],
                    excluded=intent.exclusions,
                    scope=safe_scope,
                    match_mode=mode or "any",
                    hypothesis="在排除条件下验证主锚点命中",
                    strategy="exclude_probe",
                    priority=3,
                )
            )

        governed = govern_search_keywords(
            keywords=anchor_terms,
            target_task=intent.goal,
            max_keywords=8,
            min_keywords=1,
            enable_alias_expand=True,
        )
        clusters = governed.get("clusters") or []
        for cluster in clusters[:3]:
            if not isinstance(cluster, dict):
                continue
            root = _normalize_term(cluster.get("root"))
            variants = _dedupe_keep_order(cluster.get("variants") or [], limit=3)
            if not root:
                continue
            optional = [term for term in variants if term != root][:2]
            if not optional:
                continue
            probes.append(
                self._new_probe(
                    probe_type="alias_expand",
                    required=[root],
                    optional=optional,
                    excluded=intent.exclusions,
                    scope=safe_scope,
                    match_mode="any",
                    hypothesis=f"验证别名扩展是否能补充召回：{root}",
                    strategy="alias_probe",
                    priority=4,
                )
            )

        for term in anchor_terms[:4]:
            probes.append(
                self._new_probe(
                    probe_type="fallback",
                    required=[term],
                    optional=[],
                    excluded=intent.exclusions,
                    scope=safe_scope,
                    match_mode="any",
                    hypothesis=f"单锚点回查：{term}",
                    strategy="single_anchor",
                    priority=5,
                )
            )

        deduped: List[ProbeSpec] = []
        seen_signatures: Set[str] = set()
        for probe in sorted(probes, key=lambda item: (item.priority, item.probe_type)):
            if not probe.signature or probe.signature in seen_signatures:
                continue
            if probe.signature in iteration_state.seen_probe_signatures:
                continue
            seen_signatures.add(probe.signature)
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
            novelty_rule="new probe must add a new lexical anchor or a different scope",
        )

    def pick_next_probe(self, program: QueryProgram, iteration_state: IterationState) -> Optional[ProbeSpec]:
        for probe in program.probes:
            if probe.signature not in iteration_state.seen_probe_signatures:
                return probe
        return None

    def probe_to_search_payload(self, probe: ProbeSpec, limit: int = 100) -> Dict[str, Any]:
        proximity_terms: List[str] = []
        proximity_window = 12
        if probe.probe_type == "proximity":
            proximity_terms = _dedupe_keep_order(
                list(probe.terms_required[:2]) + list(probe.terms_optional[:1]),
                limit=3,
            )
            proximity_window = 10
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
        terms_required = _dedupe_keep_order(required, limit=6)
        terms_optional = _dedupe_keep_order(optional, limit=6)
        terms_excluded = _dedupe_keep_order(excluded, limit=6)
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
        normalized_optional = sorted({_normalize_term(term).lower() for term in terms_optional if _normalize_term(term)})
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
    """Score lexical hits against IntentSpec coverage requirements."""

    def judge(
        self,
        results: Sequence[Dict[str, Any]],
        intent: IntentSpec,
        active_keywords: Sequence[str],
        min_score: float = 0.2,
    ) -> Dict[str, Any]:
        must_terms = _dedupe_keep_order(intent.must_have, limit=8)
        keyword_terms = _dedupe_keep_order(active_keywords, limit=8)
        cards: List[EvidenceCard] = []
        covered_terms: Set[str] = set()
        score_total = 0.0

        for item in results:
            if not isinstance(item, dict):
                continue
            text = str(item.get("text") or item.get("content") or item.get("snippet") or "")
            if not text:
                continue
            lowered = text.lower()
            matched_must = [term for term in must_terms if term.lower() in lowered]
            matched_keywords = [term for term in keyword_terms if term.lower() in lowered]
            locator_bonus = 0.1 if isinstance(item.get("chapter_order"), int) and isinstance(item.get("paragraph_index"), int) else 0.0

            must_ratio = (len(matched_must) / len(must_terms)) if must_terms else 0.0
            keyword_ratio = (len(matched_keywords) / len(keyword_terms)) if keyword_terms else 0.0
            score = (must_ratio * 0.7) + (keyword_ratio * 0.2) + locator_bonus
            score_total += score

            reason = "matched intent anchors" if matched_must else "lexical hit but weak intent coverage"
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
            if score >= min_score:
                covered_terms.update(card.covers_must_have)

        avg_score = (score_total / len(cards)) if cards else 0.0
        if not cards:
            failure_reason = "lexical_miss"
        elif covered_terms:
            failure_reason = ""
        elif avg_score < min_score:
            failure_reason = "semantic_mismatch"
        else:
            failure_reason = "insufficient_coverage"

        coverage_ratio = (len(covered_terms) / len(must_terms)) if must_terms else 0.0
        return {
            "cards": [card.to_dict() for card in cards],
            "covered_terms": sorted(covered_terms),
            "coverage_ratio": round(float(coverage_ratio), 4),
            "failure_reason": failure_reason,
            "avg_score": round(float(avg_score), 4),
        }
