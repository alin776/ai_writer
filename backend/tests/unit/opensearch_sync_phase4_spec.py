# -*- coding: utf-8 -*-

from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
OPENSEARCH_SERVICE = BASE / "app/services/search/opensearch_chapter_search_service.py"
CHAPTER_VECTOR_SERVICE = BASE / "app/services/chapter_vector_service.py"
MAIN_FILE = BASE / "app/main.py"
MODELS_INIT = BASE / "app/models/__init__.py"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_phase4_sync_methods_are_present() -> None:
    text = _text(OPENSEARCH_SERVICE)
    required_snippets = [
        "async def mark_chapter_sync_success(",
        "async def mark_chapter_sync_failure(",
        "async def process_retry_queue(",
        "async def audit_work_consistency(",
        "async def runtime_consistency_guard(",
        "async def audit_all_works(",
    ]
    for snippet in required_snippets:
        assert snippet in text


def test_search_path_invokes_runtime_guard() -> None:
    text = _text(OPENSEARCH_SERVICE)
    assert "await self.runtime_consistency_guard(str(work_id))" in text


def test_chapter_vector_service_reports_sync_result_and_failure() -> None:
    text = _text(CHAPTER_VECTOR_SERVICE)
    assert "await search_service.mark_chapter_sync_success(" in text
    assert "await search_service.mark_chapter_sync_failure(" in text


def test_startup_runs_sync_audit_and_model_registered() -> None:
    main_text = _text(MAIN_FILE)
    models_text = _text(MODELS_INIT)
    assert "OPENSEARCH_SYNC_AUDIT_ON_STARTUP" in main_text
    assert "audit_all_works(" in main_text
    assert "OpenSearchSyncStatus" in models_text
