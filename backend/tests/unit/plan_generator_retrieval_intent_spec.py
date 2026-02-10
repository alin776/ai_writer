# -*- coding: utf-8 -*-

from pathlib import Path


SOURCE_PATH = Path(__file__).resolve().parents[2] / "app/services/agent/planning/plan_generator.py"


def _source_text() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_plan_generator_builds_retrieval_intent_for_explore_tasks() -> None:
    text = _source_text()
    assert "def _build_retrieval_intent_payload(" in text
    assert '"retrieval_intent": retrieval_intent' in text


def test_plan_generator_keeps_search_keywords_as_fallback_only() -> None:
    text = _source_text()
    assert "# 兼容字段：fallback 用。" in text or "兼容字段：fallback" in text
    assert 'rewritten_params["search_keywords"] = keywords[:8]' in text
