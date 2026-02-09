# -*- coding: utf-8 -*-

import ast
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


SOURCE_PATH = Path(__file__).resolve().parents[2] / "app/services/search/opensearch_chapter_search_service.py"


def _load_build_query():
    source = SOURCE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE_PATH))
    fn_node = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "OpenSearchChapterSearchService":
            for child in node.body:
                if isinstance(child, ast.FunctionDef) and child.name == "_build_query":
                    fn_node = child
                    break
    assert fn_node is not None, "_build_query not found"
    module = ast.Module(body=[fn_node], type_ignores=[])
    namespace: Dict[str, Any] = {
        "Any": Any,
        "Dict": Dict,
        "List": List,
        "Optional": Optional,
        "Tuple": Tuple,
    }
    exec(compile(module, str(SOURCE_PATH), "exec"), namespace)
    return namespace["_build_query"]


BUILD_QUERY = _load_build_query()


def test_build_query_contains_exclusion_and_proximity() -> None:
    query = BUILD_QUERY(
        None,
        work_id="work-1",
        keywords=["器灵", "吞噬"],
        chapter_range=(3, 5),
        match_mode="any",
        terms_required=["器灵", "吞噬"],
        terms_optional=["代价"],
        terms_excluded=["误导"],
        proximity_terms=["器灵", "吞噬"],
        proximity_window=9,
    )
    bool_query = query.get("bool", {})
    assert bool_query.get("must")
    assert bool_query.get("must_not")
    should = bool_query.get("should") or []
    assert should, "should clauses expected for optional/proximity"
    has_slop = any(
        isinstance(item, dict)
        and isinstance(item.get("match_phrase"), dict)
        and isinstance(item["match_phrase"].get("chunk_text"), dict)
        and item["match_phrase"]["chunk_text"].get("slop") == 9
        for item in should
    )
    assert has_slop


def test_build_query_all_mode_keeps_required_must() -> None:
    query = BUILD_QUERY(
        None,
        work_id="work-2",
        keywords=["主角", "代价"],
        chapter_range=None,
        match_mode="all",
        terms_required=["主角", "代价"],
        terms_optional=[],
        terms_excluded=[],
        proximity_terms=[],
        proximity_window=None,
    )
    bool_query = query.get("bool", {})
    must = bool_query.get("must") or []
    phrase_count = sum(1 for item in must if isinstance(item, dict) and "match_phrase" in item)
    assert phrase_count >= 2
