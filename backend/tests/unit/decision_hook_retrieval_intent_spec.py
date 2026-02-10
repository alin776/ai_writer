# -*- coding: utf-8 -*-

import importlib.util
import sys
from pathlib import Path


SOURCE_PATH = Path(__file__).resolve().parents[2] / "app/services/agent/execution/decision_hook.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("decision_hook_local", SOURCE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


decision_hook_module = _load_module()
DecisionHook = decision_hook_module.DecisionHook


def test_decision_hook_emits_retrieval_intent_for_explore_remedy() -> None:
    hook = DecisionHook(max_remedies=2)
    outcome = hook.evaluate(
        task={"task_id": 7, "description": "定位改写段落", "params": {}},
        result={
            "raw_result": {
                "error": "missing_keywords",
                "missing_keywords": ["主角", "吞噬"],
                "message": "缺少定位锚点",
            }
        },
        shared_state={},
    )
    assert outcome.tasks
    remedy = outcome.tasks[0]
    assert remedy.get("tool") == "explore_content"
    params = remedy.get("params") or {}
    assert isinstance(params.get("retrieval_intent"), dict)
    must_have = params["retrieval_intent"].get("must_have") or []
    assert "主角" in must_have or "吞噬" in must_have
    assert params.get("require_paragraph_index") is True
