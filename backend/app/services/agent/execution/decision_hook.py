# -*- coding: utf-8 -*-
"""Decision Hook - 执行期自救补救任务生成器（禁用 locate_content）"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class DecisionOutcome:
    def __init__(self, tasks: Optional[List[Dict[str, Any]]] = None, pause_message: Optional[str] = None):
        self.tasks = tasks or []
        self.pause_message = pause_message


class DecisionHook:
    DEFAULT_MAX_REMEDIES = 2
    ERROR_TRIGGERS = {
        "ambiguous_locator",
        "locator_not_found",
        "locator_index_out_of_range",
        "missing_locate_targets",
        "missing_keywords",
        "tool_disabled",
    }

    def __init__(self, max_remedies: int | None = None):
        self.max_remedies = max_remedies or self.DEFAULT_MAX_REMEDIES

    def evaluate(
        self,
        task: Dict[str, Any],
        result: Dict[str, Any],
        shared_state: Optional[Dict[str, Any]] = None,
    ) -> DecisionOutcome:
        if not isinstance(task, dict) or not isinstance(result, dict):
            return DecisionOutcome()

        payload = self._extract_payload(result)
        if not payload:
            return DecisionOutcome()

        error = payload.get("error") or payload.get("status")
        missing_keywords = payload.get("missing_keywords") if isinstance(payload.get("missing_keywords"), list) else []

        should_trigger = False
        if error in self.ERROR_TRIGGERS:
            should_trigger = True
        if missing_keywords:
            should_trigger = True

        if not should_trigger:
            return DecisionOutcome()

        budget_ok, budget_left = self._consume_budget(shared_state, task.get("task_id"))
        if not budget_ok:
            return DecisionOutcome(
                pause_message=f"定位信息不足（已尝试{self.max_remedies}次补救）。请指定更明确的位置（例如“第几处/第几段/具体锚点”）。"
            )

        hint = self._build_hint(task, payload)
        search_keywords = self._extract_keywords(hint)
        if missing_keywords:
            search_keywords = list({*search_keywords, *[kw for kw in missing_keywords if isinstance(kw, str)]})

        remedy = {
            "title": "补充定位证据",
            "description": f"补充定位证据：{hint or '定位目标段落'}",
            "tool": "explore_content",
            "params": {
                "target_task": hint or "补充定位证据，产出可定位段落",
                "search_keywords": search_keywords or None,
                "require_paragraph_index": True,
                "output_mode": "full",
                "force_refresh": True,
            },
            "depends_on": [task.get("task_id")],
        }

        tasks = self._dedupe_tasks(shared_state, [remedy])
        if not tasks:
            return DecisionOutcome(
                pause_message="定位补救任务已重复或无效，请明确指定第几处/哪段。"
            )
        logger.info("[DecisionHook] 触发补救任务: %s", tasks)
        return DecisionOutcome(tasks=tasks)

    @staticmethod
    def _extract_payload(result: Dict[str, Any]) -> Dict[str, Any]:
        raw = result.get("raw_result")
        if isinstance(raw, dict):
            return raw
        if isinstance(raw, str):
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass
        text = result.get("result")
        if isinstance(text, str):
            try:
                parsed = json.loads(text)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                return {}
        return {}

    @staticmethod
    def _build_hint(task: Dict[str, Any], payload: Dict[str, Any]) -> str:
        params = task.get("params", {}) if isinstance(task.get("params"), dict) else {}
        candidates = [
            params.get("locate_target_hint"),
            params.get("user_intent"),
            params.get("text_to_rewrite"),
            params.get("insert_context"),
            params.get("target_description"),
            params.get("original_text"),
            payload.get("message"),
            task.get("description"),
        ]
        for item in candidates:
            if isinstance(item, str) and item.strip():
                return item.strip()
        return ""

    def _consume_budget(self, shared_state: Optional[Dict[str, Any]], task_id: Any) -> Tuple[bool, int]:
        if not isinstance(shared_state, dict):
            return True, self.max_remedies
        budget = shared_state.setdefault("decision_budget", {})
        try:
            key = str(task_id)
        except Exception:
            key = "unknown"
        count = int(budget.get(key, 0))
        if count >= self.max_remedies:
            return False, 0
        budget[key] = count + 1
        return True, self.max_remedies - (count + 1)

    @staticmethod
    def _extract_keywords(text: str) -> List[str]:
        if not isinstance(text, str) or not text.strip():
            return []
        quotes = re.findall(r'["“”‘’「」『』《》](.+?)["“”‘’「」『』》]', text)
        if quotes:
            return list({q.strip() for q in quotes if q.strip()})
        cleaned = re.sub(r"[\\s,，。；;：:、.!?？]+", " ", text).strip()
        parts = [p for p in cleaned.split(" ") if p and len(p) >= 2]
        if parts:
            return list(dict.fromkeys(parts))[:8]
        return [text.strip()[:20]] if text.strip() else []

    @staticmethod
    def _dedupe_tasks(shared_state: Optional[Dict[str, Any]], tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not isinstance(shared_state, dict):
            return tasks
        raw_seen = shared_state.setdefault("decision_seen", [])
        seen_set = set(raw_seen) if isinstance(raw_seen, list) else set()
        unique: List[Dict[str, Any]] = []
        for task in tasks:
            signature = f"{task.get('tool')}:{json.dumps(task.get('params', {}), sort_keys=True, ensure_ascii=False)}"
            if signature in seen_set:
                continue
            seen_set.add(signature)
            unique.append(task)
        shared_state["decision_seen"] = list(seen_set)
        return unique
