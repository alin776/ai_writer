# -*- coding: utf-8 -*-

from pathlib import Path


SOURCE_PATH = Path(__file__).resolve().parents[2] / "app/services/agent/planning/plan_generator.py"


def _source_text() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_plan_generator_rechecks_rewrite_apply_path_after_normalize() -> None:
    text = _source_text()
    assert "normalized_plan = self._normalize_plan_schema(plan_data)" in text
    assert 'normalized_plan["tasks"] = self._ensure_replace_original_text(normalized_plan.get("tasks", []))' in text
