# -*- coding: utf-8 -*-

from pathlib import Path


SOURCE_PATH = Path(__file__).resolve().parents[2] / "app/services/agent/planning/plan_generator.py"


def _source_text() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_plan_generator_builds_retrieval_intent_for_explore_tasks() -> None:
    text = _source_text()
    assert "def _build_retrieval_intent_payload(" in text
    assert '"retrieval_intent": retrieval_intent' in text


def test_plan_generator_no_keyword_matching() -> None:
    """plan_generator 不再构建 must_have/source_keywords。"""
    text = _source_text()
    assert "IntentCompiler" not in text
    assert "intent_retrieval" not in text
    # retrieval_intent 只含 goal + entities
    assert '"goal":' in text
    assert '"entities":' in text
