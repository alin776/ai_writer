# -*- coding: utf-8 -*-

from pathlib import Path


SOURCE_PATH = Path(__file__).resolve().parents[2] / "app/services/agent/execution/tool_executor.py"


def _source_text() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_tool_executor_rewrites_legacy_explore_with_retrieval_intent() -> None:
    text = _source_text()
    assert '"retrieval_intent": retrieval_intent' in text
    assert "_build_retrieval_intent_payload(" in text


def test_tool_executor_allows_retrieval_intent_param() -> None:
    text = _source_text()
    assert '"retrieval_intent"' in text
    assert 'allowed_keys = {' in text
