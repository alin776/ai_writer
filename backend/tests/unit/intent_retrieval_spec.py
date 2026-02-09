# -*- coding: utf-8 -*-

import importlib.util
import sys
from pathlib import Path


SOURCE_PATH = Path(__file__).resolve().parents[2] / "app/services/agent/utils/intent_retrieval.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("intent_retrieval_local", SOURCE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


intent_retrieval_module = _load_module()
IntentCompiler = intent_retrieval_module.IntentCompiler
QueryProgramBuilder = intent_retrieval_module.QueryProgramBuilder
EvidenceJudge = intent_retrieval_module.EvidenceJudge
IterationState = intent_retrieval_module.IterationState


def test_probe_signature_is_order_invariant() -> None:
    builder = QueryProgramBuilder()
    sig_a = builder._build_signature(
        probe_type="relation",
        terms_required=["你好", "我好"],
        terms_optional=[],
        terms_excluded=[],
        scope=(1, 3),
        match_mode="all",
    )
    sig_b = builder._build_signature(
        probe_type="relation",
        terms_required=["我好", "你好"],
        terms_optional=[],
        terms_excluded=[],
        scope=(1, 3),
        match_mode="all",
    )
    assert sig_a == sig_b


def test_probe_signature_collapses_prompt_shell_and_suffix_noise() -> None:
    builder = QueryProgramBuilder()
    sig_a = builder._build_signature(
        probe_type="core_boolean",
        terms_required=["查找关于五虎群羊刀"],
        terms_optional=["代价"],
        terms_excluded=[],
        scope=(1, 5),
        match_mode="all",
    )
    sig_b = builder._build_signature(
        probe_type="core_boolean",
        terms_required=["五虎群羊刀"],
        terms_optional=["代价"],
        terms_excluded=[],
        scope=(1, 5),
        match_mode="all",
    )
    assert sig_a == sig_b


def test_compiler_extracts_semantic_slots_and_relation_anchor() -> None:
    compiler = IntentCompiler()
    spec = compiler.compile(
        target_task='定位“主角吞噬器灵”第一次发生的原文，并确认是否有代价',
        seed_keywords=["主角", "吞噬", "器灵", "查找关于吞噬事件的描述"],
        recent_keywords=["代价", "反噬"],
        chapter_scope=(1, 5),
    )
    assert spec.constraints.get("chapter_scope") == [1, 5]
    assert spec.relation_anchors
    assert any(anchor.action in ("吞噬", "主角吞噬器灵") or "吞噬" in anchor.action for anchor in spec.relation_anchors)
    assert any(term in spec.must_have for term in ("主角", "吞噬", "器灵"))
    # 指令语句不应进入 must_have
    assert all("查找关于" not in term for term in spec.must_have)


def test_query_program_prioritizes_relation_probe() -> None:
    compiler = IntentCompiler()
    builder = QueryProgramBuilder()
    state = IterationState()
    intent = compiler.compile(
        target_task="找主角第一次吞噬器灵并判断代价",
        seed_keywords=["主角", "吞噬", "器灵", "代价"],
        recent_keywords=[],
        chapter_scope=(1, 10),
    )
    program = builder.build(
        intent=intent,
        manual_keywords=["主角", "吞噬", "器灵"],
        requested_match_mode="all",
        chapter_scope=(1, 10),
        iteration_state=state,
    )
    assert program.probes
    first = program.probes[0]
    assert first.probe_type in ("relation", "core_boolean")


def test_sanitize_external_keywords_drops_instruction_noise() -> None:
    compiler = IntentCompiler()
    cleaned = compiler.sanitize_external_keywords(
        [
            "查找关于'器灵'、'刀灵'或'牛尾刀器灵'的首次提及",
            "器灵",
            "刀灵",
            "牛尾刀器灵",
        ],
        target_task="围绕器灵事件取证",
        limit=8,
    )
    assert "器灵" in cleaned
    assert "刀灵" in cleaned
    assert all("查找关于" not in item for item in cleaned)


def test_evidence_judge_returns_relation_miss_when_relation_not_hit() -> None:
    compiler = IntentCompiler()
    judge = EvidenceJudge()
    intent = compiler.compile(
        target_task="找主角第一次吞噬器灵的原文",
        seed_keywords=["主角", "吞噬", "器灵"],
        recent_keywords=[],
        chapter_scope=(1, 12),
    )
    summary = judge.judge(
        results=[
            {
                "chapter_order": 2,
                "paragraph_index": 11,
                "text": "主角看着器灵，却没有进行吞噬，只是暂时收起。",
            }
        ],
        intent=intent,
        active_keywords=["主角", "吞噬", "器灵"],
    )
    assert summary["failure_reason"] in ("relation_miss", "insufficient_coverage", "semantic_mismatch")


def test_evidence_judge_reports_coverage_for_relation_hit() -> None:
    compiler = IntentCompiler()
    judge = EvidenceJudge()
    intent = compiler.compile(
        target_task="找主角第一次吞噬器灵并确认代价",
        seed_keywords=["主角", "吞噬", "器灵", "代价"],
        recent_keywords=[],
        chapter_scope=(1, 12),
    )
    summary = judge.judge(
        results=[
            {
                "chapter_order": 4,
                "paragraph_index": 9,
                "text": "主角在濒死时第一次吞噬器灵，随后检查是否有代价。",
            }
        ],
        intent=intent,
        active_keywords=["主角", "吞噬", "器灵", "代价"],
    )
    assert summary["failure_reason"] == ""
    assert summary["coverage_ratio"] > 0
    assert summary["covered_terms"]
    assert summary["relation_hits"] >= 1
