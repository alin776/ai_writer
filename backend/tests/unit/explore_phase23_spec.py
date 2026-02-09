# -*- coding: utf-8 -*-

from pathlib import Path


SOURCE_PATH = Path(__file__).resolve().parents[2] / "app/services/agent/tools/explore_tools.py"


def _source_text() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_explore_uses_adaptive_controller_module() -> None:
    text = _source_text()
    assert "AdaptiveController" in text
    assert "self.adaptive_controller.build_rewrite(" in text
    assert "adaptive_overrides" in text


def test_exact_search_passes_phase2_options_to_vector_service() -> None:
    text = _source_text()
    required_snippets = [
        "terms_required=layer_terms_required",
        "terms_optional=layer_terms_optional",
        "terms_excluded=layer_terms_excluded",
        "proximity_terms=layer_proximity_terms",
        "proximity_window=layer_proximity_window",
    ]
    for snippet in required_snippets:
        assert snippet in text


def test_exact_search_result_contains_filter_and_judge_metadata() -> None:
    text = _source_text()
    assert "\"filter_stats\": filter_stats" in text
    assert "\"judge\": {" in text
    assert "\"must_have_coverage_ratio\"" in text


def test_planned_probe_does_not_clear_explicit_required_terms() -> None:
    text = _source_text()
    assert "if \"terms_required\" in planned_payload:" in text
    assert "parsed_required = self._parse_search_term_values(planned_required)" in text
