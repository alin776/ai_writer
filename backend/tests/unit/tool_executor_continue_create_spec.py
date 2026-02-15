# -*- coding: utf-8 -*-

from pathlib import Path


SOURCE_PATH = Path(__file__).resolve().parents[2] / "app/services/agent/execution/tool_executor.py"


def _source_text() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_tool_executor_supports_append_to_create_upgrade() -> None:
    text = _source_text()
    assert "def _maybe_upgrade_append_to_create(" in text
    assert 'params["operation"] = "create"' in text
    assert "续写目标章节不存在，自动切换 create" in text


def test_tool_executor_keeps_existing_source_locator_on_reselect_failure() -> None:
    text = _source_text()
    assert "if force and not has_explicit_selection and has_existing_locator:" in text
    assert "source_locator 自动重选失败，回退使用已有定位" in text
