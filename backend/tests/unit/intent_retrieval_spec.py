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
        probe_type="boolean",
        terms_required=["你好", "我好"],
        terms_optional=[],
        terms_excluded=[],
        scope=(1, 3),
        match_mode="all",
    )
    sig_b = builder._build_signature(
        probe_type="boolean",
        terms_required=["我好", "你好"],
        terms_optional=[],
        terms_excluded=[],
        scope=(1, 3),
        match_mode="all",
    )
    assert sig_a == sig_b


def test_intent_compiler_prioritizes_quotes_and_seed_terms() -> None:
    compiler = IntentCompiler()
    spec = compiler.compile(
        target_task='定位原句“器灵吞噬”并判断主角是否主动触发',
        seed_keywords=["主角", "吞噬"],
        recent_keywords=["代价", "限制"],
        chapter_scope=(3, 5),
    )
    assert "器灵吞噬" in spec.must_have
    assert any(term in spec.must_have for term in ("主角", "吞噬"))
    assert spec.constraints.get("chapter_scope") == [3, 5]


def test_query_program_builder_skips_seen_signatures() -> None:
    compiler = IntentCompiler()
    builder = QueryProgramBuilder()
    state = IterationState()
    intent = compiler.compile(
        target_task="检查器灵吞噬的触发条件",
        seed_keywords=["器灵", "吞噬", "触发条件"],
        recent_keywords=[],
        chapter_scope=(1, 10),
    )
    program = builder.build(
        intent=intent,
        manual_keywords=["器灵", "吞噬"],
        requested_match_mode="all",
        chapter_scope=(1, 10),
        iteration_state=state,
    )
    first_probe = builder.pick_next_probe(program, state)
    assert first_probe is not None
    state.mark_probe(first_probe.signature)
    next_probe = builder.pick_next_probe(program, state)
    assert next_probe is not None
    assert next_probe.signature != first_probe.signature


def test_evidence_judge_returns_semantic_mismatch_when_uncovered() -> None:
    compiler = IntentCompiler()
    judge = EvidenceJudge()
    intent = compiler.compile(
        target_task="找出主角第一次吞噬器灵的原文段落",
        seed_keywords=["主角", "吞噬", "器灵"],
        recent_keywords=[],
        chapter_scope=(1, 12),
    )
    summary = judge.judge(
        results=[
            {
                "chapter_order": 2,
                "paragraph_index": 11,
                "text": "天气很好，众人闲聊晚饭吃什么。",
            }
        ],
        intent=intent,
        active_keywords=["主角", "吞噬", "器灵"],
    )
    assert summary["failure_reason"] in ("semantic_mismatch", "insufficient_coverage")
    assert summary["coverage_ratio"] == 0.0


def test_evidence_judge_reports_coverage_for_matching_result() -> None:
    compiler = IntentCompiler()
    judge = EvidenceJudge()
    intent = compiler.compile(
        target_task="找出主角第一次吞噬器灵的原文段落",
        seed_keywords=["主角", "吞噬", "器灵"],
        recent_keywords=[],
        chapter_scope=(1, 12),
    )
    summary = judge.judge(
        results=[
            {
                "chapter_order": 4,
                "paragraph_index": 9,
                "text": "主角在濒死时第一次吞噬器灵，体内灵力暴涨。",
            }
        ],
        intent=intent,
        active_keywords=["主角", "吞噬", "器灵"],
    )
    assert summary["failure_reason"] == ""
    assert summary["coverage_ratio"] > 0
    assert summary["covered_terms"]
