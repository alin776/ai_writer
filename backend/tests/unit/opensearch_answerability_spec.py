# -*- coding: utf-8 -*-

from pathlib import Path


SOURCE_PATH = Path(__file__).resolve().parents[2] / "app/services/search/opensearch_chapter_search_service.py"


def _source_text() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def test_search_results_include_answerability_score() -> None:
    text = _source_text()
    assert '"answerability_score"' in text
    assert 'top_answerability=%.4f' in text


def test_search_results_sorted_by_answerability() -> None:
    text = _source_text()
    assert 'scored_results.sort(' in text
    assert '-float(item.get("answerability_score") or 0.0)' in text
