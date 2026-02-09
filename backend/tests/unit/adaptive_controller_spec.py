# -*- coding: utf-8 -*-

import importlib.util
import sys
from pathlib import Path


SOURCE_PATH = Path(__file__).resolve().parents[2] / "app/services/agent/utils/adaptive_controller.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("adaptive_controller_local", SOURCE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


MODULE = _load_module()
AdaptiveController = MODULE.AdaptiveController


def test_semantic_mismatch_focuses_uncovered_must_have() -> None:
    controller = AdaptiveController()
    rewrite = controller.build_rewrite(
        failure_reason="semantic_mismatch",
        target_task="找主角第一次吞噬器灵并确认代价",
        intent_spec={
            "must_have": ["主角", "吞噬", "器灵", "代价"],
            "nice_to_have": ["风险"],
            "source_keywords": ["吞噬", "器灵"],
        },
        iteration_state={
            "covered_must_have_set": ["主角", "吞噬"],
            "failed_reason_histogram": {},
        },
        latest_keywords=["主角", "吞噬", "器灵"],
        latest_terms_required=["主角", "吞噬"],
        latest_terms_optional=[],
        latest_terms_excluded=[],
        latest_proximity_terms=[],
        latest_scope=(3, 5),
        seed_keywords=["代价"],
    )
    assert rewrite is not None
    payload = rewrite.to_search_args()
    assert payload["strategy"] == "adaptive_semantic_focus"
    assert any(term in payload["terms_required"] for term in ("器灵", "代价"))
    assert payload["match_mode"] in ("all", "phrase")


def test_lexical_miss_can_widen_scope() -> None:
    controller = AdaptiveController()
    rewrite = controller.build_rewrite(
        failure_reason="lexical_miss",
        target_task="找器灵吞噬机制",
        intent_spec={"must_have": ["器灵", "吞噬"], "nice_to_have": [], "source_keywords": ["器灵", "吞噬"]},
        iteration_state={"covered_must_have_set": [], "failed_reason_histogram": {"lexical_miss": 2}},
        latest_keywords=["器灵", "吞噬"],
        latest_terms_required=["器灵", "吞噬"],
        latest_terms_optional=[],
        latest_terms_excluded=[],
        latest_proximity_terms=[],
        latest_scope=(10, 12),
        seed_keywords=[],
    )
    assert rewrite is not None
    payload = rewrite.to_search_args()
    assert payload["strategy"] == "adaptive_recall_expand"
    assert payload.get("chapter_range") == [8, 14]
