# -*- coding: utf-8 -*-

from pathlib import Path


SOURCE_PATH = Path(__file__).resolve().parents[2] / "app/services/agent/execution/tool_executor.py"


def _source_text() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_tool_executor_allows_retrieval_intent_param() -> None:
    text = _source_text()
    assert '"retrieval_intent"' in text
    assert 'allowed_keys = {' in text


def test_tool_executor_v6_direct_path() -> None:
    """V6 直接调用，无 V5 回退。"""
    text = _source_text()
    assert "ExploreV6" in text
    assert "explore_content 使用 V6 完成" in text
    # 不应存在 V5 回退逻辑
    assert "V6 失败，回退 V5" not in text
    assert "EXPLORE_V6_ENABLED" not in text
